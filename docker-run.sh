#!/bin/sh
docker run --name ansible-node-alb -v /home/dyego/PycharmProjects/ansible-node-alb:/home/dyego/ansible-node-alb -w /home/dyego/ansible-node-alb -u dyego -d ansible-node-alb:latest tail -f /dev/null