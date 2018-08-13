#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
PLAYBOOK_DIR=$(dirname $(dirname $DIRECTORY))
PROJECT_NAME=$(cat $PLAYBOOK_DIR/inventories/group_vars/all.yml | grep project_name | awk -F ": " '{print $2}')

cd $DIRECTORY
sed -r 's?UID_REPLACE?'$UID'?' Dockerfile.template > Dockerfile
docker build -t $PROJECT_NAME:latest .
