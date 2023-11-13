import boto3
def main():
  s3 = boto3.resource('s3')
  # Creating new files to upload to s3
  file1 = r'D:\python_for_Lambda_func\Lambda_functions\file1.txt'
  file2 = r'D:\python_for_Lambda_func\Lambda_functions\file2.txt'
  #printing the name of all buckets in the account
  for buckets in s3.buckets.all():
    print(f"{buckets.name}")
  #Taking the name of requied s3 bucket
  bucket_name = input("input the name of the bucet to upaload objects:")

  #Uploading file1 and file2 to s3 bucket mentioned
  upload_bucket = s3.Bucket(bucket_name)
  upload_bucket.upload_file(Filename= file1 , Key= "file_1.txt")
  upload_bucket.upload_file(Filename= file2 , Key= "file_2.txt")

  #printing the name content of object
  obj = upload_bucket.Object("file_1.txt")
  body = obj.get()['Body'].read()
  print(body)

  #replacing body of file1 with file2

  upload_bucket.Object("file_1.txt").put(Body= open(file2, 'rb'))   # here 'rb' means we are opening the file in read binary mode
  obj = upload_bucket.Object("file_1.txt")
  body = obj.get()['Body'].read()
  print(body)

  #Deleting all the objects from s3 bucket
  upload_bucket.objects.all().delete()

if __name__ == '__main__':
  main()

    