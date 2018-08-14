#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
PLAYBOOK_DIR=$(dirname $(dirname $DIRECTORY))
PROJECT_NAME=$(cat $PLAYBOOK_DIR/group_vars/all.yml | grep project_name | awk -F ": " '{print $2}')

docker exec --privileged -u ansible -it $PROJECT_NAME bash