from typing import Any, List
from pydantic import BaseModel


class StatusRequest(BaseModel):
    jobs: List[str]


class JobStatus(BaseModel):
    status: str
    jobQueue: str
    jobId: str
    jobName: str
    jobArn: str
    jobDefinition: str
    container: Any
    resourceRequirements: Any
    timeout: Any


class JobStatusResponse(BaseModel):
    jobs: List[JobStatus]
