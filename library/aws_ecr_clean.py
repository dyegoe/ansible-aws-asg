#!/usr/bin/python
"""
    This python script work as an ansible module.
    It covers to remove all images before delete it.
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
module: aws_ecr_clean
short_description: Remove all images from ecr repository
author: Dyego Eugenio
email: dyegoe@gmail.com
'''

EXAMPLES = '''
- name: "Remove all images from ecr repository"
  aws_ecr_clean:
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        region: "{{ aws_region }}"
      register: result

    - debug:
        var: result
'''

from ansible.module_utils.basic import AnsibleModule
import boto3


def main():
    fields = {
        "aws_access_key": {"required": True, "type": "str"},
        "aws_secret_key": {"required": True, "type": "str"},
        "region": {"required": True, "type": "str"},
        "repository_name": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = ecr_clean(module.params)
    module.exit_json(changed=has_changed, meta=result)


def ecr_clean(data):
    client = boto3.client(
        'ecr',
        aws_access_key_id=data['aws_access_key'],
        aws_secret_access_key=data['aws_secret_key'],
        region_name=data['region']
    )

    list_images = client.list_images(
        repositoryName=data['repository_name'],
        maxResults=1000
    )

    response = client.batch_delete_image(
        repositoryName=data['repository_name'],
        imageIds=list_images['imageIds']
    )

    meta = {
        "imageIds": response['imageIds']
    }
    has_changed = False
    if len(meta['imageIds']) > 0:
        has_changed = True
    return has_changed, meta


if __name__ == '__main__':
    main()