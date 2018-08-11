FROM docker:dind

RUN apk --update upgrade && \
    apk --update add git \
                     python \
                     py-pip \
                     openssl \
                     ca-certificates \
                     openssh-client \
                     bash \
                     bash-completion && \
    apk --update add --virtual build-dependencies \
                               python-dev \
                               libffi-dev \
                               openssl-dev \
                               build-base && \
    pip install --upgrade pip cffi && \
    pip install 'ansible>=2.5.0,<2.6.0' \
                'docker-py' \
                'boto3' \
                'botocore' \
                'awscli' && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/*

COPY source /tmp/source

RUN adduser -D -u 1000 -h /home/ansible -s /bin/bash ansible && \
    cp /tmp/source/.bashrc /home/ansible/.bashrc && \
    chown -R ansible:ansible /home/ansible/.bashrc && \
    mv /tmp/source/.bashrc /root/.bashrc && \
    chown -R root:root /root/.bashrc && \
    sed -i 's?/bin/ash?/bin/bash?' /etc/passwd && \
    sed -i 's?root:x:0:root?root:x:0:root,ansible?' /etc/group && \
    mkdir /etc/bash_completion.d/ && \
    mv /tmp/source/docker /etc/bash_completion.d/docker && \
    echo "complete -C '/usr/bin/aws_completer' aws" > /etc/bash_completion.d/aws && \
    rm -rf /tmp/source