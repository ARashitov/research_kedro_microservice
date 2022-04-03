"""
    About: Module with pytest fixtures required over all project components
    Author: Adil Rashitov
"""
from pathlib import Path
from kedro.extras.extensions.ipython import _find_kedro_project
from kedro.framework.context.context import KedroContext
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
import pytest


ENVIRONMENT = "test"


@pytest.fixture
def context() -> KedroContext:
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
    session = KedroSession.create(metadata.package_name, project_path, extra_params=extra_params, env=ENVIRONMENT)
    _context = session.load_context()

    return _context
