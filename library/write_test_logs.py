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
import time
from traceback import format_exc
import os.path


class WriteTestsLogs:
    def __init__(self):
        fields = {
            "log_file": {"required": True, "type": "str"},
            "log_dir": {"required": True, "type": "str"},
            "input": {"required": True, "type": "dict"},
            "host": {"required": True, "type": "str"},
            "type": {
                "required": True,
                "choices": ['database', 'docker', 'uri'],
                "type": 'str'
            },
        }
        self.module = AnsibleModule(argument_spec=fields)
        self.log_dir = self.module.params['log_dir']
        self.log_file = self.module.params['log_file']
        self.input = self.module.params['input']
        self.host = self.module.params['host']

    def main(self):
        choice_map = {
            "database": self.__log_database,
            "docker": self.__log_docker,
            "uri": self.__log_uri
        }
        has_changed, result = choice_map.get(self.module.params['type'])()
        self.module.exit_json(changed=has_changed, meta=result)

    def __log_database(self):
        __lines = list()
        __lines.append("Hostname: {0}".format(self.host))
        if self.host == '127.0.0.1' or self.host == 'localhost':
            if self.input['failed']:
                __lines.append("Status: OK")
                __lines.append("CMD: {0}".format(self.input['cmd']))
                __lines.append("Output: {0}".format(self.input['stderr_lines'][1]))
                self.__write_file(__lines)
                return False, __lines
            else:
                return True, {"Test": True}

    @staticmethod
    def __log_docker(self):
        return False, {"Test": True}

    @staticmethod
    def __log_uri(self):
        return False, {"Test": True}

    def __write_file(self, __lines):
        try:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            if not os.access(self.log_dir, os.W_OK):
                self.module.fail_json(msg="Source {0} not writable".format(self.log_dir))
        except Exception as __w_exc:
            self.module.fail_json(msg=str(__w_exc), exc=format_exc())
        try:
            with open("{0}{1}".format(self.log_dir, self.log_file), "a+") as __log:
                for __line in __lines:
                    ts = time.gmtime()
                    __log.write("[{0}] {1}\n".format(
                        time.strftime("%Y-%m-%d %H:%M:%S", ts),
                        __line)
                    )
                __log.write("---------------------------------------------------------------------------------------\n")
                return True
        except Exception as __w_exc:
            self.module.fail_json(msg=str(__w_exc), exc=format_exc())
            return False


if __name__ == '__main__':
    write_test_logs = WriteTestsLogs()
    write_test_logs.main()
