FROM ubuntu:18.04

RUN useradd -m -u 1000 dyego && \
    apt update -y && \
    apt upgrade -y && \
    apt install -yq ansible python-boto3 python-botocore

CMD [ "ansible", "--version" ]