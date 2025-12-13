from __future__ import annotations

import json
import zipfile

from typing import Dict, Any

from Utils import tuplize_version, Version

try:
    from worlds.Files import APWorldContainer
except ImportError:
    from ._vendor.world_container import APWorldContainer


LITERAL_KEYS = ("github", "authors", "world_version_full", "tracker", "flags")

class RepoWorldContainer(APWorldContainer):
    """A zipfile containing a world implementation."""
    github: str | None = None

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        try:
            manifest = super().read_contents(opened_zipfile)
        except KeyError:
            manifest = self.read_incorrect_contents(opened_zipfile)
        if 'poptracker' in manifest:
            manifest['tracker'] = manifest.pop('poptracker')
            del manifest['poptracker']
        for lit_key in LITERAL_KEYS:
            if lit_key in manifest:
                setattr(self, lit_key, manifest[lit_key])
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        for lit_key in LITERAL_KEYS:
            value = getattr(self, lit_key, None)
            if value is not None:
                manifest[lit_key] = value
        return manifest

    def read_incorrect_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        """Read contents of the zipfile from an archipelago.json file in the subdirectory."""
        # This isn't needed as of v7, but is currently kept for backwards compatibility with older installs.
        manifest = {}
        for file in opened_zipfile.namelist():
            if file.endswith("archipelago.json"):
                with opened_zipfile.open(file) as f:
                    contents = f.read()
                manifest = json.loads(contents)
        for string_key in ("game",):
            if string_key in manifest:
                setattr(self, string_key, manifest[string_key])

        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            if version_key in manifest:
                setattr(self, version_key, Version(*tuplize_version(manifest[version_key])))

        return manifest
