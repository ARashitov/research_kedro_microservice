import os
import boto3
from .settings import AWS_CREDENTIALS


AWS_BATCH_CLIENT = boto3.client(
    "batch",
    **{
        **AWS_CREDENTIALS,
        "region_name": os.environ["aws_region"],
    },
)
AWS_BATCH_SUBMIT_JOB_CONFIGS = {
    "jobDefinition": "test-research-kedro-microservice-job-definition",
    "schedulingPriorityOverride": 123,
    "shareIdentifier": "A1*",
    "jobQueue": "test-research-kedro-microservice-spot",
}
