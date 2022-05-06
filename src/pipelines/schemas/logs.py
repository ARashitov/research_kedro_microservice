from typing import Any, List, Literal, Union
from pydantic import BaseModel


class NodeLog(BaseModel):
    inputs: Union[List[str], str, None]
    outputs: Union[List[str], str, None]
    name: str
    namespace: Union[str, None]
    tags: Union[Any, None]
    confirms: Union[Any, None]


class PipelineLog(BaseModel):
    inputs: Union[List[str], str, None]
    outputs: Union[List[str], str, None]
    name: str
    namespace: Union[str, None]
    tags: Union[Any, None]
    confirms: Union[Any, None]


class DatasetLog(BaseModel):
    dataset_name: str
    operation: Literal["save", "load"]


class KedroExecutionDetails(BaseModel):
    environment: Literal["dev", "test", "ua_test", "prod"]
    task_id: Union[str, None]
    stage: Literal["pipeline", "node", "dataset"]
    step: Literal["before", "after"]
    datetime: str
    duration: Union[float, None] = None


class KedroLogRecord(KedroExecutionDetails):
    """Schema used to capture kedro pipeline logs"""

    element_log: Union[PipelineLog, NodeLog, DatasetLog]
