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

This playbook was developed to run on aws, to execute it you must have an AWS account with at least the permission described on `docs/aws/aws-policy.json`. Use can create the user and attach the content as **Inline policy**. This account must has a **Programmatic access**. With the keys in hand, you should configure `group_vars/all.conf`.

### A linux machine

I could be your desktop, a vm or an ec2 instance. It should have **git** installed.

**OBS.:** This environment was tested using Ubuntu 18.04, 16.04 and CentOS 7

```text
ubuntu@ip-172-31-25-18:~$ sudo apt-get update -y
ubuntu@ip-172-31-25-18:~$ sudo apt-get install -y git
or
[root@ip-172-31-22-97 ~]# yum update -y
[root@ip-172-31-22-97 ~]# yum install -y git
```

You will need **Docker** installed.

```text
ubuntu@ip-172-31-25-18:~$ sudo apt-get install -y docker.io
ubuntu@ip-172-31-25-18:~$ sudo usermod -G docker ubuntu
ubuntu@ip-172-31-25-18:~$ logout
or
[root@ip-172-31-22-97 ~]# yum install -y docker
[root@ip-172-31-22-97 ~]# systemctl start docker
[root@ip-172-31-22-97 ~]# systemctl enable docker
[root@ip-172-31-22-97 ~]# usermod -G root centos
[root@ip-172-31-22-97 ~]# logout
[centos@ip-172-31-22-97 ~]$ logout
```

And connect again!

Now, if you want to run the playbook from you computer, you should install the packages described below. But if you want to use a Docker container solution to run your playbook, you can skip those packages. I will describe how to build and execute the container.

Actually, any other distribution should work using container, as you have installed Docker and run the scripts to build as a non-root user.

#### Ubuntu 18.04

```text
ubuntu@ip-172-31-25-18:~$ sudo apt-get -y install awscli ansible python-boto python-boto3 python-botocore python-docker python-mysqldb mysql-client
```

#### Ubuntu 16.04

```text
ubuntu@ip-172-31-25-18:~$ sudo apt-get install -y python-pip libmysqlclient-dev mysql-client
ubuntu@ip-172-31-25-18:~$ sudo pip install --upgrade pip
ubuntu@ip-172-31-25-18:~$ sudo pip install -r https://raw.githubusercontent.com/dyegoe/ansible-aws-asg/master/docs/python/requirements.txt
```

If you have some issue with locale as I had.

```text
ubuntu@ip-172-31-25-18:~$ export LC_ALL="en_US.UTF-8"
ubuntu@ip-172-31-25-18:~$ export LC_CTYPE="en_US.UTF-8"
```

#### CentOS 7.x

```text
[root@ip-172-31-22-97 ~]# yum install -y python-boto3 python-docker MySQL-python mariadb mariadb-devel epel-release
[root@ip-172-31-22-97 ~]# yum install -y python-pip
[root@ip-172-31-22-97 ~]# pip install --upgrade pip
[root@ip-172-31-22-97 ~]# pip install -r https://raw.githubusercontent.com/dyegoe/ansible-aws-asg/master/docs/python/requirements.txt
```

## How to use

As a **Non-Root** user, run this commands. This user should be able to perform **Docker** commands.

```text
ubuntu@ip-172-31-25-18:~$ git clone https://github.com/dyegoe/ansible-aws-asg.git
Cloning into 'ansible-aws-asg'...
remote: Counting objects: 742, done.
remote: Compressing objects: 100% (24/24), done.
remote: Total 742 (delta 9), reused 17 (delta 4), pack-reused 708
Receiving objects: 100% (742/742), 108.75 KiB | 0 bytes/s, done.
Resolving deltas: 100% (311/311), done.
Checking connectivity... done.
ubuntu@ip-172-31-25-18:~$ cd ansible-aws-asg/
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ cp group_vars/example-all.yml group_vars/all.yml
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ vi group_vars/all.yml
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

### Using the container to run the playbook

So, if you choose to run the playbook from docker, you can use the scripts located on `docs/docker/`. **Remember** Use a Non-Root user with Docker access.

```text
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ ./docs/docker/docker-build.sh
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ ./docs/docker/docker-run.sh
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ ./docs/docker/docker-exec.sh
```

After the last script, you will enter on the container on the work directory, where you can find the playbooks.

```text
...
...
Removing intermediate container 6efc6287796d
Step 4/4 : RUN adduser -D -u 1000 -h /home/ansible -s /bin/bash ansible &&     cp /tmp/source/.bashrc /home/ansible/.bashrc &&     chown -R ansible:ansible /home/ansible/.bashrc &&     mv /tmp/source/.bashrc /root/.bashrc &&     chown -R root:root /root/.bashrc &&     sed -i 's?/bin/ash?/bin/bash?' /etc/passwd &&     sed -i 's?root:x:0:root?root:x:0:root,ansible?' /etc/group &&     mkdir /etc/bash_completion.d/ &&     mv /tmp/source/docker /etc/bash_completion.d/docker &&     echo "complete -C '/usr/bin/aws_completer' aws" > /etc/bash_completion.d/aws &&     rm -rf /tmp/source
 ---> Running in 0a77eeddb05e
 ---> 33b2c79c1a20
