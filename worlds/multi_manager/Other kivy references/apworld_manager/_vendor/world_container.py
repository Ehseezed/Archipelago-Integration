from __future__ import annotations

import json
import zipfile
import os
import threading

from typing import (ClassVar, Dict, Any, Optional, Union, BinaryIO, TYPE_CHECKING)


semaphore = threading.Semaphore(os.cpu_count() or 4)

del threading
del os

if TYPE_CHECKING:
    from Utils import Version

from worlds.Files import InvalidDataError

container_version: int = 6

class APContainer:
    """A zipfile containing at least archipelago.json, which contains a manifest json payload."""
    version: ClassVar[int] = container_version
    compression_level: ClassVar[int] = 9
    compression_method: ClassVar[int] = zipfile.ZIP_DEFLATED

    path: Optional[str]

    def __init__(self, path: Optional[str] = None):
        self.path = path

    def write(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot write {self.__class__.__name__} due to no path provided.")
        with semaphore:  # TODO: remove semaphore once generate_output has a thread limit
            with zipfile.ZipFile(
                    zip_file, "w", self.compression_method, True, self.compression_level) as zf:
                if file:
                    self.path = zf.filename
                self.write_contents(zf)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        manifest = self.get_manifest()
        try:
            manifest_str = json.dumps(manifest)
        except Exception as e:
            raise Exception(f"Manifest {manifest} did not convert to json.") from e
        else:
            opened_zipfile.writestr("archipelago.json", manifest_str)

    def read(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        """Read data into patch object. file can be file-like, such as an outer zip file's stream."""
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot read {self.__class__.__name__} due to no path provided.")
        with zipfile.ZipFile(zip_file, "r") as zf:
            if file:
                self.path = zf.filename
            try:
                self.read_contents(zf)
            except Exception as e:
                message = ""
                if len(e.args):
                    arg0 = e.args[0]
                    if isinstance(arg0, str):
                        message = f"{arg0} - "
                raise InvalidDataError(f"{message}This might be the incorrect world version for this file") from e

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        with opened_zipfile.open("archipelago.json", "r") as f:
            manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        return {
            # minimum version of patch system expected for patching to be successful
            "compatible_version": 5,
            "version": container_version,
        }


class APWorldContainer(APContainer):
    """A zipfile containing a world implementation."""
    game: str | None = None
    world_version: "Version | None" = None
    minimum_ap_version: "Version | None" = None
    maximum_ap_version: "Version | None" = None

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        from Utils import tuplize_version, Version
        manifest = super().read_contents(opened_zipfile)
        self.game = manifest["game"]
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            if version_key in manifest:
                setattr(self, version_key, Version(*tuplize_version(manifest[version_key])))
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest["game"] = self.game
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            version = getattr(self, version_key)
            if version:
                manifest[version_key] = version.as_simple_string()
        return manifest
