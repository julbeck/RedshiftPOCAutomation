
<script>
echo Current date and time >> %SystemRoot%\Temp\test.log
echo %DATE% %TIME% >> %SystemRoot%\Temp\test.log
cd c:\
mkdir SCT
cd SCT
curl -o aws-schema-conversion-tool-1.0.latest.zip  https://s3.amazonaws.com/publicsctdownload/Windows/aws-schema-conversion-tool-1.0.latest.zip
tar -xf aws-schema-conversion-tool-1.0.latest.zip
msiexec.exe /i "AWS Schema Conversion Tool-1.0.652.msi" /passive /l log.txt
curl -o AWSCLIV2.msi https://awscli.amazonaws.com/AWSCLIV2.msi
msiexec.exe /i "AWSCLIV2.msi" /passive /l logcli.txt
set PATH="c:\Program Files\Amazon\AWSCLIV2\";%PATH%
aws configure set role_arn arn:aws:iam::962393875414:role/windows-cli-role
aws configure set credential_source Ec2InstanceMetadata
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/sctcliauto.scts sctcliauto.scts
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/sctrun.sh sctrun.sh
mkdir Drivers
cd Drivers
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/mssql-jdbc-7.4.1.jre8.jar mssql-jdbc-7.4.1.jre8.jar
aws s3 cp s3://event-driven-app-with-lambda-redshift/scripts/redshift-jdbc42-2.0.0.4.jar redshift-jdbc42-2.0.0.4.jar
</script>
