#!/usr/bin/env python3

from aws_cdk import core

from cdk_fargate.cdk_fargate_stack import CdkFargateStack


app = core.App()
CdkFargateStack(app, "cdk-fargate")

app.synth()
