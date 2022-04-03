"""
    About: module for jupyter notebooks initilizing kedro environmnets
    Author: Adil Rashitov
"""
# 1. Initialization kedro session
from pathlib import Path
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from kedro.extras.extensions.ipython import _find_kedro_project
from kedro.framework.context.context import KedroContext


KEDRO_CONTEXT_ENVS = ["dev", "test", "ua_test", "prod"]


def get_kedro_context(env: str) -> KedroContext:
    """Function performs extraction of kedro context using built-in tools

    Args:
        env (str): input environment

    Returns:
        KedroContext: Generated kedro context
    """
    # 1. Bootstrapping project to find main path
    startup_path = Path.cwd()
    project_path = _find_kedro_project(startup_path)
    metadata = bootstrap_project(project_path)
    extra_params = None

    # 2. Initlize session & create context
    session = KedroSession.create(
        metadata.package_name,
        project_path,
        extra_params=extra_params,
        env=env,
    )
    context = session.load_context()

    return context



dev = get_kedro_context(KEDRO_CONTEXT_ENVS[0])
test = get_kedro_context(KEDRO_CONTEXT_ENVS[1])
ua_test = get_kedro_context(KEDRO_CONTEXT_ENVS[2])
prod = get_kedro_context(KEDRO_CONTEXT_ENVS[3])
