import boto3

region_name = 'us-west-2'

#print('s3_save(%s, %s)' % (s3path, content))
s3 = boto3.client(
    service_name = "s3",
    region_name = region_name
)
print('s3: client')

paginator = s3.get_paginator('list_objects_v2')
response_iterator = paginator.paginate(
    Bucket="mlops-lims-dump-prod", 
    Prefix="output_files/"
)
print(response_iterator)
try:
    for page in response_iterator:
        print(page)
except Exception as e:
    print(e)
    raise e
