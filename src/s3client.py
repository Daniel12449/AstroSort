from configparser import ConfigParser
import vars
import logging, boto3

class s3client:
    def __init__(self, config_path):
        
        self.config_path = config_path
        self.session = None
        self.resource = None

        self.createS3resource()
        
    def createS3resource(self):    
        
        if not self.config_path.exists():
            logging.warning("No config file found. Please create it before using s3.")

        cfg = ConfigParser()
        cfg.read(self.config_path)
        
        profile = cfg.get('S3', 'profile_name', fallback='default')
        
        try:
            self.session = boto3.Session(profile_name=profile)
            self.resource = boto3.resource('s3')
        except:
            logging.info("No aws credentials file found or unknown profile: " + profile)
            logging.info("Trying credentials from config file")

        
        service_name = cfg.get('S3', 'service_name', fallback='s3')
        region_name = cfg.get('S3', 'region_name', fallback=None)
        api_version = cfg.get('S3', 'api_version', fallback=None)
        use_ssl = bool(cfg.getboolean('S3', 'use_ssl', fallback='True'))
        verify = bool(cfg.getboolean('S3', 'verify', fallback='True'))
        endpoint_url = cfg.get('S3', 'endpoint_url', fallback=None)
        aws_access_key_id = cfg.get('S3', 'aws_access_key_id', fallback=None)
        aws_secret_access_key = cfg.get('S3', 'aws_secret_access_key', fallback=None)
        aws_session_token = cfg.get('S3', 'aws_session_token', fallback=None)
        config = boto3.session.Config(cfg.get('S3', 'config', fallback=None))
        
        try:
            self.resource = boto3.resource(service_name,
                region_name,
                api_version,
                use_ssl,
                verify,
                endpoint_url,
                aws_access_key_id,
                aws_secret_access_key,
                aws_session_token,
                config
            )

            logging.info("S3 Resource created with config file parameters.")
        except:
            logging.warning("Unable to create the s3 resource")
            
    def getBuckets(self):
        bucket_names = []
        buckets = self.resource.buckets.all()
        for bucket in buckets:
            bucket_names.append(bucket.name)

        vars.s3_bucket_list = bucket_names
        
