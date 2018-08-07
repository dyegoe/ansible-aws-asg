FROM ubuntu:latest

RUN useradd -u 1000 dyego && \
    apt update -y && \
    apt upgrade -y && \
    apt install -yq ansbile python-boto3 python-botocore

CMD [ "ansible", "--version" ]