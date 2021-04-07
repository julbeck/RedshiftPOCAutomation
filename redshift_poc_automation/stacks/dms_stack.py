from aws_cdk import aws_dms as _dms
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam
from aws_cdk import core

class GlobalArgs():
    """
    Helper to define global statics
    """

    OWNER = "SamirKakli"
    ENVIRONMENT = "development"
    REPO_NAME = "redshift-demo"
    SOURCE_INFO = f"https://github.com/kaklis/{REPO_NAME}"
    VERSION = "2021_03_15"
    SUPPORT_EMAIL = ["kaklis@amazon.com", ]

class DmsStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct, id: str,
        vpc,
        cluster,
        source_engine,
        source_db,
        source_schema,
        source_host,
        source_user,
        source_pwd,
        source_port,
        migrationtype,
        stack_log_level: str,
        **kwargs

    ) -> None:
        super().__init__(scope, id, **kwargs)

        # DMS IAM Role
#        if from_vpc_id is not None:
#            self.vpc = _ec2.Vpc.from_lookup(
#                self, "vpc",
#                vpc_id=from_vpc_id
#            )
#        else:

        _rs_cluster_role = _iam.Role(
            self, "dmsvpcrole",
            assumed_by=_iam.ServicePrincipal(
                "dms.amazonaws.com"),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonDMSVPCManagementRole"
                )
            ],
            role_name = "dms-vpc-role"
        )

        tablemappings="""{
          "rules": [
            {
              "rule-type": "selection",
              "rule-id": "1",
              "rule-name": "1",
              "object-locator": {
                "schema-name": "%"""+source_schema + """",
                "table-name": "%"
              },
              "rule-action": "include",
              "filters": []
            }
          ]
        }"""

        self.dms_endpoint_tgt = _dms.CfnEndpoint(
            self,
            "DMSendpointtgt",
            endpoint_type="target",
            engine_name="redshift",
            database_name=f"{cluster.get_cluster_dbname}",
            password=f"{cluster.get_cluster_password}",
            username=f"{cluster.get_cluster_user}",
            server_name=f"{cluster.get_cluster_host}",
            port=5439
         )

        self.dms_endpoint_src = _dms.CfnEndpoint(
            self,
            "DMSendpointsrc",
            endpoint_type="source",
            engine_name=source_engine,
            database_name=source_db,
            password=source_pwd,
            port=source_port,
            username=source_user,
            server_name=source_host,
         )

        dmssubnetgrp = _dms.CfnReplicationSubnetGroup(
            self,
            "DMSsubnetgroup",
            replication_subnet_group_description="Subnet group for DMS replication instance",
            subnet_ids=vpc.get_vpc_public_subnet_ids
         )

        self.dms = _dms.CfnReplicationInstance(
            self,
            "SQLservertoRedshift",
            replication_instance_class="dms.t3.medium",
            allocated_storage=50,
            allow_major_version_upgrade=None,
            auto_minor_version_upgrade=None,
            multi_az=False,
            publicly_accessible=True,
            replication_subnet_group_identifier=dmssubnetgrp.ref
        )

        dms_task = _dms.CfnReplicationTask(
            self,
            "DMSreplicationtask",
            migration_type=migrationtype,
            replication_instance_arn=self.get_repinstance_id,
            source_endpoint_arn=self.get_srcendpoint_id,
            target_endpoint_arn=self.get_tgtendpoint_id,
            table_mappings=tablemappings
        )

    @property
    def get_repinstance_id(self):
        return self.dms.ref

    @property
    def get_tgtendpoint_id(self):
        return self.dms_endpoint_tgt.ref

    @property
    def get_srcendpoint_id(self):
        return self.dms_endpoint_src.ref

