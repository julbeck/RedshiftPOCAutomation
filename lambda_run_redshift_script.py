import boto3
import time
import traceback
import botocore.exceptions as be
import json
import os
import cfnresponse

def handler(event, context):
    print(event)
    redshift_host=os.environ('REDSHIFT_HOST')
    redshift_iam_role=os.environ('REDSHIFT_IAM_ROLE')
    script_s3_path=os.environ('SCRIPT_S3_PATH')

    db = event['Input'].get('db')
    user = event['Input'].get('user')

    parameter_group_name = event['Input'].get('parameter_group_name')
    sql_id = event['Input'].get('sql_id')
    source_clusterid = event['Input'].get('source_clusterid')
    cluster_type = event['Input'].get('cluster_type')
    clusterid = source_clusterid + "-" + cluster_type if cluster_type else source_clusterid

    try:
        client = boto3.client('redshift')
        extract_prefix = json.loads(get_config_from_s3(extract_bucket, 'config/extract_prefix.json')) if extract_bucket else {'prefix':'','extract_output':''}
        prefix = extract_prefix['prefix']
        extract_output = extract_prefix['extract_output']
        if action == "cluster_status":
            res = {'status': cluster_status(client, clusterid)}
        elif action == "setup_redshift_objects":
            res = {'sql_id': setup_redshift_objects(replay_bucket, clusterid, db, user)}
        elif action == "unload_stats":
            script = "call unload_detailed_query_stats('" + prefix + "')"
            sql_id = run_sql(clusterid, db, user, script)
            res = {'sql_id': sql_id}
        elif action == "load_stats":
            script = "call load_detailed_query_stats('" + prefix + "')"
            sql_id = run_sql(clusterid, db, user, script, False, 'async')
            res = {'sql_id': sql_id}
        elif action == "sql_status":
            res = {'status': sql_status(sql_id)}
        else:
            raise ValueError("Invalid Task: " + action)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise
    print(res)
    return res

def cluster_status(client, clusterid):
    try:
        desc = client.describe_clusters(ClusterIdentifier=clusterid)['Clusters'][0]
        if isinstance(desc, dict):
            status = desc.get('ClusterStatus') + desc.get('ClusterAvailabilityStatus') + (desc.get('RestoreStatus').get('Status') if desc.get('RestoreStatus') else "")
        else:
            status = 'Unavailable'
    except be.ClientError as e:
        msg = e.response['Error']['Code']
        if msg == 'ClusterNotFound':
            status = 'nonExistent'
        else:
            print(desc)
            raise
    return status

def get_config_from_s3(bucket, key):
    obj = boto3.client('s3').get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode('utf-8')

def setup_redshift_objects(bucket, clusterid, db, user):
    key = 'config/setup_redshift_objects.sql'
    script = get_config_from_s3(bucket, key)
    sql_id = run_sql(clusterid, db, user, script)
    return sql_id

def run_sql(clusterid, db, user, script, with_event=True, run_type='sync'):
    res = boto3.client("redshift-data").execute_statement(Database=db, DbUser=user, Sql=script,
                                                          ClusterIdentifier=clusterid, WithEvent=with_event)
    query_id = res["Id"]
    statuses = ["STARTED", "FAILED", "FINISHED"] if run_type == 'async' else ["FAILED", "FINISHED"]
    done = False
    while not done:
        status = sql_status(query_id)
        if status in statuses:
            break
    return query_id

def sql_status(query_id):
    res = boto3.client("redshift-data").describe_statement(Id=query_id)
    status = res["Status"]
    if status == "FAILED":
        raise Exception('Error:' + res["Error"])
    return status.strip('"')
