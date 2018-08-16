#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
PLAYBOOK_DIR=$(dirname $(dirname $DIRECTORY))
PROJECT_NAME=$(cat $PLAYBOOK_DIR/group_vars/all.yml | grep project_name | awk -F ": " '{print $2}')

docker run --name $PROJECT_NAME -v ${PLAYBOOK_DIR}:/home/ansible/${PLAYBOOK_DIR##*/} -w /home/ansible/${PLAYBOOK_DIR##*/} --privileged -d $PROJECT_NAME:latest
