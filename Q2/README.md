Assume that the current aws pem key is stored as ~/.ssh/aws-pem-key, by running command `./aws_ec2_ssh_connection.sh <EC2 name>`, ec2 instance can be login. `Host not found` will appear if the name cannot be found in the AWS account.
Also assume that `aws_secret_access_key` and `aws_secret_access_key` have been stored in ~/.aws/credentials already 

Below are required python packages
- sys
- boto3
- json
