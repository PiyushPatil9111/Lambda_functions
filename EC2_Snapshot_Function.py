#This is program creates a snapshot of your provided volume and given is current date, then prints the snapshot id

import boto3
import json
import logging
import time
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    current_date = datetime.now().strftime('%d-%m-%Y')

    try:
        response =  ec2.create_snapshot(
            Description='Snapshot taken for testing',
            VolumeId='vol-0377b30794bd25b74',
            TagSpecifications =
            [
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"test_snapshot_{current_date}"
                        }
                    ]
                }
            ],
            DryRun=False
        )
        print("SNapshot is in progress")
        time.sleep(5)
        ec2_resource = boto3.resource("ec2")
        all_snapshots = ec2_resource.snapshots.all()
        for snapshot in all_snapshots:
            if snapshot.tags is not None:   
                for tag in snapshot.tags:
                    if tag['Key'] == 'Name' and tag['Value'] == f"test_snapshot_{current_date}":
                        snapshot_id = snapshot.id
                        print(f"THe new snapshot is created and its snapshot id is {snapshot_id}")

        logger.info(f"THe Snapshot has been created: {json.dump(response, default=str)}")

    except Exception as Ee:
        logger.info(f"The Snapshot was not created because {str(Ee)}")

if __name__ == '__main__':
    lambda_handler(None, None)
    