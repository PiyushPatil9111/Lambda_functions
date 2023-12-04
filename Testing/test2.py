import boto3
import time

def main():
    rds = boto3.client('rds')
    username = 'mydbuser'
    password = 'mydbpassword'  # Fixed the typo in the password
    db_subnet_grp = 'my-subnet-group'
    db_cluster_id = 'my-rds-cluster'

    # Creating the DB cluster
    try:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        print(f"The RDS cluster with the name {db_cluster_id} already exists")
    except rds.exceptions.DBClusterNotFoundFault:
        pass

    response = rds.create_db_cluster(
        MasterUsername=username,
        MasterUserPassword=password,
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
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)  # Pass DBClusterIdentifier parameter
        clusters = response.get('DBClusters', [])
        if clusters and clusters[0].get('Status') == 'available':
            print(f"The new RDS {db_cluster_id} has been created and its status is available")
            break
        time.sleep(40)
        print(f"The status of the new RDS {db_cluster_id} is not available yet. Retrying...")


if __name__ == '__main__':
    main()