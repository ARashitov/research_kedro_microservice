import sys
import traceback
from typing import Any, Dict

from fastapi import HTTPException, status
from kedro.framework.session import KedroSession
from kedro.io.core import AbstractDataSet
from kedro.runner import SequentialRunner


_TRACEBACK_RESPONSE_NO = 2
_TRACEBACK_LIMIT = 30
_RUNNER = SequentialRunner(is_async=True)


def _get_traceback() -> str:
    """
    Performs generation of exception message as string

    Returns:
    str: exception message content
    """
    tb_content = sys.exc_info()[_TRACEBACK_RESPONSE_NO]
    tb_content = traceback.format_tb(tb_content, limit=_TRACEBACK_LIMIT)
    tb_content = "\n".join(tb_content)
    return tb_content


def get_http_exception(status_code: int, message: str, traceback: str = None) -> HTTPException:
    if traceback is None:
        traceback = _get_traceback()
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "traceback": traceback,
        },
    )


def excecute_pipeline(
    session: KedroSession,
    pipeline_name: str,
    catalog_extensions: Dict[str, AbstractDataSet],
) -> Dict[str, Any]:
    try:
        result = session.run(
            pipeline_name=pipeline_name,
            runner=_RUNNER,
            extend_catalog=catalog_extensions,
        )
        return result
    except Exception as kedro_exc:
        raise get_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(kedro_exc),
            traceback=_get_traceback(),
        )
