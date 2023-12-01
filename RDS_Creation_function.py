import boto3
import time

def main():
    rds = boto3.client('rds')
    username = 'mydbuser'
    password = 'mydbpassword'
    db_subnet_grp = 'my-subnet-group'
    db_cluster_id = 'my-rds-cluster'

    # Check if the DB cluster exists
    response = None
    try:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        print(f"The RDS cluster with the name {db_cluster_id} already exists")
    except rds.exceptions.DBClusterNotFoundFault:
        pass  # Cluster does not exist, proceed with creation

    # If the cluster doesn't exist, create it
    if not response:
        response = rds.create_db_cluster(
            MasterUsername=username,
            MasterUserPassword=password,
            DBClusterIdentifier=db_cluster_id,
            DBSubnetGroupName=db_subnet_grp,
            Engine='aurora-mysql',
            EngineVersion='5.7.mysql_aurora.2.08.3',
            DatabaseName='my_rds_db',
            EnableHttpEndpoint=True,
            EngineMode='serverless',
            ScalingConfiguration={
                'MinCapacity': 1,
                'MaxCapacity': 2,
                'AutoPause': True,
                'SecondsUntilAutoPause': 300,
            }
        )

    # Wait for the cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response['DBClusters'][0]['Status']
        if status == 'available':
            print(f"The new RDS {db_cluster_id} has been created and its status is {status}")
            break
        time.sleep(40)
        print(f"The status of the new RDS {db_cluster_id} is {status}")

if __name__ == '__main__':
    main()
