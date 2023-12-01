#This code check if the submited instance name is already present amongst the exisiting instances and gives is ID,
#if not then it creates a new instance with the submited name and then waits for 1 minute and then terminates it.

import boto3
import time
def main():
    ec2= boto3.resource('ec2')
    image_id= "ami-06984ea821ac0a879"
    instance_type= "t2.micro"
    key_name= "kube-node"
    instance_name= "my test instance2"

    all_instances= ec2.instances.all()
    instance_exists= None

    for instance in all_instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                instance_id = instance.id
                instance_exists= True
            else:
                instance_id = None
                instance_exists = False
    if instance_exists == False:
        create_instance(image_id, instance_type, key_name, instance_name)
        print("instance is getting created")
        time.sleep(5)
        all_instances= ec2.instances.all()
        for instance in all_instances:
         for tag in instance.tags:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                instance_id = instance.id
                print(f"An instance has been created with the name {instance_name} with instance id {instance_id}")
                time.sleep(60)
                ec2.Instance(instance_id).stop()
                ec2.Instance(instance_id).terminate()
                print(f"here we have terminated the instance {instance_name}")
    else:
        print(f"the instance with name {instance_name} is already present with instance id {instance_id}") 

def create_instance(image_id, instance_type, key_name, instance_name ):
    ec2= boto3.resource('ec2')
    instance = ec2.create_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_name,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': "my test instance2"}
            ]
        }
    ]
)[0]
    
if __name__ == '__main__':
    main()