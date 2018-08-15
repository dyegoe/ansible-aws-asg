#!/usr/bin/python
"""
    This python script work as an ansible module.
    It writes a log file based on the input.
"""

__author__ = "Dyego Eugenio"
__copyright__ = "Copyleft with your own risk"
__credits__ = ["Dyego Eugenio"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Dyego Eugenio"
__email__ = "dyegoe@gmail.com"
__status__ = "Production"


DOCUMENTATION = '''
---
module: write_test_logs
short_description: Write log files
author: Dyego Eugenio
email: dyegoe@gmail.com
'''

EXAMPLES = '''
- name: "Write log file"
  write_test_logs:
        log_file: tests.log
        log_dir: /any/absolut/path/to/save/your/logs
        input: any_registered_var_from_previous_command
        type: database | docker | uri
        
'''

from ansible.module_utils.basic import AnsibleModule
from traceback import format_exc
import os.path


class WriteTestsLogs:
    def __init__(self):
        fields = {
            "log_file": {"required": True, "type": "str"},
            "log_dir": {"required": True, "type": "str"},
            "input": {"required": True, "type": "str"},
            "type": {
                "required": True,
                "choices": ['database', 'docker', 'uri'],
                "type": 'str'
            },
        }
        choice_map = {
            "database": self.__log_database,
            "docker": self.__log_docker,
            "uri": self.__log_uri
        }
        self.module = AnsibleModule(argument_spec=fields)
        has_changed, result = choice_map.get(self.module.params['type'])(self.module.params)
        self.module.exit_json(changed=has_changed, meta=result)

    def main(self):


    def __log_database(self, data):
        return False, 'not'


    def __log_docker(self, data):
        return False, 'not'


    def __log_uri(self, data):
        return False, 'not'


    def __write_file(self, log_dir, log_file, lines):
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            if not os.access(log_dir, os.W_OK):
                self.module.fail_json(msg="Source {0} not writable".format(log_dir))
        except Exception as __w_exc:
            self.module.fail_json(msg=str(__w_exc), exc=format_exc())
        try:
            with open("{0}{1}".format(log_dir, log_file), "a+") as __log:
                for line in lines:
                    __log.write(line)
        except Exception as __w_exc:
            self.module.fail_json(msg=str(__w_exc), exc=format_exc())


if __name__ == '__main__':
    write_test_logs = WriteTestsLogs
    write_test_logs.main()