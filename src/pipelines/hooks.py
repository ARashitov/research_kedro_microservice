import logging
import os
from abc import ABC
from datetime import datetime
from typing import Any, Dict, Union

from kedro.framework.hooks import hook_impl
from kedro.pipeline.node import Node


from .schemas.logs import DatasetLog, KedroExecutionDetails, KedroLogRecord, NodeLog, PipelineLog

ENVIORNMENT = os.environ["ENVIRONMENT"]

KEDRO_LOGGER = logging.getLogger("pipeline")
_TASK_ID_REGISTRY = "task_id"

_BEFORE_STEP = "before"
_AFTER_STEP = "after"

_PIPELINE_STAGE = "pipeline"
_NODE_STAGE = "node"
_DATASET_STAGE = "dataset"


class AbstractLogger(ABC):
    """
    Abstract Node & Pipeline logger
    """

    def _log(self, kedro_log: Dict[str, Any]) -> None:
        KEDRO_LOGGER.info(kedro_log)

    def _factory_execution_log(self, *args, **kwargs):
        return KedroExecutionDetails(*args, **kwargs)

    def _factory_log_instance(
        self,
        element_log: Union[NodeLog, PipelineLog],
        execution_log: KedroExecutionDetails,
    ) -> None:
        return KedroLogRecord(
            **execution_log.dict(),
            element_log=element_log,
        )

    def _create_log_instance_and_send_to_logger(self, element_log: Any, execution_log: KedroExecutionDetails):
        log_instance = self._factory_log_instance(
            element_log=element_log,
            execution_log=execution_log,
        )
        self._log(log_instance.dict())


class NodeLoggingHooks(AbstractLogger):
    """
    Node hook logger
    """

    def __init__(self):
        self._start_time = datetime.now()
        self._end_time = datetime.now()

    def __factory_node_log(self, node: Node) -> NodeLog:
        node_attrs = node.__dict__
        return NodeLog(
            inputs=node_attrs["_inputs"],
            outputs=node_attrs["_outputs"],
            name=node_attrs["_name"],
            namespace=node_attrs.get("_namespace"),
            tags=node_attrs.get("_tags"),
            confirms=node_attrs.get("_confirms"),
        )

    @hook_impl
    def before_node_run(
        self,
        node: Node,
        session_id: str,
    ) -> None:
        self._start_time = datetime.now()

        node_log = self.__factory_node_log(node)
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=session_id,
            stage=_NODE_STAGE,
            step=_BEFORE_STEP,
            datetime=str(self._start_time),
        )

        self._create_log_instance_and_send_to_logger(node_log, execution_log)

    @hook_impl
    def after_node_run(
        self,
        node: Node,
        session_id: str,
    ) -> None:

        self._end_time = datetime.now()
        duration = (self._end_time - self._start_time).total_seconds()
        duration = float(duration)

        node_log = self.__factory_node_log(node)
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=session_id,
            stage=_NODE_STAGE,
            step=_AFTER_STEP,
            datetime=str(self._end_time),
            duration=duration,
        )

        self._create_log_instance_and_send_to_logger(node_log, execution_log)


class DatasetLoggingHooks(AbstractLogger):
    """
    Node hook logger
    """

    LOAD_OPERATION = "load"
    SAVE_OPERATION = "save"

    def __init__(self):
        self._start_time = datetime.now()
        self._end_time = datetime.now()

    @hook_impl
    def before_dataset_loaded(
        self,
        dataset_name: str,
    ) -> None:
        self._start_time = datetime.now()
        dataset_log = DatasetLog(
            dataset_name=dataset_name,
            operation=self.LOAD_OPERATION,
        )
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=None,
            stage=_DATASET_STAGE,
            step=_BEFORE_STEP,
            datetime=str(self._end_time),
        )
        self._create_log_instance_and_send_to_logger(dataset_log, execution_log)

    @hook_impl
    def after_dataset_loaded(
        self,
        dataset_name: str,
    ) -> None:
        self._end_time = datetime.now()
        duration = (self._end_time - self._start_time).total_seconds()
        dataset_log = DatasetLog(
            dataset_name=dataset_name,
            operation=self.LOAD_OPERATION,
        )
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=None,
            stage=_DATASET_STAGE,
            step=_AFTER_STEP,
            datetime=str(self._end_time),
            duration=float(duration),
        )
        self._create_log_instance_and_send_to_logger(dataset_log, execution_log)

    @hook_impl
    def before_dataset_saved(
        self,
        dataset_name: str,
    ) -> None:
        self._start_time = datetime.now()
        dataset_log = DatasetLog(
            dataset_name=dataset_name,
            operation=self.SAVE_OPERATION,
        )
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=None,
            stage=_DATASET_STAGE,
            step=_BEFORE_STEP,
            datetime=str(self._end_time),
        )
        self._create_log_instance_and_send_to_logger(dataset_log, execution_log)

    @hook_impl
    def after_dataset_save(
        self,
        dataset_name: str,
    ) -> None:
        self._end_time = datetime.now()
        duration = (self._end_time - self._start_time).total_seconds()
        dataset_log = DatasetLog(
            dataset_name=dataset_name,
            operation=self.SAVE_OPERATION,
        )
        execution_log = self._factory_execution_log(
            environment=ENVIORNMENT,
            task_id=None,
            stage=_DATASET_STAGE,
            step=_AFTER_STEP,
            datetime=str(self._end_time),
            duration=float(duration),
        )
        self._create_log_instance_and_send_to_logger(dataset_log, execution_log)
