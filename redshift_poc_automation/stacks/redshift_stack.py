from aws_cdk import aws_redshift
from aws_cdk import aws_ec2
from aws_cdk import aws_iam
from aws_cdk import aws_secretsmanager
from aws_cdk import core
import json

class RedshiftStack(core.Stack):

    def __init__(
            self,
            scope: core.Construct, id: str,
            vpc,
            redshift_endpoint: str,
            redshift_config: dict,
            stack_log_level: str,
            **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # if redshift_endpoint != "CREATE":
        #     self.vpc = aws_ec2.Vpc.from_lookup(
        #         self, "vpc",
        #         vpc_id=vpc_id
        #     )
        # else:

        cluster_identifier = redshift_config.get('cluster_identifier')
        database_name = redshift_config.get('database_name')
        node_type = redshift_config.get('node_type')
        number_of_nodes = int(redshift_config.get('number_of_nodes'))
        master_user_name = redshift_config.get('master_user_name')

        secret_string = aws_secretsmanager.SecretStringGenerator(secret_string_template=json.dumps({'username': master_user_name}),
                                                                 generate_string_key='password')

        # Create Cluster Password
        cluster_masteruser_secret = aws_secretsmanager.Secret(
            self,
            "setRedshiftDemoClusterSecret",
            description="Redshift Demo Cluster Secret",
            secret_name="RedshiftDemoClusterSecret",
            generate_secret_string= secret_string,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        cluster_iam_role = aws_iam.Role(
            self, "redshiftClusterRole",
            assumed_by=aws_iam.ServicePrincipal(
                "redshift.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonS3ReadOnlyAccess"
                )
            ]
        )
        cluster_masteruser_secret.grant_read(cluster_iam_role)

        cluster_subnet_group = aws_redshift.CfnClusterSubnetGroup(
            self,
            "redshiftDemoClusterSubnetGroup",
            subnet_ids=vpc.get_vpc_private_isolated_subnet_ids,
            description="Redshift Demo Cluster Subnet Group"
        )

        # clusterpwd = core.SecretValue.secrets_manager('RedshiftDemoClusterSecret').to_string()

        # Subnet Group for Cluster



        if number_of_nodes > 1:
            clustertype = "multi-node"
        else:
            clustertype = "single-node"
            number_of_nodes = None

        self.demo_cluster = aws_redshift.CfnCluster(
            self,
            cluster_identifier,
            cluster_type=clustertype,
            number_of_nodes=number_of_nodes,
            db_name=database_name,
            master_username=master_user_name,
            # master_user_password=cluster_masteruser_secret.secret_value.to_string(),
            master_user_password="Test#12345", ################################################ TODO FIX IT ##############################################
            iam_roles=[cluster_iam_role.role_arn],
            node_type=f"{node_type}",
            cluster_subnet_group_name=cluster_subnet_group.ref
        )



    # properties to share with other stacks
    @property
    def get_cluster(self):
        return self.demo_cluster

    @property
    def get_cluster_dbname(self):
        return self.demo_cluster.db_name

    @property
    def get_cluster_user(self):
        return self.demo_cluster.master_username

    @property
    def get_cluster_password(self):
        return self.demo_cluster.master_user_password

    @property
    def get_cluster_host(self):
        return self.demo_cluster.attr_endpoint_address

        ###########################################
        ################# OUTPUTS #################
        ###########################################
        output_1 = core.CfnOutput(
            self,
            "RedshiftCluster",
            value=f"{demo_cluster.attr_endpoint_address}",
            description=f"RedshiftCluster Endpoint"
        )

        output_2 = core.CfnOutput(
            self,
            "RedshiftClusterPassword",
            value=(
                f"https://console.aws.amazon.com/secretsmanager/home?region="
                f"{core.Aws.REGION}"
                f"#/secret?name="
                f"{comments_cluster_secret.secret_arn}"
            ),
            description=f"Redshift Cluster Password in Secrets Manager"
        )
        output_3 = core.CfnOutput(
            self,
            "RedshiftIAMRole",
            value=(
                f"{_rs_cluster_role.role_arn}"
            ),
            description=f"Redshift Cluster IAM Role Arn"
        )
