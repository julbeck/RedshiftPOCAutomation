from aws_cdk import aws_iam
from aws_cdk import aws_ec2
from aws_cdk import core
from aws_cdk import aws_secretsmanager
import boto3
import json

class SctOnPremToRedshiftStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct, id: str,
        cluster,
        dmsredshift_config: dict,
        sctredshift_config: dict,
        redshift_config: dict,
        vpc,
        stack_log_level: str,
        **kwargs

    ) -> None:
        super().__init__(scope, id, **kwargs)

        source_db = dmsredshift_config.get('source_db')
        source_engine = dmsredshift_config.get('source_engine')
        source_schema = dmsredshift_config.get('source_schema')
        source_host = dmsredshift_config.get('source_host')
        source_user = dmsredshift_config.get('source_user')
        source_pwd = dmsredshift_config.get('source_pwd')
        keyname = sctredshift_config.get('key_name')
        s3_bucket_output = sctredshift_config.get('s3_bucket_output')
        source_port = int(dmsredshift_config.get('source_port'))
        redshift_host = cluster.get_cluster_host
        redshift_db = cluster.get_cluster_dbname
        redshift_user = cluster.get_cluster_user
        redshift_port = cluster.get_cluster_iam_role
        secret_arn = 'RedshiftClusterSecretAA'
        amiID = 'ami-042e0580ee1b9e2af'

        if source_engine == 'sqlserver':
            source_sct = 'MSSQLDW'

        with open("./sctconfig.sh") as f:
            user_data = f.read()

        with open("./sctconfig2.sh") as f:
            user_data2 = f.read()

        # Instance Role and SSM Managed Policy
        role = aws_iam.Role(self, "InstanceSSM", assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))
        role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))

        #secrets_client = boto3.client(service_name='secretsmanager', region_name='us-east-1')
        #get_secret_value_response = secrets_client.get_secret_value(
        #    SecretId=secret_arn
        #)
        #redshift_pwd = [value for value in get_secret_value_response.values()][3]

        ### TAKE THIS OUT SO THAT INSTANCE IS NOT PUBLIC ###
        subnet = aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType('PUBLIC'))

        my_security_group = aws_ec2.SecurityGroup(self, "SecurityGroup",
                                              vpc=vpc.vpc,
                                              description="Allow ssh access to ec2 instances",
                                              allow_all_outbound=True
                                              )
        my_security_group.add_ingress_rule(aws_ec2.Peer.any_ipv4(), aws_ec2.Port.tcp(22), "allow ssh access from the world")
        my_security_group.add_ingress_rule(my_security_group, aws_ec2.Port.all_tcp(), "self-referencing rule")

        custom_ami = aws_ec2.MachineImage.latest_amazon_linux(
            generation=aws_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=aws_ec2.AmazonLinuxEdition.STANDARD,
            virtualization=aws_ec2.AmazonLinuxVirt.HVM,
            storage=aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
        # Instance

        instance = aws_ec2.Instance(self, "Instance",
            instance_type=aws_ec2.InstanceType("m5.large"),
            machine_image=custom_ami,
            vpc = vpc.vpc,
            vpc_subnets=subnet,
            key_name=keyname,
            role = role,
            security_group=my_security_group,
#            resource_signal_timeout=core.Duration.minutes(5),
            user_data=aws_ec2.UserData.custom(user_data)
            )

        sctcommand = 'sh sctrun.sh ' + source_sct + " REDSHIFT " + source_host + " " + str(source_port) + " " + source_db + " " + source_schema + " " + source_user + " " + source_pwd + " " + redshift_host + " 5439 " + redshift_db + " " + redshift_user + " " + 'redshift_pwd'
        #print(sctcommand)
        instance.add_user_data(sctcommand)

        instance.add_user_data(user_data2)

        sctcommand2 = 'java -XX:+UseParallelGC --add-opens=java.base/jdk.internal.loader=ALL-UNNAMED --add-exports=java.base/jdk.internal.loader=ALL-UNNAMED --add-exports=java.base/jdk.internal.misc=ALL-UNNAMED -jar "/opt/aws-schema-conversion-tool/lib/app/AWSSchemaConversionToolBatch.jar" -type scts -script sctcliauto.scts'
        instance.add_user_data(sctcommand2)

        sctcommand3 = 'aws s3 cp /awsutilities/SCT/schemaddl.sql ' + s3_bucket_output
        instance.add_user_data(sctcommand3)

        sctcommand4 = 'aws s3 cp /awsutilities/SCT/assessmentreport.pdf ' + s3_bucket_output
        instance.add_user_data(sctcommand4)
