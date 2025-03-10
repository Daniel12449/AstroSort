import boto3
import hashlib

#from configparser import ConfigParser

# config_path = pathlib.Path('/home/daniel/.config/astrosort.ini')

# cfg = ConfigParser()
# cfg.read(config_path)
       

# service_name = cfg.get('S3', 'service_name', fallback='s3')
# region_name = cfg.get('S3', 'region_name', fallback=None)
# api_version = cfg.get('S3', 'api_version', fallback=None)
# use_ssl = cfg.getboolean('S3', 'use_ssl', fallback='True')
# verify = cfg.getboolean('S3', 'verify', fallback='True')
# endpoint_url = cfg.get('S3', 'endpoint_url', fallback=None)
# aws_access_key_id = cfg.get('S3', 'aws_access_key_id', fallback=None)
# aws_secret_access_key = cfg.get('S3', 'aws_secret_access_key', fallback=None)
# aws_session_token = cfg.get('S3', 'aws_session_token', fallback=None)
# config = cfg.get('S3', 'config', fallback=None)

service_name = 's3'
endpoint_url = 'https://cephgw2.relaix.net'
aws_access_key_id = 'D5VC3MNPUMEL6K6HI1RX' 
aws_secret_access_key = '9DdOSprGHzUmVHzTsGE8aBVL7XnA1jr3Kw8GOe1T'

resource = boto3.resource(service_name=service_name,
                #region_name=region_name,
                #api_version=api_version,
                #use_ssl=use_ssl,
                #verify=bool(verify),
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                #aws_session_token=aws_session_token,
                #config=config
            )

conn = boto3

input_path = 'astrosort.ini'
new_name = 'File/test.ini'
bucket_name = 'test-astroraw'
#resource.put_object(input_path, new_name, Body= ChecksumAlgorithm="sha1")


with open(input_path, 'rb') as data:
    resource.Bucket(bucket_name).put_object(Key=new_name, Body=data)

