#!/usr/bin/env python3

from aws_cdk import core

from redshift_poc_automation.redshift_poc_automation_stack import RedshiftPocAutomationStack


app = core.App()
RedshiftPocAutomationStack(app, "redshift-poc-automation", env={'region': 'us-west-2'})

app.synth()
