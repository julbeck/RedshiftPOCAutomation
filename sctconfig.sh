#!/bin/bash -e
mkdir /awsutilities
cd /awsutilities
mkdir SCT
curl -o aws-schema-conversion-tool-1.0.latest.zip  https://s3.amazonaws.com/publicsctdownload/Fedora/aws-schema-conversion-tool-1.0.latest.zip
unzip aws-schema-conversion-tool-1.0.latest.zip
yum -y install aws-schema-conversion-tool-*.rpm
yum -y install java-11-amazon-corretto
mkdir /usr/local/jdbc-drivers
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/mssql-jdbc-7.4.1.jre8.jar /usr/local/jdbc-drivers/mssql-jdbc-7.4.1.jre8.jar
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/redshift-jdbc42-2.0.0.4.jar /usr/local/jdbc-drivers/redshift-jdbc42-2.0.0.4.jar
chmod 755 /usr/local/jdbc-drivers/*
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/sctcliauto.scts ./sctcliauto.scts
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/sctrun.sh ./sctrun.sh

#mypwd=$(aws secretsmanager get-secret-value --region us-east-1 --secret-id arn:aws:secretsmanager:us-east-1:320963489128:secret:setRedshiftDemoClusterSecre-xZVBT6zvxSMy-kvgtVh| python3 -c "import json, sys; print(json.load(sys.stdin)['SecretString'])")

#sed -i "s/password: ''/password: '$mypwd'/" ./sctcliauto.scts
