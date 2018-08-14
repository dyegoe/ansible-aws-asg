# Evidences

I created a CentOS EC2 instance on AWS to run this playbook

![01](https://i.imgur.com/tnWgDUD.png)

Install git

![02](https://i.imgur.com/0BMirMS.png)

Install Docker

![03](https://i.imgur.com/Z7HxVwv.png)

Start docker and enable to start. Trying to include the user centos as docker group member, but it doesn't exist.

![04](https://i.imgur.com/LRYOug5.png)

Trying to include on dockerroot group, but the sock doesn't belong to his group. It belongs to root. It isn't the fancy way to solve, but I included centos user as root member.

![05](https://i.imgur.com/84Qo6RL.png)

Clone the repository. Copy example file. Change vars.

![06](https://i.imgur.com/9SVVsNi.png)

Build the container to deploy the infrastructure.

![07](https://i.imgur.com/BqbcJYO.png)

Run the container, join in and run the playbook

![08](https://i.imgur.com/hhkbIRv.png)

Between 5 and 10 minutes. It is ready.

![09](https://i.imgur.com/c40VfQw.png)

Now it's time to login on console. Let's start from CloudFormation and their outputs
![10](https://i.imgur.com/dmfDtnD.png)

![11](https://i.imgur.com/ROSxcWp.png)

![12](https://i.imgur.com/SRLx8Ic.png)

![12](https://i.imgur.com/Q5aWe1j.png)

![13](https://i.imgur.com/7jPmysU.png)

EC2 Instances

![14](https://i.imgur.com/kce0BmD.png)

![15](https://i.imgur.com/hWxDsvO.png)

![16](https://i.imgur.com/xwdeSjx.png)

Auto Scaling Group

![17](https://i.imgur.com/FT93KGa.png)

Launch Configuration with userdata. This script run the container which was pushed to ECR.

![18](https://i.imgur.com/vNPTVXw.png)

Aplication Load Balancer

![19](https://i.imgur.com/EIRqo8v.png)

Listener default

![20](https://i.imgur.com/6Gzgxnj.png)

Target group with 3 healthy instances.

![21](https://i.imgur.com/JBygx48.png)

RDS DB Instance

![22](https://i.imgur.com/aPYL92W.png)

ECR Registry and repository

![23](https://i.imgur.com/WZK3l6x.png)

Subnets and VPC

![24](https://i.imgur.com/n1rzXmf.png)

SG for ALB - Allow 80 from any

![25](https://i.imgur.com/3iJQb18.png)

ASG EC2 SG - Allow SSH from any and 5000 only from ALB

![26](https://i.imgur.com/d0MPpvt.png)

RDS SG - Allow 3306 from ASG SG

![27](https://i.imgur.com/Jki8kJL.png)

Access the ALB url /users (URL that consume the database) and check if the hostnames match with the instances.

10.10.1.248 - Subnet a

![28](https://i.imgur.com/fRKthjE.png)

10.10.2.62 - Subnet B

![29](https://i.imgur.com/1MPzLD4.png)

10.10.3.216 - Subnet C

![30](https://i.imgur.com/4MIqryc.png)

SSH to the instance. Check container. Look docker-compose.yml. Install MySQL to attemp to connect on database.

![31](https://i.imgur.com/TkgWCc7.png)

Query on database returns the same data as the web url.

![32](https://i.imgur.com/2Y2OZ6h.png)

Logs from container start and the health checks request came from ALB.

![33](https://i.imgur.com/fJ1xKfc.png)

Start to remove the resources

![34](https://i.imgur.com/uL1TODB.png)

![35](https://i.imgur.com/jnryxc3.png)

![36](https://i.imgur.com/Sprbhfq.png)

![37](https://i.imgur.com/JJeVe9x.png)

![38](https://i.imgur.com/H2f8eFz.png)

![39](https://i.imgur.com/MglqUsG.png)

No more Subnets, VPC, Instances. Everything is gone.

![40](https://i.imgur.com/EBVcRjJ.png)