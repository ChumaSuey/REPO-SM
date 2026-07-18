import os
import pathlib
import sys
from typing import List, Optional

_SAVE_PATH_SUFFIX = pathlib.PureWindowsPath("AppData/LocalLow/semiwork/Repo/saves")

def _get_windows_path() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser("~")) / _SAVE_PATH_SUFFIX

def _get_macos_paths() -> List[pathlib.Path]:
    home = pathlib.Path(os.path.expanduser("~"))
    return [
        home / "Library/Application Support/semiwork/Repo",
    ]

def _get_linux_native_path() -> pathlib.Path:
    return pathlib.Path(os.path.expanduser("~")) / ".config/unity3d/semiwork/Repo"

def _get_proton_steam_roots() -> List[pathlib.Path]:
    home = pathlib.Path(os.path.expanduser("~"))
    candidates = [
        home / ".steam/steam",
        home / ".var/app/com.valvesoftware.Steam/.steam/steam",
        home / ".local/share/Steam",
        home / "snap/steam/common/.local/share/Steam",
    ]
    return [c for c in candidates if c.exists()]

def _scan_proton_prefixes() -> List[pathlib.Path]:
    found: List[pathlib.Path] = []
    for steam_root in _get_proton_steam_roots():
        compatdata = steam_root / "steamapps/compatdata"
        if not compatdata.exists():
            continue
        for app_dir in sorted(compatdata.iterdir()):
            if not app_dir.is_dir():
                continue
            candidate = app_dir / "pfx" / "drive_c/users/steamuser/AppData/LocalLow/semiwork/Repo/saves"
            if candidate.exists():
                found.append(candidate)
    return found

def get_save_path() -> Optional[pathlib.Path]:
    if sys.platform == "win32":
        candidates = [_get_windows_path()]
    elif sys.platform == "darwin":
        candidates = _get_macos_paths()
    else:
        candidates = [_get_linux_native_path()] + _scan_proton_prefixes()

    for path in candidates:
        if path.exists() and path.is_dir():
            return path
    return None

def get_default_save_path() -> pathlib.Path:
    """Returns the expected save path for the current platform, even if it doesn't exist."""
    if sys.platform == "win32":
        return _get_windows_path()
    elif sys.platform == "darwin":
        return _get_macos_paths()[0]
    else:
        return _get_linux_native_path()
