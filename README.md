# Ansible AWS Auto Scaling Group

An ansible playbook to deploy an infrastrucutre with these itens:

- AWS ECR
- AWS VPC
- AWS RDS
- AWS Auto Scaling Group
  - AWS EC2 Instances
  - AWS Application Load Balancer

## Requirements

TODO:

## Limitations

During the development I discovered that is no way to send a base64 as parameter content, so I move from cloudformation file to a jinja template and it will replace the jinja var with a base64 file content to use as cloud-init script. I include on the cloudformation the `.aws/config` and `.aws/credentials` to be create on launch and on the same way a `docker-compose.yml` to launch the app on the boot.

## Premisses

I've tested this playbooks on aws account which has only an ECR endpoint. I was not tested using cross account ECR permissions. I can't guarantee that my module will work property if there are more than 1 endpoint.

You should use AWS as you cloud provider and you must provide the aws_access_key and aws_secret_key. This account must has the rights to create and delete the resources. You can find a policy example on `docs/aws/aws-policy.json`. This playbook doesn't cover the user creation.

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