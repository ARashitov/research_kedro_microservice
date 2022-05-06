import sys
import traceback

from fastapi import HTTPException


_TRACEBACK_RESPONSE_NO = 2
_TRACEBACK_LIMIT = 30


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


def get_http_exception(status_code: int, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "traceback": _get_traceback(),
        },
    )
