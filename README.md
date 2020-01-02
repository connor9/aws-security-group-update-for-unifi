# AWS security groups auto-update for Unifi controller

This script detects changes in your external IP and uses AWS boto library 
to update the ports in a specific security group for your AWS controller.

# Setup

## AWS Security Group
Make sure that you have a single security group that contains all the port mappings 
needed. I.e.

```
{ 'protocol': 'udp', 'port': 10001 },
{ 'protocol': 'udp', 'port': 3478 },
{ 'protocol': 'tcp', 'port': 8080 },
{ 'protocol': 'tcp', 'port': 22 },
{ 'protocol': 'tcp', 'port': 8443 },
{ 'protocol': 'tcp', 'port': 6789 },
{ 'protocol': 'tcp', 'port': 8880 }    
```

The script relies on a single security group.

## Install requirements

You should generally setup a venv for this script but you can run it however you like.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Setup boto3 library

Once the requirements are installed you'll need to configure the boto3 library.
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

Basically you need to set up your programmatic access to your AWS account via an access/secret key
combo.

Follow AWS's advice.

## Create settings.json

Copy the settings.json.template to settings.json and update the security group ID and file path accordingly.

## Run

You can now run `python aws.py` and you should see it update your security group accordingly. 

 