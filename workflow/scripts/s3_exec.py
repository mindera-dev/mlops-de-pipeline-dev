import boto3

region_name = 'us-west-2'
def s3_save(s3path, content):
    print('s3_save(%s, %s)' % (s3path, content))
    s3 = boto3.client(
        service_name = "s3",
        region_name = region_name
    )
    print('s3: client')

    s3addreass = s3path.split('/')
    s3.put_object(Bucket=s3addreass[0], 
                Key=s3addreass[1], 
                Body=content)
    print('upload_file:',s3path) 
