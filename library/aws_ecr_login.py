#!/usr/bin/python
# Reference: https://blog.toast38coza.me/custom-ansible-module-hello-world/

DOCUMENTATION = '''
---
module: aws_ecr_login
short_description: Get auth data from ecr
'''

EXAMPLES = '''
- name: Get auth data from ecr
  aws_ecr_login:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ aws_region }}"
      register: result

    - debug:
        var: result
'''

from ansible.module_utils.basic import *
import boto3
import base64
import re


def main():
    fields = {
        "aws_access_key": {"required": True, "type": "str"},
        "aws_secret_key": {"required": True, "type": "str"},
        "region": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = ecr_get_token(module.params)
    module.exit_json(changed=has_changed, meta=result)


def ecr_get_token(data):
    client = boto3.client(
        'ecr',
        aws_access_key_id=data['aws_access_key'],
        aws_secret_access_key=data['aws_secret_key'],
        region_name=data['region']
    )

    response = client.get_authorization_token()

    match = re.match(
        r'(.*):(.*)', base64.b64decode(response['authorizationData'][0]['authorizationToken'])
    )

    meta = {}
    if match:
        meta = {
            "username": match.group(1),
            "token": match.group(2),
            "endpoint": response['authorizationData'][0]['proxyEndpoint'],
            "expires_at": response['authorizationData'][0]['expiresAt']
        }

    has_changed = False
    return has_changed, meta


if __name__ == '__main__':
    main()
