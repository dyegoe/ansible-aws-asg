#!/usr/bin/python
# Reference: https://blog.toast38coza.me/custom-ansible-module-hello-world/

from ansible.module_utils.basic import *
import boto3


def main():
    fields = {
        "aws_access_key": {"required": True, "type": "str"},
        "aws_secret_key": {"required": True, "type": "str"},
        "region": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)

    client = boto3.client(
        'ecr',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region=
    )

    response = client.get_authorization_token(registryIds=['891480698835'])

    # response = {"Token": "world"}
    module.exit_json(changed=False, meta=response)

if __name__ == '__main__':
    main()
