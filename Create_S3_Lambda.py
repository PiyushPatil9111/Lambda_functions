#The following lambda function takes string value as input checks if a bucket of same name already exists if not then,
#Then creates a new cucket and lists all the s3 buckets in your account and then just deletes the newly created s3 bucket

import boto3
def main():
  s3= boto3.resource('s3')   
  x = input('please enter the name of the bucket:')         #Taking input for bucket name

  if createbucket(x) == True:                                   #Calling createbucket function and passing input
   print('\nYour Bucket has not been created with name {x}')
  else:
   print('\nYour Bucket has been created with name {x}')

   print('\nListing all the buckets in your account:')       #Listing all existing buckets in account
   for bucket in s3.buckets.all():
     print(f'\n{bucket.name}')
   new_bucket = s3.Bucket(x)                                 #new_bucket is a variable that reps the new bucket
   print(f'\nDeleting the newly created {new_bucket} now')
   new_bucket.delete()                                                 #Here we delete newly created bucket

def createbucket(bucketname):
 s3= boto3.resource('s3') 
 all_buckets = [bucket.name for bucket in s3.buckets.all()]
 if bucketname not in all_buckets:
   try:
    print(f"\n{bucketname} does not already exist in your ACCOUNT, creating the new bucket")                
    response = s3.create_bucket(
    Bucket= bucketname,
    ACL='private',
    CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    print(response)
   except Exception as ke:
    print(f"\nError: {ke} \n\nthe bucket name must be unique globally, choose a diff name")
    bucket_existsglobally = True
    return bucket_existsglobally
 else:
   print(f"\n{bucketname} already exist, please enter a distinct name")

if __name__ == '__main__':
    main()