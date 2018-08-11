FROM ubuntu:18.04

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt update -y && \
    apt upgrade -y && \
    apt install -yq git ansible python-boto3 python-botocore docker.io && \
    useradd -m -u 1000 dyego -G docker

CMD [ "dockerd" ]