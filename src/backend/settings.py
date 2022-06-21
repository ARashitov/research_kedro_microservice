import os


ENVIRONMENT = os.environ["ENVIRONMENT"]

AWS_CREDENTIALS = {
    "aws_access_key_id": os.environ["aws_access_key_id"],
    "aws_secret_access_key": os.environ["aws_secret_access_key"],
}
