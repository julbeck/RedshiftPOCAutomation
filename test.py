#!/usr/bin/env python3

import os

# from aws_cdk import core
# from redshift_poc_automation.stacks.vpc_stack import VpcStack
# from redshift_poc_automation.stacks.redshift_stack import RedshiftStack
# from redshift_poc_automation.stacks.glue_crawler_stack import GlueCrawlerStack
# from redshift_poc_automation.stacks.dms_stack import DmsStack


import json

# app = core.App()


config = json.load(open("user-config.json"))

vpc_id = config.get('vpc_id')
vpc_config = config.get('vpc')

redshift_endpoint = config.get('redshift_endpoint')
redshift_config = config.get('redshift')

glue_crawler_s3_target = config.get('glue_crawler_s3_target')
glue_crawler_s3_config = config.get('glue_crawler_s3')

# if glue_crawler_s3_target != "N/A":
#     glue_crawler = GlueCrawlerStack(
#         app,
#         f"{app.node.try_get_context('project')}-stack",
#         glue_crawler_s3_config=glue_crawler_s3_config,
#         stack_log_level="INFO",
#         description="Redshift POC Automation: Deploy Glue Crawler for S3 data lake"
#     )
#     redshift_demo.add_dependency(vpc_stack);

iam_role_arn = glue_crawler_s3_config.get('iam_role_arn')
database_name = glue_crawler_s3_config.get('database_name')
s3_locations = glue_crawler_s3_config.get('s3_locations')
s3_paths = []
for i in s3_locations:
    var = {"path": i}
    s3_paths.append(var)



# VPC Stack for hosting Secure API & Other resources
if vpc_id == "CREATE":
    vpc_stack = VpcStack(
        app,
        f"{app.node.try_get_context('project')}-vpc-stack",
        vpc_id=vpc_id,
        vpc_config=vpc_config,
        stack_log_level="INFO",
        description="Redshift POC Automation: Custom Multi-AZ VPC"
    )

if redshift_endpoint != "N/A":
    # Deploy Redshift cluster and load data"
    redshift_demo = RedshiftStack(
        app,
        f"{app.node.try_get_context('project')}-stack",
        vpc=vpc_stack,
        redshift_endpoint=redshift_endpoint,
        redshift_config=redshift_config,
        stack_log_level="INFO",
        description="Redshift POC Automation: Deploy Redshift cluster and load data"
    )
    redshift_demo.add_dependency(vpc_stack);




# DMS Stack for migrating database to redshift
# dms_stack = DmsStack(
#     app,
#     f"{app.node.try_get_context('project')}-dms-stack",
#     vpc=vpc_stack,
#     cluster=redshift_demo,
#     source_engine=source_engine,
#     source_db=source_db,
#     source_schema=source_schema,
#     source_host=source_host,
#     source_user=source_user,
#     source_pwd=source_pwd,
#     source_port=source_port,
#     migrationtype=migration_type,
#     stack_log_level="INFO",
#     description="Redshift POC Automation: Custom Multi-AZ VPC"
# )
#
# dms_stack.add_dependency(vpc_stack);
# dms_stack.add_dependency(redshift_demo);

# Stack Level Tagging
_tags_lst = app.node.try_get_context("tags")

if _tags_lst:
    for _t in _tags_lst:
        for k, v in _t.items():
            core.Tags.of(app).add(k, v, apply_to_launched_instances=True)


app.synth()
