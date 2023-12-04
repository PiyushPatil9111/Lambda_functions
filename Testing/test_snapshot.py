import boto3
import json
import logging
from datetime import datetime

def main():
    current_date = datetime.now().strftime('%Y-%m-%d')
    # ec2 = boto3.resource("ec2")
    # all_snapshots = ec2.snapshots.all()
    # for snapshot in all_snapshots:
    #   if snapshot.tags is not None:   
    #     for tag in snapshot.tags:
    #         if tag['Key'] == 'Name' and tag['Value'] == 'my_todo_snapshot':
    #             snapshot_id = snapshot.id
    #             print(f"THe new snapshot is created and its snapshot id is {snapshot_id}")
    print(f"{current_date}")

if __name__ == '__main__':
    main()



