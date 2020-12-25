#!/bin/sh
hostname=$1
ip=`python3 pythontest.py $hostname`
if [ "$ip"  != "Host not found" ]; then
ssh -i ~/.ssh/aws-pem-key $ip -l ec2-user
else
  echo $ip
fi
