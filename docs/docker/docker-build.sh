#!/bin/bash
DIRECTORY=$(cd `dirname $0` && pwd)
PLAYBOOK_DIR=$(dirname $(dirname $DIRECTORY))
PROJECT_NAME=$(cat $PLAYBOOK_DIR/inventories/group_vars/all.yml | grep project_name | awk -F ": " '{print $2}')

#!/bin/bash
if [[ $EUID -eq 0 ]]; then
   echo "This script must be run as NON-Root user" 
   exit 1
fi

cd $DIRECTORY
sed -r 's?UID_REPLACE?'$UID'?' Dockerfile.template > Dockerfile
docker build -t $PROJECT_NAME:latest .
