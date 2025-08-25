import click
import random
import boto3
from actions import s3actions
from actions import ec2actions
from actions import route53actions
from actions.consts import *

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
owner = boto3.client('sts').get_caller_identity().get('Account')

@click.command()
@click.argument('command')
@click.option('-n', '--name', default='', help="Name of object")
@click.option('--public', is_flag=True, default=False, help="To enable public access")
@click.option('-p', '--path', default='', help="Path to object")
@click.option('-o','--object_name', default='', help="name of new s3 object")
def s3(command, name, public, path, object_name):
    if command == 'create':
        if public:
            value = click.prompt('You choose public, are you sure Y/n?', default='y', type=str)
            if value == 'y':
                click.echo(s3actions.creat_s3_bucket(name, owner, public))
            else:
                click.echo('creation canceled')
        #click.echo(f"bucket {name} created successfully")
        else:
            s3actions.creat_s3_bucket(name, owner, public)
    elif command == 'list':
        click.echo(s3actions.get_buckets_with_tags())
    elif command == 'upload':
        click.echo(s3actions.upload_file(path, name, object_name))
    else:
        click.echo(f"Unknown command: {command}, try again with --help")

@click.command()
@click.argument('command')
@click.option('-t', '--instance_type',
              default=default_ec2_type,
              help="Type of ec2; takes t2.small or t3.micro, t2.small is the default")
@click.option('-a', '--ami', default=linux, help="AMI to use; default=linux; only(linux | ubuntu)")
@click.option('-k','--keypair', default=default_key, help="To generate a keypair")
@click.option('-i','--instance_id', default='', help="To give specific instance for actions")
@click.option('-s', '--security_group', default=default_security_group, help="Security group to use")
def ec2(command, instance_type, ami, keypair,  instance_id, security_group):
    if command == 'create':
        security_group = [security_group]
        click.echo(ec2actions.ec2_create(instance_type, ami, keypair, security_group))
        pass
    elif command == 'list':
        click.echo(ec2actions.get_ec2_instances_by_tag()[0])
    elif command in ['stop', 'start']:
        click.echo(command)
        if instance_id:

            ec2actions.ec2_manage(command, instance_id)
    else:
        click.echo(f"Unknown command: {command}, try again with --help")

@click.command()
@click.argument('command')
@click.option('-z', '--z_name', default='', help="Name of new host zone to create or hot zone for new record")
@click.option('-f', '--fqdns', default='', help="full qualified domain name of new or updated record")
@click.option('-type', '--type_of_record', default='A', help="Type of new record to add")
@click.option('-t', '--target', default='', help="Target of new record to add")
@click.option('--delete', is_flag=True, default=False, help="Use for delete a record")
@click.option('--add', is_flag=True, default=False, help="Use for add a record")
@click.option('--update', is_flag=True, default=False, help="Use for update a record")
def route53(command, z_name, fqdns, target: str, type_of_record, add, delete, update):
    if command == 'create':
        route53actions.create(z_name)
        click.echo(f"route53 created for {z_name}")
        pass
    elif command == 'manage':
        if add:
            route53actions.manage(fqdns, target, type_of_record, z_name, 'CREATE')
            click.echo(f"route53 managed for {z_name}, record added -- {fqdns}")
        elif delete:
            route53actions.manage(fqdns, target, type_of_record, z_name, 'DELETE')
            click.echo(f"route53 managed for {z_name}, record deleted -- {fqdns}")
        elif update:
            route53actions.manage(fqdns, target, type_of_record, z_name, 'UPDATE')
            click.echo(f"route53 managed for {z_name}, record updated -- {fqdns}")
        else:
            click.echo(f"No changes were made, no valid option mentioned(--add, --delete, --update)")
    elif command == 'list':
        click.echo(route53actions.get_host_zones())
    else:
        click.echo(f"Unknown command: {command}, try again with --help")

@click.command()
@click.option('-n', '--name', prompt="Please enter the name of the new keypair", help="Name of new keypair")
def keypair(name):
    if name:
        click.echo(ec2actions.creating_key_pair(name))
    else:
        click.echo('key name cannot be empty')