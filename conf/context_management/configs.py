import os


BUCKET_NAME = "dev-template-repo"


ENVIRONMENTS = {
    "dev",
    "test",
    "ua_test",
    "prod",
}


CATALOG_MAPPINGS = {
    "{s3_bucket}": BUCKET_NAME,
    "{credentials}": "aws_s3_credentials",
}


CREDENTIALS_MAPPINGS = {
    "{aws_access_key_id}": os.environ["aws_access_key_id"],
    "{aws_secret_access_key}": os.environ["aws_secret_access_key"],
}
