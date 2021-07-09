#!/bin/bash -e
redshift_pwd=`python3 << END
import boto3
secrets_client = boto3.client(service_name='secretsmanager',region_name='us-east-1')
get_secret_value_response = secrets_client.get_secret_value(SecretId='RedshiftClusterSecretAA')
print([value for value in get_secret_value_response.values()][3])
END`

sed -i "s/password: 'redshift_pwd'/password: '$redshift_pwd'/" ./sctcliauto.scts

#java -XX:+UseParallelGC --add-opens=java.base/jdk.internal.loader=ALL-UNNAMED --add-exports=java.base/jdk.internal.loader=ALL-UNNAMED --add-exports=java.base/jdk.internal.misc=ALL-UNNAMED -jar "/opt/aws-schema-conversion-tool/lib/app/AWSSchemaConversionToolBatch.jar" -type scts -script sctcliauto.scts