Removing intermediate container 0a77eeddb05e
Successfully built 33b2c79c1a20
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ ./docs/docker/docker-run.sh
9ecca99b962e637e727394fb2dd9b450deec9be8910a1653d7da17c1ccc5a179
ubuntu@ip-172-31-25-18:~/ansible-aws-asg$ ./docs/docker/docker-exec.sh
ansible@9ecca99b962e:ansible-aws-asg $ ls -lah
total 68
drwxrwxr-x   11 ansible  ansible     4.0K Aug 14 01:40 .
drwxr-sr-x    1 ansible  ansible     4.0K Aug 13 21:39 ..
drwxrwxr-x    8 ansible  ansible     4.0K Aug 14 01:36 .git
-rw-rw-r--    1 ansible  ansible       44 Aug 11 17:24 .gitignore
drwxrwxr-x    3 ansible  ansible     4.0K Aug 12 13:28 .idea
drwxrwxr-x    2 ansible  ansible     4.0K Aug 11 23:21 .vscode
-rw-rw-r--    1 ansible  ansible     8.5K Aug 14 01:16 README.md
drwxr-xr-x    3 ansible  ansible     4.0K Aug 11 18:06 build
-rw-rw-r--    1 ansible  ansible      130 Aug 13 16:31 deploy_infrastructure.yml
drwxrwxr-x    6 ansible  ansible     4.0K Aug 13 23:10 docs
drwxr-xr-x    2 ansible  ansible     4.0K Aug 13 16:17 files
drwxrwxr-x    3 ansible  ansible     4.0K Aug  7 21:08 inventories
drwxrwxr-x    2 ansible  ansible     4.0K Aug 12 13:25 library
-rw-rw-r--    1 ansible  ansible      114 Aug 14 01:04 remove_infrastructure.yml
drwxrwxr-x   13 ansible  ansible     4.0K Aug 13 16:30 roles
ansible@9ecca99b962e:ansible-aws-asg $
```

### To deploy

```text
ansible@9ecca99b962e:ansible-aws-asg $ ansible-playbook -i inventories/localhost.conf deploy_infrastructure.yml

PLAY [all] ******************************************************************************************

TASK [Gathering Facts] ******************************************************************************
ok: [localhost]

TASK [deploy_ecr : Set ECR stack name] **************************************************************
ok: [localhost]

... the playbook continue

```

### To test

You should wait your infrastructure get ready and than you can run the playbook.

```text
ansible@9ecca99b962e:ansible-aws-asg $ ansible-playbook -i inventories/ec2.py test_infrastructure.yml

PLAY [localhost] ************************************************************************************

TASK [Gathering Facts] ******************************************************************************
ok: [localhost]

TASK [test_env_localhost : include_vars] ************************************************************
ok: [localhost]

