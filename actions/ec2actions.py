import boto3
import os
import logging
from actions.consts import *
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
owner = boto3.client('sts').get_caller_identity().get('Account')


def get_ec2_instances_by_tag():

    instance_running_count = 0

    tags = [personal_tags, platform_tags]
    filters = []
    for tag in tags:
        filters.append({"Name": f"tag:{tag['Key']}", "Values": [tag["Value"]]})

    response = ec2.describe_instances(Filters=filters)
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            state = instance['State']['Name']
            if state == 'running':
                instance_running_count += 1
            instance_data = {
                "InstanceId": instance["InstanceId"],
                "State": state,
                "Tags": {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
            }
            instances.append(instance_data)
    return [instances, instance_running_count]

def creating_key_pair(name):
    resp = ec2.create_key_pair(KeyName=name)
    file = open('keypair.pem','w')
    file.write(resp['KeyMaterial'])
    file_path = os.path.abspath('keypair.pem')
    return file_path


def ec2_create(instance_type, image_id,key_name ,security_groups):
    running_instances = get_ec2_instances_by_tag()[1]
    if running_instances >= maximum_running_instances:
        return f"Requested creation not qualified duo to maximum running instances reach({maximum_running_instances})"
    response = ec2_resource.create_instances(ImageId = image_id,
                                             MinCount = 1,
                                             MaxCount = 1,
                                             InstanceType = instance_type,
                                             KeyName=key_name,
                                             TagSpecifications=[{
                                                     'ResourceType': 'instance',
                                                     "Tags": [{"Key": "CreatedBy", "Value": "cli-platform"},
                                                              {"Key": "owner", "Value": user_name},]}],
                                             SecurityGroupIds=security_groups,
                                             SubnetId = default_subnet
                                             )
    return response


def ec2_manage(state, instance_id):
    if state:
        ec2.stop_instances(InstanceIds=[instance_id])
    else:
        ec2.start_instances(InstanceIds=[instance_id])
