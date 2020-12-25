import sys
import boto3
import json

ec2name = sys.argv[1]
ec2 = boto3.client('ec2')

# Find the IP of the target ec2 instance
response = ec2.describe_instances(Filters=[{'Name' : 'tag:Name','Values' : [ec2name]}])
if not 'Reservations' in response or len(response['Reservations']) == 0:
  print('Host not found')
else:
  for r in response['Reservations']:
    for i in r['Instances']:
        for b in i['NetworkInterfaces']:
            ip = b['Association']['PublicIp']
            print(ip)

