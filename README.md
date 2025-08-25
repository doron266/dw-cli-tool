# AWS CLI

**Automating AWS resource provisioning for development teams**

A Python CLI that allows developers to manage AWS resources (EC2, S3, Route53). 



## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Instructions](#instructions)
- [EC2 examples](#ec2-examples)
- [S3 examples](#s3-examples)
- [Route53 examples](#route53-examples)
- [General information](#general-information)

---

## Prerequisites
- Python 3.9
- pip
- poetry (pip package)
- AWS account with an IAM user/role that has permissions for EC2, S3 and Route53.
- AWS credentials configured locally

Configure AWS credentials:

```bash
aws configure # Enter credentials
```
## Compatiblity
Compatible with Windows 10 & Amazon Linux 2023


## General Information

All resources created by the CLI are tagged so the tool can safely operate on its own resources.

Tags:

- `CreatedBy=platform-cli`
- `Owner=<username>` (developer requesting the resource)


## Installation
```bash
# Clone this repo
git clone https://github.com/doron266/cli-tool.git

cd cli-tool/cli-tool

yum install pip

pip install poetry

poetry install

pip install --editable .

# View commands
awscli -h
```

---

## Instructions

The CLI format is as follows:

```bash
awscli <resource> <options> [command]
```

General pattern examples:

```bash
# create an EC2 instance
awscli ec2 --ami ubuntu --type t3.micro --key-name my-key create

# list instances
awscli ec2 list

# create a private s3 bucket
awscli s3 --name my-bucket create

# create a public s3 bucket (prompts for confirmation)
awscli s3 --name my-bucket --public create

# create a route53 zone
awscli route53 --name yourdomain.com create
```

Run `--help` on the top-level or any subcommand for more details:

```bash
awscli --help
awscli ec2 --help
awscli s3 --help
awscli route53 --help
```

---

## EC2 examples

**Create an EC2 instance**

```bash
awscli ec2 create \
  --ami ubuntu \
  --type t3.micro \
  --key-name my-ssh-key 
```

**Start an instance**

```bash
awscli ec2 -i i-0123456789abcdef0 start
```

**Stop an instance**

```bash
awscli ec2 -i i-0123456789abcdef0 stop
```


**List instances created by the CLI**

```bash
awscli ec2 list
```

---

## S3 examples

**Create a private bucket**

```bash
awscli s3 --name my-bucket create
```

**Create a public bucket (interactive confirmation required)**

```bash
awscli s3 --public create
# CLI will prompt: Are you sure? (yes/no)
```

**Upload a file to a CLI-created bucket**

```bash
awscli s3  -p path/to/file -n my-bucket -o myobjectname upload
```

**List CLI-created buckets**

```bash
awscli s3 list
```

> Upload and delete operations are allowed only for buckets the CLI created (scoped by tags).

---

## Route53 examples

**Create a hosted zone**

```bash
awscli route53 --name yourdomain.com create
```

**Create a record (only for CLI-created zones)**

```bash
awscli route53 -z my.zone -f dev.my.zone -t 192.0.0.8 --add manage
```

**Update a record**

```bash
awscli route53 -z my.zone -f dev.my.zone -t 192.0.0.8 --update manage
```

**Delete a record**

```bash
awscli route53 -z my.zone -f dev.my.zone -t 192.0.0.8 --delete manage

**List CLI-created zones & records**

```bash
awscli route53 list
```

---
