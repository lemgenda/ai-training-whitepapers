"""Read-only access to the sibling repositories the audit compares against.

The docs repository sits next to the other LemGendary repositories. The
workspace root is the parent of the docs root unless the environment variable
``LEMGENDARY_WORKSPACE_ROOT`` names another directory (tests point it at a
fixture workspace).

Sources:

* ``ecosystem.json`` of the LemGendary Environment Manager: service ports and
  the project folder of each service.
* ``unified_models_v2.yaml`` of the LemGendary Model Training Suite: the model
  registry. Its folder is taken from the ``training-suite`` service in
  ``ecosystem.json``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

WORKSPACE_ENV = "LEMGENDARY_WORKSPACE_ROOT"
ECOSYSTEM_PATH = Path("lemgendary-env-manager") / "ecosystem" / "ecosystem.json"
TRAINING_SERVICE_ID = "training-suite"
TRAINING_REGISTRY_FILE = "unified_models_v2.yaml"
REGISTRY_METADATA_KEY = "_registry_metadata"


class WorkspaceError(RuntimeError):
    """A sibling source file is missing or does not have the expected shape."""


def workspace_root(docs_root: Path) -> Path:
    """The workspace root: ``LEMGENDARY_WORKSPACE_ROOT`` or the docs root's parent."""
    override = os.environ.get(WORKSPACE_ENV)
    if override:
        return Path(override).resolve()
    return docs_root.resolve().parent


@dataclass(frozen=True)
class Service:
    """One ``services[]`` entry of ``ecosystem.json``."""

    service_id: str
    project: str
    port: int


class Workspace:
    """The sibling sources, loaded lazily and cached."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def _require(self, relative: Path) -> Path:
        path = self.root / relative
        if not path.is_file():
            raise WorkspaceError(
                f"{relative.as_posix()} not found under the workspace root {self.root}. "
                f"Check out the sibling repository next to lemgendary-docs or set "
                f"{WORKSPACE_ENV} to the directory that contains it."
            )
        return path

    @cached_property
    def ecosystem(self) -> dict[str, Any]:
        """The parsed ``ecosystem.json`` of the LemGendary Environment Manager."""
        path = self._require(ECOSYSTEM_PATH)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("services"), list):
            raise WorkspaceError(f"{ECOSYSTEM_PATH.as_posix()} has no services list")
        return data

    @cached_property
    def services(self) -> dict[str, Service]:
        """Services by id."""
        return {
            entry["id"]: Service(entry["id"], entry["project"], int(entry["port"]))
            for entry in self.ecosystem["services"]
        }

    def service(self, service_id: str) -> Service:
        """The service ``service_id``; ``WorkspaceError`` when it is not listed."""
        try:
            return self.services[service_id]
        except KeyError as exc:
            raise WorkspaceError(
                f"{ECOSYSTEM_PATH.as_posix()} has no service {service_id!r}"
            ) from exc

    @property
    def training_registry_path(self) -> Path:
        """Workspace-relative path of ``unified_models_v2.yaml``."""
        return Path(self.service(TRAINING_SERVICE_ID).project) / TRAINING_REGISTRY_FILE

    @cached_property
    def training_model_ids(self) -> list[str]:
        """Model keys of the training registry, without ``_registry_metadata``."""
        relative = self.training_registry_path
        data = yaml.safe_load(self._require(relative).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise WorkspaceError(f"{relative.as_posix()} is not a mapping of models")
        return [str(key) for key in data if key != REGISTRY_METADATA_KEY]
