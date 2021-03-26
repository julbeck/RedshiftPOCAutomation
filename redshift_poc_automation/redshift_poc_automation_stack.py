from aws_cdk import aws_redshift as _redshift
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_secretsmanager as _sm
from aws_cdk import core

class RedshiftPocAutomationStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct, id: str,
        vpc,
        ec2_instance_type: str,
        numberofnodes: int,
        stack_log_level: str,
        **kwargs

    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Cluster Password
        comments_cluster_secret = _sm.Secret(
            self,
            "setRedshiftDemoClusterSecret",
            description="Redshift Demo Cluster Secret",
            secret_name="RedshiftDemoClusterSecret",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Subnet Group for Cluster

        demo_cluster_subnet_group = _redshift.CfnClusterSubnetGroup(
            self,
            "redshiftDemoClusterSubnetGroup",
            subnet_ids=vpc.get_vpc_public_subnet_ids,
            description="Redshift Demo Cluster Subnet Group"
        )

        if numberofnodes > 1:
          clustertype="multi-node"
        else:
          clustertype="single-node"
          numberofnodes=None

        self.demo_cluster = _redshift.CfnCluster(
            self,
            "redshiftDemoCluster",
            cluster_type=clustertype,
            number_of_nodes=numberofnodes,
            db_name="comments_cluster",
            master_username="dwh_user",
            master_user_password="W7wFE7ojiL9TeLFQ11cm7uuKu1amu4rc",
            node_type=f"{ec2_instance_type}",
            cluster_subnet_group_name=demo_cluster_subnet_group.ref
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
