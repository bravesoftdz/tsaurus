
# docker api sdk was a pain to use. decided to go with REST API client instead
#import docker
#client = docker.Client(base_url='tcp://ec2-13-55-34-231.ap-southeast-2.compute.amazonaws.com:4243')


# AWS commander snippets
import boto3

ec2client = boto3.client('ec2')

regions = ec2client.describe_regions()

def list_all_instances():
    for region in regions['Regions']:
        region_name = region['RegionName']
        ec2resource = boto3.resource('ec2', region_name=region_name)
        instances = ec2resource.instances.filter()

        for i in instances:
            print(i.id, i.public_ip_address, i.tags, i.placement['AvailabilityZone'], i.state, i.state_reason,
                      i.subnet_id)

# list_all_instances()


# --------------------
# Docker API client

import docker

client = docker.DockerClient(base_url='http://ec2-13-55-34-231.ap-southeast-2.compute.amazonaws.com:4243')

containers = client.containers.list(all=True)

for c in containers:
    print(c.short_id, c.name, c.status)


def delete_all_containers()



