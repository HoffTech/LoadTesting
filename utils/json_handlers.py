import io
import json
import os
import shutil


class JsonTemplateReader:

    def __init__(self, file_way):
        tmp_file_way = os.path.dirname(file_way) + \
                       '/tmp_' + \
                       os.path.basename(file_way)
        shutil.copy(file_way, tmp_file_way)
        file_way = tmp_file_way
        self.file_way = file_way

    def set_variable(self, variable, value, encoding: str = 'cp1251'):
        with open(self.file_way, 'r', encoding=encoding) as _f:
            file_data = _f.read()

        file_data = file_data.replace("${" + variable + "}", value)

        with open(self.file_way, 'w', encoding=encoding) as _f:
            _f.write(file_data)

    def read(self, encoding: str = 'cp1251'):
        with io.open(self.file_way, "r", encoding=encoding) as _f:
            res_json = json.load(_f)
        return res_json

    def destroy(self):
        os.remove(self.file_way)
