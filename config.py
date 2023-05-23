
import logging

from envyaml import EnvYAML

logging.basicConfig(
    filename='load_testing.log',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log = logging.getLogger(__name__)

env = EnvYAML(yaml_file='./config.yaml', strict=False)
SERVICE_NAME = env['load_testing.service']
log.info(f'Service name: %s' % SERVICE_NAME)
SERVICE_FOLDER = env['load_testing.path'] + '/' + SERVICE_NAME
log.info(f'Service folder: %s' % SERVICE_FOLDER)
EXCEL_TEMPLATE = env['load_testing.excel_template']
log.info(f'Excel template: %s' % EXCEL_TEMPLATE)
JSON_FOLDER = env['load_testing.json_folder']
log.info(f'Json folder: %s' % JSON_FOLDER)