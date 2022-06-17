"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html."""

import logging
import sys
from pathlib import Path

from kedro.extras.extensions.ipython import _find_kedro_project

PIPELINE_LOGGER_NAME = "pipeline"
HOOKS = ()


def expand_project_path() -> str:
    """Function performs extraction of kedro context using built-in tools

    Args:
        env (str): input environment

    Returns:
        KedroContext: Generated kedro context
    """
    # 1. Bootstrapping project to find main path
    startup_path = Path.cwd()
    project_path = _find_kedro_project(startup_path)
    sys.path.append(str(project_path))


# if hooks.ENVIORNMENT.lower() == "test":
#     logging.warn("Kedro profiling hooks are activated")
#     HOOKS = (
#         hooks.NodeLoggingHooks(),
#         hooks.DatasetLoggingHooks(),
#         hooks.PipelineLoggingHooks(),
#     )


def get_logger():
    logger = logging.getLogger(PIPELINE_LOGGER_NAME)
    return logger


# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import ShelveStore
# SESSION_STORE_CLASS = ShelveStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.
# from kedro.config import TemplatedConfigLoader
# CONFIG_LOADER_CLASS = TemplatedConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
# CONFIG_LOADER_ARGS = {
#     "globals_pattern": "*globals.yml",
# }

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
