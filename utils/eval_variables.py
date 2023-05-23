import logging
import random
from datetime import datetime
from typing import Any
from string import Template
from uuid import uuid4
log: logging.Logger = logging.getLogger(__name__)


def random_uuid() -> Any:
    return str(uuid4())


def random_bool() -> Any:
    return str(random.choice([True, False])).lower()
    # return True


def random_int(a: int, b: int) -> Any:
    return random.randint(a, b)


def now_date_time() -> Any:
    return datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')


functions_matching = {
    'now_date_time': now_date_time(),
    'random_uuid': random_uuid(),
    'random_int': random_int(1, 1000000),
    'random_bool': random_bool()
}


def evaluate_variable(value: str, index_i: int = 0) -> Any:
    templates = [s[1] or s[2] for s in Template.pattern.findall(value) if s[1] or s[2]]
    if templates:
        temp = {}
        for template in templates:
            log.debug(f'Got template %s' % template)
            if template != 'num_int':
                temp[template] = functions_matching[template]
            else:
                temp[template] = index_i
        result = Template(value).safe_substitute(temp)
    else:
        log.debug(f'No template found in string %s' % value)
        result = value
    return result


def jsonify_variable(file_data: Any, variable: str, value: Any):
    return str(file_data).replace("${" + variable + "}", value) \
        .replace('None', 'null') \
        .replace('False', 'false') \
        .replace('True', 'true')

