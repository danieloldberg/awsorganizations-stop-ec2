import boto3
def lambda_handler(event, context):
    client = boto3.client('ec2')
    ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2_regions:
        ec2 = boto3.resource('ec2',region_name=region)
        instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        RunningInstances = [instance.id for instance in instances]
        if RunningInstances:
            stoppingInstances = client.stop_instances(
                InstanceIds=RunningInstances,
                Force=True
            )
            print(stoppingInstances)
    client = boto3.client('rds')
    for region in ec2_regions:
        rdsinstances = client.describe_db_instances()
        print(rdsinstances)
        for db in rdsinstances['DBInstances']:
            stoppingInstances = client.stop_db_instance(
                DBInstanceIdentifier=db['DBInstanceIdentifier']
            )
            print(stoppingInstances)