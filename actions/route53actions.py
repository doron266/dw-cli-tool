import boto3
from datetime import datetime
from actions.consts import *

route53 = boto3.client('route53')
now = datetime.now()

def manage(fqdns, target, type_of_record, name, action):
    response = route53.list_hosted_zones_by_name(DNSName=name)
    host_zone_id = response['HostedZones'][0]['Id'].split('/')[-1]
    response = route53.change_resource_record_sets(
        HostedZoneId=host_zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': fqdns,
                        'Type': type_of_record,
                        'TTL': 300,
                        'ResourceRecords': [{'Value': target}]}}]})


def create(name):
    response = route53.create_hosted_zone(
        Name=name,
        CallerReference=str(now),
    )
    hot_zone_id = response['HostedZone']['Id'].split('/')[-1]
    response = route53.change_tags_for_resource(
        ResourceType='hostedzone',  # Can also be 'healthcheck'
        ResourceId=hot_zone_id,
        AddTags=[personal_tags, platform_tags]
    )
    return  response

def get_host_zone_id_from_arn(arn):
    return arn.split(":::")[-1].split("/")[-1]

def get_host_zones():
    tags = [personal_tags, platform_tags]
    filters = []
    hosted_zones = []
    for tag in tags:
        filters.append({"Key": f"{tag['Key']}", "Values": [tag["Value"]]})
    tag_client = boto3.client("resourcegroupstaggingapi")
    response = tag_client.get_resources(
        ResourceTypeFilters=["route53"],
        TagFilters=filters
    )
    for resource in response["ResourceTagMappingList"]:
        records = []
        arn = resource["ResourceARN"]
        host_zone_id = get_host_zone_id_from_arn(arn)
        host_zone_name = route53.get_hosted_zone(Id=host_zone_id)['HostedZone']['Name'].split('/')[-1]
        response = route53.list_resource_record_sets(
            HostedZoneId=host_zone_id,

        )
        for record in response['ResourceRecordSets']:
            record_name = record['Name']
            record_type = record['Type']
            record_target = record['ResourceRecords'][0]['Value']
            records.append({"Name": record_name, "Type": record_type, "Target": record_target})


        hosted_zones.append(
            {
                "name": host_zone_name,
                "records": records
            }
        )

    return hosted_zones