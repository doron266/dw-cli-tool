import boto3
import os
from actions.consts import *
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
owner = boto3.client('sts').get_caller_identity().get('Account')

def is_cli_created(bucket_name, key, value):
    try:
        tagging = s3.get_bucket_tagging(Bucket=bucket_name)
        tags = {t["Key"]: t["Value"] for t in tagging["TagSet"]}
        return tags.get(key) == value
    except ClientError as e:
        return str(e)

def creat_s3_bucket(name, owner, public):
    try:
        s3.create_bucket(Bucket=name)
        s3.put_bucket_tagging(
            Bucket=name,
            Tagging={
                'TagSet': [personal_tags, platform_tags]})
        if public:
            s3.delete_public_access_block(Bucket=name, ExpectedBucketOwner=owner)
        return f'Bucket {name} created.'
    except ClientError as e:
        return f"Error creating S3 bucket {name}: {e}"


def get_bucket_name_from_arn(arn):
    return arn.split(":::")[-1]

def get_buckets_with_tags():
    tags = [personal_tags, platform_tags]
    filters = []
    for tag in tags:
        filters.append({"Key": f"{tag['Key']}", "Values": [tag["Value"]]})
    tag_client = boto3.client("resourcegroupstaggingapi")
    response = tag_client.get_resources(
        ResourceTypeFilters=["s3"],
        TagFilters= filters
    )

    buckets = []
    for resource in response["ResourceTagMappingList"]:
        arn = resource["ResourceARN"]
        bucket_name = get_bucket_name_from_arn(arn)

        bucket_object = s3_resource.Bucket(bucket_name)
        bucket_creation_date = bucket_object.creation_date

        buckets.append(
            {
                "name": bucket_name,
                "creation_date": bucket_creation_date,
            }
        )
    return buckets

def upload_file(file_path, bucket, object_name):
    try:
        valid_bucket = is_cli_created(bucket, platform_tags['Key'], platform_tags['Value'])
        if file_path and isinstance(valid_bucket, bool) and valid_bucket:
            if object_name == '':
                object_name = os.path.basename(file_path)
            s3_client = boto3.client('s3')
            s3_client.upload_file(file_path, bucket, object_name)
            return f"Uploaded {object_name} to {bucket}"
        else:
            return f"Error uploading {object_name} to {bucket} bucket: {valid_bucket}"
    except FileNotFoundError as e:
        return f"Error uploading {object_name} to {bucket} bucket: {e}"



def download_file():
    pass

def delete_s3_bucket():
    pass