
import os
import shutil
import sys

import pandas as pd
import yaml

from const import LOAD_YAML, endpoints, MISSED_SYMBOL

from utils.ammo import gen_request
from config import *
from utils.eval_variables import evaluate_variable, jsonify_variable
from utils.json_handlers import JsonTemplateReader


if __name__ == '__main__':

    try:
        service_config = EnvYAML(SERVICE_FOLDER + "/" + SERVICE_NAME + '.yaml', strict=False)

        #######################
        # Overload settings - begin
        LOAD_YAML['overload']['job_name'] = SERVICE_NAME
        LOAD_YAML['overload']['job_dsc'] = f'Запуск {SERVICE_NAME} с нагрузкой {service_config["rps_type"]}'

        overload_token = open(r'token.txt', 'w', encoding='utf-8')
        overload_token.write(env['load_testing.overload_token'])
        overload_token.close()
        # Overload settings - end
        #######################

        if service_config.get('engine', 'phantom') == 'phantom':
            #######################
            # Phantom settings - begin
            LOAD_YAML['bfg'] = {
                "enabled": False
            }

            LOAD_YAML['phantom']['address'] = service_config['host']
            LOAD_YAML['phantom']['enabled'] = True
            LOAD_YAML['phantom']['load_profile']['load_type'] = service_config['load_type']
            LOAD_YAML['phantom']['load_profile']['schedule'] = service_config['rps_type']

            if service_config.get('ssl', False):
                LOAD_YAML['phantom']['ssl'] = True

            if service_config['instances'] != 'Dynamic_instances':
                LOAD_YAML['phantom']['instances'] = service_config['instances']
                
            if service_config.get('endpoints'):
                for endpoint in service_config['endpoints']:
                    endpoints.append({
                        'title': endpoint['title'],
                        'endpoint': endpoint['endpoint'],
                        'json_file': endpoint['json_file'] if service_config.get('method').lower() == 'post' else None,
                        'json': {}
                    })

            if service_config.get('timeout', 'No') == 'No':
                log.info('10')
                LOAD_YAML['phantom']['timeout'] = '10'
            else:
                log.info(str(service_config.get('timeout')))
                LOAD_YAML['phantom']['timeout'] = str(service_config.get('timeout'))

            if service_config.get('writelog', 'No') != 'No':
                log.info(str(service_config.get('writelog')))
                LOAD_YAML['phantom']['writelog'] = str(service_config.get('writelog'))

            try:
                keys_mapping = service_config['length']['mapping']
            except KeyError as key_error:
                if 'length' in key_error.args or 'mapping' in key_error.args:
                    keys_mapping = []
                else:
                    raise key_error

            excel = pd.ExcelFile(SERVICE_FOLDER + "/" + EXCEL_TEMPLATE)

            results = []
            for sheet in excel.sheet_names:
                df = excel.parse(sheet, header=1)
                excel_vars = {
                    'sheet_name': sheet
                }
                log.debug(f'Sheet %s' % excel_vars)
                log.debug(f'Amount columns: %s' % len(df.columns))

                json_file = JsonTemplateReader(SERVICE_FOLDER + "/" + JSON_FOLDER + '/' + sheet)
                log.debug(f'Json file %s' % json_file)
                json_data = json_file.read()
                for json_template in df.to_dict(orient='records'):
                    tmp_data = json_data
                    for key, val in json_template.items():
                        if any(key in d for d in keys_mapping):
                            len_key = keys_mapping[next(i for i, d in enumerate(keys_mapping) if key in d)][key]
                            log.debug('For key %s length must be %d' % (key, len_key))
                            if len(str(val)) > len_key:
                                val = str(val)[:-len_key or None]
                            elif len(str(val)) < len_key:
                                missed = len_key - len(str(val))
                                val = str(missed * MISSED_SYMBOL) + str(val)
                            log.debug('New value is %s' % val)

                        if str(val) == 'NoValue':
                            val = ""
                        print(tmp_data, key, str(val))
                        tmp_data = jsonify_variable(tmp_data, key, str(val))
                    log.debug(f'Json %s' % tmp_data)
                    print(f'Json %s' % tmp_data)

                    for endpoint in endpoints:
                        if service_config.get('method').lower() == 'post':
                            if endpoint['json_file'] == sheet:
                                endpoint['json'] = tmp_data
                                results.append(dict(endpoint))
                        elif service_config.get('method').lower() == 'get':
                            endpoint['json'] = {}
                            results.append(dict(endpoint))
            log.warning(f'All jsons %s' % results)

            log.debug('Load.yaml: %s' % LOAD_YAML)

            log.debug('Amount of requests %s' % len(results))
            endpoints = results * service_config['ammount_rps']
            log.debug('Amount of requests %s' % len(results))

            file = open(r'ammo.txt', 'w', encoding='utf-8')
            for i, endpoint in enumerate(results):
                log.debug(f'{i}- {endpoint}')
                print(str(endpoint['json']))
                temp_json = evaluate_variable(value=str(endpoint['json']), index_i=i) \
                    if service_config.get('method').lower() == 'post' else None
                log.debug(f'{temp_json}')
                r = gen_request(service_config['method'],
                                endpoint['endpoint'],
                                str(service_config['host']),
                                {
                                    'Accept': '*/*',
                                    'Content-Type': 'application/json',
                                    'Connection': 'Close'
                                },
                                str(temp_json) if service_config.get('method').lower() == 'post' else '')
                log.debug(r)
                file.write(r)
            file.close()

            # Phantom settings - end
            #######################
        elif service_config.get('engine') == 'bfg':
            #######################
            # BFG settings - begin
            LOAD_YAML['phantom'] = {
                "enabled": False
            }
            LOAD_YAML['bfg']['enabled'] = True
            LOAD_YAML['bfg']['instances'] = service_config.get('instances', '10')
            LOAD_YAML['bfg']['loop'] = service_config.get('bfg_loop', '100')
            LOAD_YAML['bfg']['gun_config']['class_name'] = service_config.get('class_name', 'NoValue')
            LOAD_YAML['bfg']['gun_config']['module_name'] = service_config.get('module_name', 'NoValue')
            LOAD_YAML['bfg']['gun_config']['host'] = service_config.get('host', 'NoValue')
            LOAD_YAML['bfg']['load_profile']['load_type'] = service_config.get('load_type', 'rps')
            LOAD_YAML['bfg']['load_profile']['schedule'] = service_config.get('rps_type', 'const(10, 60s)')

            if LOAD_YAML['bfg']['gun_config']['class_name'] == 'NoValue' or \
                    LOAD_YAML['bfg']['gun_config']['module_name'] == 'NoValue' or \
                    LOAD_YAML['bfg']['gun_config']['host'] == 'NoValue':
                sys.exit(1)
            else:
                shutil.copy(SERVICE_FOLDER + '/' +
                            LOAD_YAML['bfg']['gun_config']['module_name'] + '.py',
                            LOAD_YAML['bfg']['gun_config']['module_name'] + '.py')

                for ext in [".pdf", ".json"]:
                    results = [each for each in os.listdir(SERVICE_FOLDER) if each.endswith(ext)]
                    if len(results) > 0:
                        for result in results:
                            log.info(result)
                            shutil.copy(SERVICE_FOLDER + '/' + result, result)

            with open("ammo.line", "w") as file:
                file.write('{"test1": "test_value", "test2": "test_value2"}')
            # BFG settings - end
            ####################### jsonify_variable
        else:
            log.info(f"Unknown type {service_config.get('engine', 'phantom')} of engine.")
            sys.exit(1)

        ######################
        # Create load.yaml - begin
        with open(r'load.yaml', 'w') as file:
            documents = yaml.dump(LOAD_YAML, file)
        # Create load.yaml - end
        ######################
    except FileNotFoundError as file_error:
        log.error(file_error)
