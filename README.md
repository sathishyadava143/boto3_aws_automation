**AWS_AUTOMATION_USING_BOTO3**
******************************

Configuration AWS_CLI in WINDOWS or Linux

 LINUX_AWS_CLI_Configuration:
 ----------------------------

Ubunutu:
--------
$ snap install aws-cli --classic

RHEL and Other-Distribution:
----------------------------

$ curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
$ unzip awscli-bundle.zip
$ sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

Configure aws-cli:
------------------
$ aws configure

AWS Access Key ID : xxxxxxxxxxxxxxxxxxxxx
AWS Secret Access Key : xxxxxxxxxxxxxxxxxxxxxxx
Default region name : ap-south-1
Default output format : json

WINDOWS_AWS-CLI:
----------------

download aws-cli masi installer: https://s3.amazonaws.com/aws-cli/AWSCLI64PY3.msi

$ aws --version

without AWS-cli through pass a AWS Access Key ID and AWS Secret Access Key python script itself but its an risky way!.

ex: test.py

"""

import boto3
response=boto3.client('iam', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name="us-east-1") 

"""




