#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
PLAYBOOK_DIR=$(dirname $(dirname $DIRECTORY))
PROJECT_NAME=$(cat $PLAYBOOK_DIR/inventories/group_vars/all.yml | grep project_name | awk -F ": " '{print $2}')

docker stop $PROJECT_NAME
docker rm $PROJECT_NAME
docker rmi $PROJECT_NAME:latest