TASK [test_env_localhost : "Try to access the RDS directly from this machine using internet."
"It should >>fail<<, as the playbook create a SG that doesn't allow it."] ***************************
fatal: [localhost]: FAILED! => {"changed": true, "cmd": "mysql -uroot -pui3krOCaPIsBnmnw -h test1-rds1.cl05xge8lnbu.eu-west-1.rds.amazonaws.com dbtest --connect-timeout=10 -B -e 'SELECT * FROM users;'", "delta": "0:00:10.049307", "end": "2018-08-16 21:35:24.656049", "msg": "non-zero return code", "rc": 1, "start": "2018-08-16 21:35:14.606742", "stderr": "mysql: [Warning] Using a password on the command line interface can be insecure.\nERROR 2003 (HY000): Can't connect to MySQL server on 'test1-rds1.cl05xge8lnbu.eu-west-1.rds.amazonaws.com' (110)", "stderr_lines": ["mysql: [Warning] Using a password on the command line interface can be insecure.", "ERROR 2003 (HY000): Can't connect to MySQL server on 'test1-rds1.cl05xge8lnbu.eu-west-1.rds.amazonaws.com' (110)"], "stdout": "", "stdout_lines": []}
...ignoring

TASK [test_env_localhost : Write test logs] *********************************************************
ok: [localhost]

... the playbook continue

```

This playbook will return some expected errors, that is because it tries to connect where is not possible as the playbook close the ports on the security groups.

After it finishes, you can check the logs `logs/tests_result.log` (default directory or any other that you had configure on all.yml)

### To remove

```text
ansible@9ecca99b962e:ansible-aws-asg $ ansible-playbook -i inventories/localhost.conf remove_infrastructure.yml
```

## Deep view of this playbook

I developed an ansible module to get ecr token to use as login on Docker to push image. I found solutions on internet using shell (inside ansible role) but I like the approach to have a solution inside the playbook. You can find on `library/`. There are also on module to clean up ECR before delete, because if it is not empty, it will block the ECR delete.

Inside `docs/docker` I created some shell scripts and a Dockerfile to cover knowledge on these topics.

You can find the dump file inside `docs/sql`.

The `requirements.txt` for `pip` is on `docs/python`.

Some roles I splited tasks more than just `main.yml` to use it again, as when I call the `deploy_rds/tasks/rds-sg.yml` from `deploy_asg/tasks/main.yml`. I'm using it because in the first time, the RDS is open to the world. After the creation of ASG (also EC2 instances), I update the cloudformation to restrict the access to 3306 just from EC2.

I choose to develop a Rest api using pyhton and it consumes from RDS/MariaDB. The traffic is balanced using ALB.

## Limitations

### Cloudformation doesn't accept base64 as parameter value

During the development I discovered that is no way to send a base64 as parameter content, so I move from cloudformation file to a jinja template and it will replace the jinja var with a base64 file content to use as cloud-init script. I include on the cloudformation the `.aws/config` and `.aws/credentials` to be create on launch and on the same way a `docker-compose.yml` to launch the app on the boot

### Regions with less than 3 AZ

As described before, you must avoid the regions that have less than 3 AZ.

*e.g.*

```text
"ap-south-1a", "ap-south-1b"
"ap-northeast-2a", "ap-northeast-2c"
"sa-east-1a", "sa-east-1c"
"ca-central-1a", "ca-central-1b"
"us-west-1a", "us-west-1c"
```

### Key_pair issue

If you try to deploy again the same project name, in a new git clone directory, when the playbook deploy the key_pair it didn't create the private key value because aws only provides it when you generate on the first time. Without the private key on the new directory, you cannot proceed with the tests.

## Premisses

I've tested this playbooks on aws account which has only an ECR endpoint. I was not tested using cross account ECR permissions. I can't guarantee that my module will work property if there are more than 1 endpoint.

You should use AWS as you cloud provider and you must provide the aws_access_key and aws_secret_key. This account must has the rights to create and delete the resources. You can find a policy example on `docs/aws/aws-policy.json`. This playbook doesn't cover the user creation.

## To improve

- Include avaibility zone on VPC CloudFormation to avoid the error when deploy it on regions that don't have avaibility zones `b`.
- Implement tests inside python modules, as: Check paths, return error if cannot connect, etc.
- Find a way to access the ansible vars from python module.

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
- [Ansible Working with Dynamic Inventory](https://docs.ansible.com/ansible/2.5/user_guide/intro_dynamic_inventory.html#example-aws-ec2-external-inventory-script)
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
- [SSH Key for Dynamic Inventory](https://stackoverflow.com/questions/33795607/how-to-define-ssh-private-key-for-servers-fetched-by-dynamic-inventory-in-files)