# Ansible AWS Auto Scaling Group

An ansible playbook to deploy an infrastrucutre with these itens:

- AWS ECR
- AWS VPC
- AWS RDS
- AWS Auto Scaling Group
  - AWS EC2 Instances
  - AWS Application Load Balancer

## Premisses

I've tested this playbooks on aws account which has only an ECR endpoint. I was not tested using cross account ECR permissions. I can't guarantee that my module will work property if there are more than 1 endpoint.

You should use AWS as you cloud provider and you must provide the aws_access_key and aws_secret_key. This account must has the rights to create and delete the resources. You can find a policy example on `docs/aws/aws-policy.json`. This playbook doesn't cover the user creation.

## References

- https://docs.ansible.com/ansible/2.6/modules/docker_image_module.html
- https://docs.ansible.com/ansible/2.5/modules/docker_login_module.html
- https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
- https://docs.ansible.com/ansible/latest/modules/list_of_cloud_modules.html
- https://docs.ansible.com/ansible/2.6/modules/cloudformation_facts_module.html
- https://docs.ansible.com/ansible/2.5/modules/mysql_db_module.html
- https://docs.ansible.com/ansible/2.6/modules/wait_for_module.html
- https://awspolicygen.s3.amazonaws.com/policygen.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.- html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html
- https://boto3.readthedocs.io/en/latest/guide/configuration.html
- https://boto3.readthedocs.io/en/latest/reference/services/ecr.html
- https://blog.toast38coza.me/custom-ansible-module-hello-world/
- https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/RDS/RDS_with_DBParameterGroup.yaml