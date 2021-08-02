
# AWS Redshift Infrastructure Automation

## Table of Contents

1. [Introduction](#overview-of-deployment)
1. [Prerequisites](#prerequisites)
	1. [Launching a VPC](#launching-a-vpc)
	1. [Auto-assigning public IPv4 addresses](#auto-assigning-public-ipv4-addresses)
1. [Deployment Steps](#deployment-steps)
	1. [Configure the config file](#configure-the-config-file)
	1. [Launch the staging template](#launch-the-staging-template)
1. [Troubleshooting](#troubleshooting)

## Overview of Deployment

This project consists of a two-phase deployment: the staging infrastructure, and the target infrastructure. The target infrastructure is the end-goal configuration of AWS analytics services which are needed for a POC or other use case. The staging infrastructure will launch an EC2 instance to run a CDK application which will provision the resources of this target infrastructure. 

To achieve this, a JSON-formatted config file specifying the desired service configurations needs to be uploaded to an S3 bucket. The location of this file in S3 is used as a parameter in the CloudFormation stack, alongside further details of the staging infrastructure. Once the CloudFormation stack is launched, the resources are provisioned automatically.

Here you can see a diagram giving an overview of this flow:

![Architecture Flow](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Architecture_Flow.png)

The following sections give further details of how to complete these steps.

## Prerequisites

In order to run the staging stack, some resources need to be preconfigured:
* A VPC containing a public subnet that has IPv4 auto-assign enabled -- if either of these aren't configured please see [launching a VPC](#launching-a-vpc) and [auto-assigning public IPv4 addresses](#auto-assigning-public-ipv4-addresses) below
* If using DMS or SCT, opening source firewalls/ security groups to allow for traffic from AWS

If these are complete, continue to [deployment steps](#deployment-steps).

### Launching a VPC

An option for provisioning the VPC is to use the [VPC Launch Wizard console](https://console.aws.amazon.com/vpc/home?region=us-east-1#wizardSelector:) -- you can see the details of the infrastructure launched using this wizard [here](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario1.html)
1. Open the VPC Launch Wizard console linked above, change to desired region, and press **Select**
2. Configure your desired VPC size, VPC name, subnet size, and subnet name -- other values can be kept as default. Example:

	![Example](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Screen%20Shot%202021-08-02%20at%2017.36.05.png)

	2. Minimum VPC size: 
	2. Minimum subnet size:
3. Press **Create VPC**

### Auto-assigning public IPv4 addresses

To ensure instances launched in this subnet will be auto-assigned public IPv4 addresses, 
1. Navigate to the **Subnets** tab in the VPC console -- select the subnet you intend to use for your staging infrastructure, and under details, see whether the "Auto-assign public IPv4 address" value is Yes or No

	![Autoassign](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Screen%20Shot%202021-08-02%20at%2017.19.11.png)

2. If the value is No, select **Actions** > **Modify auto-assign IP settings**

	![Modify](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Screen%20Shot%202021-08-02%20at%2017.20.41.png)

	select the "Enable auto-assign public IPv4 address" checkbox

	![Checkbox](https://github.com/julbeck/RedshiftPOCAutomation/blob/master/Screen%20Shot%202021-08-02%20at%2017.22.36.png)
	
3. Press **Save**

## Deployment Steps

### Configure the config file

### Launch the staging template

## Troubleshooting

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

