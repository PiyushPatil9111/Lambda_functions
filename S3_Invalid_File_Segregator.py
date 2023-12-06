import boto3
import json
import csv
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    #Taking name of the bucket and the name of the CSV object from the eventbridge generated event from s3 once an obect is uploaded
    upload_bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['name']
    #Name of the error bucket
    error_bucket = 'my-csv-error-bucket'
    #puling the csv file object
    obj = s3.object(upload_bucket, csv_file)
    #Reading and decoding the data from CSV whit split lines
    data = obj.get()['Body'].read().decode('utf-8').splitlines()
    error_found = False

    #defining the valid product lines and valid currencies
    valid_product_line = ['Bakery', 'Meat', 'Dairy']
    valid_currency = ['USD', 'MXN', 'CAD']

    #Iterating through each row in the data file except for first row which has column names and keeping comma as
    #a delimiter.
    for row in csv.reader(data[1:], delimiter= ','):
        print(f"{row}")
        #Separating the date, product line, currency, bill amount from the specific columns in each row.
        #Since we separated each row from the data using splitlines earlier, now each row acts as a list
        #Now in each row every 6th object is date and every 4th object is product line
        date = row[6]
        product_line = row[4]
        currency = row[7]
        bill_amount = float(row[8])
        #Checking if product line is valid
        if product_line not in valid_product_line:
            print(f"THe product line {product_line} is invalid in row {row[0]}")
            error_found = True
            break
        #Checking if Currency is Valid
        if currency not in valid_currency:
            print(f"THe product line {currency} is invalid in row {row[0]}")
            error_found = True
            break
        #Checking if bill amount is not negative
        if bill_amount < 0.0:
            print(f"THe bill amount {bill_amount} is invalid in row {row[0]}")
            error_found = True
            break
        #Checking if date is in correct format
        try:
            date = datetime.strptime(date, '%Y-%m-%d')  #With strptime, it parses the provided date through the format given, if our date in that format, then returns our date, else throws valueError
        except ValueError as Vv:
            print(f"THe date {date} is present in row {row[0]} is in incorrect format")
            error_found = True
            break
    #If an error is found, sending the problematic CSV file to the Error Bucket and deleting the CSV from upload bucket
    if error_found:
        source_file = {
            'Bucket': upload_bucket,
            'Key': csv_file
        }
        try:
            s3.meta.client.copy(source_file, error_bucket, csv_file)
            print(f"THe {csv_file} with invalid values has been copied to {error_bucket} ")
            s3.object(upload_bucket, csv_file).delete()
            print(f"Deleted the original file from {upload_bucket} ")
        except Exception as E:
            print(f"Error while copying files to error_bucket {str(E)}")
    else:
        return {
            'statusCode': 200,
            'body': ('TO anamoly folund in the uploaded file')
        }