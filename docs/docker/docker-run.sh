#!/bin/sh
docker run --name ansible-aws-asg -v /home/dyego/PycharmProjects/ansible-aws-asg:/home/dyego/ansible-aws-asg -w /home/dyego/ansible-aws-asg --privileged -d ansible-aws-asg:latest
