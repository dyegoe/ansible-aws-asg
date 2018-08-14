# Ansible AWS Auto Scaling Group

An ansible playbook to deploy an infrastrucutre with these itens:

- AWS ECR
- AWS VPC
- AWS RDS
- AWS Auto Scaling Group
  - AWS EC2 Instances
  - AWS Application Load Balancer

## Requirements

### AWS Account

This playbook was developed to run on aws, to execute it you must have an AWS account with at least the permission described on `docs/aws/aws-policy.json`. Use can create the user and attach the content as **Inline policy**. This account must has a **Programmatic access**. With the keys in hand, you should configure `inventories/group_vars/all.conf`.

### A linux machine

I could be your desktop, a vm or an ec2 instance. It should have **git** installed.

**OBS.:** This environment was tested using Ubuntu 18.04, 16.04 and CentOS 7

```text
sudo apt-get install git
or
yum install git
```

You will need **Docker** installed.

```text
sudo apt-get install docker.io
or
yum install docker
```

Now, if you want to run the playbook from you computer, you should install the packages described below. But if you want to use a Docker container solution to run you playbook, you can skip those packages. I will describe how to build and execute the container.

#### Ubuntu 18.04

```text
sudo apt-get install awscli ansible python-boto3 python-botocore python-docker python-mysqldb mysql-client
```

#### Ubuntu 16.04

```text
sudo apt install python-pip libmysqlclient-dev mysql-client
sudo pip install --upgrade pip
sudo pip install -r https://raw.githubusercontent.com/dyegoe/ansible-aws-asg/master/docs/python/requirements.txt
```

#### CentOS 7.x

*OBS* Run as root

```text
yum install -y python-boto3 python-docker MySQL-python mariadb-client mardiadb-libs-dev epel-release
yum install -y python-pip
pip install --upgrade pip
pip install -r https://raw.githubusercontent.com/dyegoe/ansible-aws-asg/master/docs/python/requirements.txt
systemctl start docker
systemctl enable docker
```

## How to use

As a **normal** user, run this commands.

```text
git clone https://github.com/dyegoe/ansible-aws-asg.git
cd ansible-aws-asg/
cp inventories/group_vars/example-all.yml inventories/group_vars/all.yml
vi inventories/group_vars/all.yml
```

At this point, you must provide `aws_access_key` and `aws_secret_key`. Also you should configure `aws_region` of your preference.

**!! Atention !!** During the tests, I figured out this playbook can only run on regions that has at least 3 avaibility zones, becouse the VPC Cloudformation has 3 subnets parameters and the avaibility zones are hard code on this CloudFormation

To property test this project, you should use this repository. Configure it.

```text
app_git_repo: https://github.com/dyegoe/python-rest.git
```

You can also, change the project_name, but only if you want. Likewise the other ones you can leave as default.

Your file should look like this.

```yaml
---
aws_access_key: include-your-access-key-here
aws_secret_key: include-your-secret-key-here
aws_region: eu-west-1
project_name: ubuntu1804
app_git_repo: https://github.com/dyegoe/python-rest.git
app_port: 5000
db_name: dbtest
db_user: root
db_password: change-your-password
db_instance_class: db.t2.micro
ec2_sshport: 22
ec2_image_name: amzn-ami-minimal-hvm-2018.03.0.20180622-x86_64-ebs
asg_max_size: 3
asg_start_size: 3
```

So, if you choose to run the playbook from docker, you can use the scripts located on `docs/docker/`.

```text
./docs/docker/docker-build.sh
./docs/docker/docker-run.sh
./docs/docker/docker-exec.sh
```

```text
ansible-playbook -i inventories/inventory.conf deploy_infrastructure.yml
```

## Limitations

During the development I discovered that is no way to send a base64 as parameter content, so I move from cloudformation file to a jinja template and it will replace the jinja var with a base64 file content to use as cloud-init script. I include on the cloudformation the `.aws/config` and `.aws/credentials` to be create on launch and on the same way a `docker-compose.yml` to launch the app on the boot.

As described before, you must avoid the regions that have less than 3 AZ.

*e.g.*

```text
"ap-south-1a", "ap-south-1b"
"ap-northeast-2a", "ap-northeast-2c"
"sa-east-1a", "sa-east-1c"
"ca-central-1a", "ca-central-1b"
"us-west-1a", "us-west-1c"
```

## Premisses

I've tested this playbooks on aws account which has only an ECR endpoint. I was not tested using cross account ECR permissions. I can't guarantee that my module will work property if there are more than 1 endpoint.

You should use AWS as you cloud provider and you must provide the aws_access_key and aws_secret_key. This account must has the rights to create and delete the resources. You can find a policy example on `docs/aws/aws-policy.json`. This playbook doesn't cover the user creation.

## To improve

Include avaibility zone on VPC CloudFormation to avoid the error when deploy it on regions that don't have avaibility zones `b`.

## References

- [Ansible Docker Image module](https://docs.ansible.com/ansible/2.6/modules/docker_image_module.html)
- [Ansible Docker Login module](https://docs.ansible.com/ansible/2.5/modules/docker_login_module.html)
- [Ansible Playbooks Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible List of cloud modules](https://docs.ansible.com/ansible/latest/modules/list_of_cloud_modules.html)
- [Ansible Cloudformation facts module](https://docs.ansible.com/ansible/2.6/modules/cloudformation_facts_module.html)
- [Ansible Mysql DB module](https://docs.ansible.com/ansible/2.5/modules/mysql_db_module.html)
- [Ansible Wait for module](https://docs.ansible.com/ansible/2.6/modules/wait_for_module.html)
- [Ansible Tempfile module](https://docs.ansible.com/ansible/2.5/modules/tempfile_module.html)
- [Ansible Lineinfile module](https://docs.ansible.com/ansible/2.5/modules/lineinfile_module.html)
- [AWS CloudFormation Policy Gen](https://awspolicygen.s3.amazonaws.com/policygen.html)
- [AWS CloudFormation RDS Properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html)
- [AWS CloudFormation ECR Repository](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html)
- [AWS CloudFormation EC2 Subnet Route Table Association](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html)
- [AWS CloudFormation EC2 Route Table](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html)
- [AWS CloudFormation EC2 Subnet](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html)
- [AWS CloudFormation Auto Scaling Group properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html)
- [AWS CloudFormation Application Load Balancer](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html)
- [AWS CloudFormation IAM Policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html)
- [AWS CloudFormation IAM Role](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html)
- [AWS CloudFormation IAM Instance Profile](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html)
- [AWS CloudFormation EC2 Security Group](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html)
- [AWS CloudFormation Internet Gateway](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html)
- [AWS CloudFormation EC2 Route](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html)
- [AWS CloudFormation EC2 VPC](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html)
- [AWS CloudFormation Parameter Section Structure](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
- [Boto3 Configuration](https://boto3.readthedocs.io/en/latest/guide/configuration.html)
- [Boto3 ECR](https://boto3.readthedocs.io/en/latest/reference/services/ecr.html)
- [Docker Compose](https://docs.docker.com/compose/compose-file/)
- [Buil a custom ansible module](https://blog.toast38coza.me/custom-ansible-module-hello-world/)
- [RDS DBParameterGroup](https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/RDS/RDS_with_DBParameterGroup.yaml)
- [Use Ansible base64 encode](https://stackoverflow.com/questions/22978319/how-to-use-ansible-b64encode?rq=1)
- [Evaluate null ansible vars](https://github.com/ansible/ansible/issues/37441)