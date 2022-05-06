"""
    About: Module with FastAPI starting & initialization utilities
    Author: Adil Rashitov <adil@wastelabs.co>
"""
import os
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Union


import anyconfig


_PYPROJECT = "pyproject.toml"
_ENDPOINTS_LOC = "/src/backend/endpoints"
_NOTEBOOK_LOC = "/notebooks"


class ProjectMetadata(NamedTuple):
    """Structure holding project metadata derived from `pyproject.toml`"""

    title: str
    version: str
    description: str


def _get_pyproject_toml_file(project_path: Path) -> Path:
    """Makes sure presence pyproject toml file

    Args:
    project_path (Path): full path to project

    Returns:
    (Path): full path to toml file
    """
    pyproject_toml = project_path / _PYPROJECT
    if not pyproject_toml.is_file():
        raise RuntimeError(
            f"Could not find the project configuration file '{_PYPROJECT}' in {project_path}. ",
        )
    return pyproject_toml


def _load_application_metadata(pyproject_toml: Path) -> Dict[str, Any]:
    """Loads application metadata

    Args:
        project_path (Path): full path to project

    Raises:
        RuntimeError: if can't read

    Returns:
        Dict[str, Any]: _description_
    """
    try:
        metadata_dict = anyconfig.load(pyproject_toml)
    except Exception as exc:
        raise RuntimeError(f"Failed to parse '{_PYPROJECT}' file.") from exc
    return metadata_dict


def _get_app_metadata(pyproect_content: Dict[str, Any]) -> Dict[str, str]:
    """Extracts application metadata

    Args:
        pyproect_content (Dict[str, Any]): source newly readed config

    Raises:
        RuntimeError: if does't find [app.metadata]' section in pyproject.toml

    Returns:
        Dict[str, str]: application metadata form pyproject.toml
    """
    try:
        metadata_dict = pyproect_content["app"]["metadata"]
    except KeyError as exc:
        raise RuntimeError(
            f"There's no '[app.metadata]' section in the '{_PYPROJECT}'. "
            f"Please add '[app.metadata]' section to the file with appropriate "
            f"configuration parameters.",
        ) from exc
    try:
        metadata_dict = {
            **metadata_dict,
            **pyproect_content["tool"]["commitizen"],
        }
    except KeyError as exc:
        raise RuntimeError(
            f"There's no '[tool.commitizen]' section in the '{_PYPROJECT}'. "
            f"Please add '[tool.commitizen]' section to the file with appropriate "
            f"configuration parameters.",
        ) from exc
    return metadata_dict


def _check_mandatory_keys(metadata_dict: Dict[str, str], mandatory_keys: List[str]):
    """checks presence of mandatory keys

    Args:
    metadata_dict (Dict[str, str]): metadata config
    mandatory_keys (List[str]): list of mandatory keys

    Raises:
    RuntimeError: if one of the mandatory key is missing
    """
    missing_keys = [key for key in mandatory_keys if key not in metadata_dict]
    if missing_keys:
        raise RuntimeError(f"Missing required keys {missing_keys} from '{_PYPROJECT}'.")


def _initilize_project_metadata(
    metadata_dict: Dict[str, str],
    mandatory_keys: List[str],
) -> ProjectMetadata:
    """Performs initialization of application project metadata object

    Args:
    metadata_dict (Dict[str, str]): arguments for ProjectMetadata object
    mandatory_keys (List[str]): _description_

    Raises:
        RuntimeError: if redundant parameters are provided

    Returns:
    ProjectMetadata: Application metadata object
    """
    try:
        return ProjectMetadata(**metadata_dict)
    except TypeError as exc:
        raise RuntimeError(
            f"Found unexpected keys in '{_PYPROJECT}'. Make sure "
            f"it only contains the following keys: {mandatory_keys}.",
        ) from exc


def _ensure_parent_notebooks_dir(project_path: Path) -> Path:
    project_path = str(project_path).replace(_NOTEBOOK_LOC, "")
    return Path(project_path)


def _get_project_metadata(project_path: Union[str, Path]) -> ProjectMetadata:
    """Read project metadata from `<project_path>/pyproject.toml` config file,
    under the `[app.metadata]` section.
    Args:
        project_path: Local path to project root
            directory to look up `pyproject.toml` in.
    Raises:
        RuntimeError: `pyproject.toml` was not
            found or the `[app.metadata]` section
            is missing, or config file cannot be parsed.
    Returns:
        A named tuple that contains project metadata.
    """
    project_path = Path(project_path).expanduser().resolve()
    project_path = _ensure_parent_notebooks_dir(project_path)

    pyproject_toml = _get_pyproject_toml_file(project_path)
    metadata_dict = _load_application_metadata(pyproject_toml)
    metadata_dict = _get_app_metadata(metadata_dict)

    mandatory_keys = ["title", "version", "description"]
    _check_mandatory_keys(metadata_dict, mandatory_keys)
    return _initilize_project_metadata(metadata_dict, mandatory_keys)


def get_endpoint_route(endpoint_path: str) -> str:
    """Function extracts from endpoint.py filename route location

    Args:
        endpoint_path (str): endpoint path

    Returns:
        str: route name
    """
    # 1. Resolve full filepath & endpoint path
    project_path = str(Path().resolve())
    endpoints_path = project_path + _ENDPOINTS_LOC

    # 2. Route naming extraction
    route = str(Path(os.path.realpath(endpoint_path)))
    route = route.split(endpoints_path)[1]
    route = route.rsplit("/", 1)[0]

    return route


def get_endpoint_tag(endpoint_path: str) -> str:
    """Function performs extraction of tag based on route name

    Args:
        endpoint_path (str): endpoint path

    Returns:
        str: Endpoint tag
    """
    route = get_endpoint_route(endpoint_path)
    return route.split("/")[0]


metadata = _get_project_metadata(Path.cwd())
