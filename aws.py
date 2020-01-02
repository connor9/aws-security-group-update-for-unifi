import boto3
from botocore.exceptions import ClientError
from requests import get
import json
import datetime

security_group_id = None
ip_filename = None
with open('settings.json') as f:
    settings = json.load(f)
    ip_filename = settings['ip_filename']
    security_group_id = settings['security_group_id']

print("AWS SG Sync\n")
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Get previous ip from file

process_changes = False

fr = open(ip_filename, "r")
pip = fr.read()
fr.close()

pip = pip.strip().lower()

# Current external IP

ip = get('https://api.ipify.org').text
ip = ip.strip().lower()

print("Previous IP: " + str(pip) + "\n")
print("Current IP: " + str(ip) + "\n")

# If IP addresses have changed, we'll need to update AWS security groups
if str(pip) != str(ip):
    print("Not same")
    process_changes = True

f = open(ip_filename, "w")
f.write(ip)
f.close()

if process_changes:
        
    ip = ip + '/' + '32'

    print('My public IP address is:', ip)

    ec2 = boto3.client('ec2')

    # Ports to open for Unifi
    required_rules = [
        { 'protocol': 'udp', 'port': 10001 },
        { 'protocol': 'udp', 'port': 3478 },
        { 'protocol': 'tcp', 'port': 8080 },
        { 'protocol': 'tcp', 'port': 22 },
        { 'protocol': 'tcp', 'port': 8443 },
        { 'protocol': 'tcp', 'port': 6789 },
        { 'protocol': 'tcp', 'port': 8880 }    
    ]

    print(required_rules)

    try:
        sg = ec2.describe_security_groups(GroupIds=[security_group_id])

        items = sg['SecurityGroups'][0]['IpPermissions']

        for item in items:

            fromPort = item['FromPort']
            cidrIp = item['IpRanges'][0]['CidrIp']
            protocol = item['IpProtocol']

            print("Remove", fromPort, cidrIp, protocol)

            data = ec2.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpProtocol=protocol, 
                CidrIp=cidrIp, 
                FromPort=fromPort, 
                ToPort=fromPort
            )

        for rule in required_rules:

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': rule['protocol'],
                    'FromPort': rule['port'],
                    'ToPort': rule['port'],
                    'IpRanges': [{'CidrIp': ip}]}
                ])

            print('Ingress Successfully Set %s' % data)

    except ClientError as e:
        print(e)
