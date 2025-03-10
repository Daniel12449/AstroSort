import boto3

# Credentials
s3_url = 'https://cephgw2.relaix.net'
s3_access_key = 'D5VC3MNPUMEL6K6HI1RX'
s3_secret_key = '9DdOSprGHzUmVHzTsGE8aBVL7XnA1jr3Kw8GOe1T'



s3_target = boto3.resource('s3', 
    endpoint_url=s3_url,
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key,
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4')
)

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html

#buckets = s3_target.buckets.all()
#for bucket in buckets:
#    print(bucket.name)
    
int_buckets = s3_target.Bucket('zeitraffer')

folders = set()
files = []

for obj in int_buckets.objects.all():
    # Add the folder (prefix) to the set (folder is determined by the object's key)
    folder = obj.key.split('/')[0]
    if folder and obj.key != folder:
        folders.add(folder)
    # Add the file to the list of files
    files.append(obj.key)
    
print("Folders:")
for folder in folders:
    print(f"Folder: {folder}/")

print("\nFiles:")
for file in files:
    print(f"File: {file}")