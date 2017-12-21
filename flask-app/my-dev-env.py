import boto3
import botocore
from requests import get


INSTANCE_ID = 'i-00e55757287dd8cd1'
SG = 'sg-03bb5565'
MY_PUB_IP = get('http://ip.42.pl/raw').text
ec2 = boto3.client('ec2')

# ec2_r = boto3.resource('ec2')
# sg = ec2_r.SecurityGroup(SG)

res = ec2.describe_instances()['Reservations']

print('My Public IP', MY_PUB_IP)


def print_instance_details():
    for r in res:
        for i in r['Instances']:
            print(i['InstanceId'], i['InstanceType'], i['PublicDnsName'], i['State']['Name'], i['Tags'])
            # print(i)


def start_instance():
    try:
        waiter = ec2.get_waiter('instance_running')
        data = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
        print(data)
    except botocore.exceptions.ClientError as e:
        print(e)
        if 'would have succeeded' in str(e):
            data = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
            waiter.wait(InstanceIds=[INSTANCE_ID])
            print(data)


def stop_instance():
    waiter = ec2.get_waiter('instance_stopped')
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    waiter.wait(InstanceIds=[INSTANCE_ID])


def reset_ingress():
    try:
        data = ec2.describe_security_groups(GroupIds=[SG])

        ec2.revoke_security_group_ingress(
            GroupId=SG, IpPermissions=data['SecurityGroups'][0]['IpPermissions']
        )

        # print(ec2.describe_security_groups(GroupIds=[SG]))

        # add my ip to security groups
        permissions = {
            'FromPort': 0,
            'ToPort': 65535,
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': MY_PUB_IP + '/32'
                }
            ]}

        data = ec2.authorize_security_group_ingress(
            GroupId=SG, IpPermissions=[permissions]
        )

        print('Ingress successfully set {}'.format(data))

        # print(ec2.describe_security_groups(GroupIds=[SG]))

    except botocore.exceptions.ClientError as e:
        print(e)



# reset_ingress()
# start_instance()
# stop_instance()
print_instance_details()

# print(ec2.describe_instance_status())




