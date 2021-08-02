
# AWS Redshift Infrastructure Automation

## Table of Contents

1. [Introduction](#overview-of-deployment)
1. [Prerequisites](#prerequisites)
1. [Deployment Steps](#deployment-steps)
	1. [Configuring the config file](#configuring-the-config-file)
	1. [Launcing the staging template](#launching-the-staging-template)
1. [Troubleshooting](#troubleshooting)

## Overview of Deployment

This project consists of a two-phase deployment: the staging infrastructure, and the target infrastructure. The target infrastructure is the end-goal configuration of AWS analytics services which are needed for a POC or other use case. The staging infrastructure will launch an EC2 instance to run a CDK application which will provision the resources of this target infrastructure. 

To achieve this, a JSON-formatted config file specifying the desired service configurations needs to be uploaded to an S3 bucket. The location of this file in S3 is used as a parameter in the CloudFormation stack, alongside further details of the staging infrastructure. Once the CloudFormation stack is launched, the resources are provisioned automatically.

Here you can see a diagram giving an overview of this flow:

![Architecture Flow](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Architecture_Flow.png)

The following sections give further details of how to complete these steps.

## Prerequisites


## Deployment-Steps

### Configuring the config file

### Launching the staging template

## Troubleshooting

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

