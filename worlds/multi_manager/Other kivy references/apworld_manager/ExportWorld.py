
# TODO: handle data
# TODO: handle clients
# TODO: handle yaml templates
import argparse
import json
import os.path
import platform
import sys
import zipfile
from pathlib import Path
import Utils

if __name__ == "__main__":
    ap_root = os.path.normpath(os.path.dirname(Utils.__file__))
    os.chdir(ap_root)
    sys.path.append(ap_root)

from worlds.AutoWorld import AutoWorldRegister, World

METADATA_KEYS = [
    "game",
    "world_version",
    "minimum_ap_version",
    "maximum_ap_version",
    # license
    # description
    # maintainers
]

def create_world_meta(world_key, world_type, is_frozen):
    metadata = {}
    metadata["compatible_version"] = 6
    for key in METADATA_KEYS:
        if hasattr(world_type, key):
            metadata[key] = getattr(world_type, key)
    if world_type.__doc__ != World.__doc__ and world_type.__doc__ is not None:
        metadata["description"] = world_type.__doc__.strip()
    metadata["id"] = world_key
    metadata["frozen"] = is_frozen
    if is_frozen:
        metadata["arch"] = platform.machine()
        metadata["os"] = platform.system() # TODO: linux
        metadata["pyversion"] = f"{sys.version_info[0]}.{sys.version_info[1]}"
    else:
        metadata["arch"] = "any"
        metadata["os"] = "any"
        metadata["pyversion"] = "any"
    return metadata

def export_world(libfolder, world_type, output_dir, is_frozen):
    world_key = os.path.split(os.path.dirname(world_type.__file__))[1]
    world_directory = libfolder / "worlds" / world_key

    metadata = create_world_meta(world_key, world_type, is_frozen)

    arch = metadata["arch"]
    os_type = metadata["os"]
    if arch == "any" and os_type == "any" and metadata["pyversion"] == "any":
        base_file_name = f"{world_key}-{metadata['world_version']}"
    else:
        base_file_name = f"{world_key}-{arch}-{os_type}-py{metadata['pyversion']}-{metadata['world_version']}"
    world_file_name = f"{base_file_name}.apworld"

    output_name = output_dir / world_file_name
    with zipfile.ZipFile(output_name, "x", zipfile.ZIP_DEFLATED,
                            compresslevel=9) as zf:
        for path in world_directory.rglob("*.*"):
            relative_path = os.path.join(*path.parts[path.parts.index("worlds")+1:])
            if '__pycache__' in path.parts:
                continue
            zf.write(path, relative_path)
        zf.writestr("archipelago.json", json.dumps(metadata, indent=4))
    return output_name

if __name__ == "__main__":
    ap_root_path = Path(ap_root)

    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("world_name", help="World to be exported.", type=str)
    parser.add_argument("output_dir", help="Export directory.", type=Path, default=ap_root_path / "custom_worlds", nargs='?')
    args = parser.parse_args()

    output = export_world(ap_root_path, AutoWorldRegister.world_types[args.world_name], args.output_dir, is_frozen=False)
    print(f"Output to {output}")
