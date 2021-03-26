#!/usr/bin/env python3

import os

from aws_cdk import core

from redshift_poc_automation.stacks.vpc_stack import VpcStack
from redshift_poc_automation.redshift_poc_automation_stack import RedshiftPocAutomationStack
from redshift_poc_automation.stacks.dms_stack import DmsStack
from inputs import *

#account_info = "320963489128"
#region_info = "us-east-1"
#source_engine = "sqlserver"
#source_db = "dms_sample"
#source_host = "ec2-3-86-250-37.compute-1.amazonaws.com"
#source_user = "awssct"
#source_pwd = "Password1"
#source_port = 1433
#migration_type = "full-load" 

app = core.App()

# VPC Stack for hosting Secure API & Other resources
vpc_stack = VpcStack(
    app,
    f"{app.node.try_get_context('project')}-vpc-stack",
    from_vpc_id="vpc-0dcdbbb111a70d3b9",
    stack_log_level="INFO",
    description="Redshift POC Automation: Custom Multi-AZ VPC",
    env=core.Environment(account=account_info, region=region_info)
)


# Deploy Redshift cluster and load data"

redshift_demo = RedshiftPocAutomationStack(
    app,
    f"{app.node.try_get_context('project')}-stack",
    vpc=vpc_stack,
    ec2_instance_type="dc2.large",
    numberofnodes=1,
    stack_log_level="INFO",
    description="Redshift POC Automation: Deploy Redshift cluster and load data"
)

redshift_demo.add_dependency(vpc_stack);

# DMS Stack for migrating database to redshift 
dms_stack = DmsStack(
    app,
    f"{app.node.try_get_context('project')}-dms-stack",
    vpc=vpc_stack,
    cluster=redshift_demo,
    source_engine=source_engine,
    source_db=source_db,
    source_host=source_host,
    source_user=source_user,
    source_pwd=source_pwd,
    source_port=source_port,
    migrationtype=migration_type,
    stack_log_level="INFO",
    description="Redshift POC Automation: Custom Multi-AZ VPC"
)

dms_stack.add_dependency(vpc_stack);
dms_stack.add_dependency(redshift_demo);

# Stack Level Tagging
_tags_lst = app.node.try_get_context("tags")

if _tags_lst:
    for _t in _tags_lst:
        for k, v in _t.items():
            core.Tags.of(app).add(k, v, apply_to_launched_instances=True)


app.synth()
