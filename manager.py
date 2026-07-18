import json
import logging
import os
import pathlib
import re
import shutil
import sys
from typing import Optional, Union

import parser

DEFAULT_LOCAL_BACKUP_FOLDER = "REPO Local backup"
CONFIG_FILE = "config.json"
LOG_FILE = "app.log"
DEFAULT_SUFFIX = "_backup"
RECYCLE_BIN_FOLDER = "Recycle Bin"

def _sanitize_backup_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"^\.+", "", name)
    if not name:
        name = "backup"
    return name

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(get_base_path() / LOG_FILE),
            logging.StreamHandler(sys.stdout),
        ],
    )

def get_base_path() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        return pathlib.Path(os.path.dirname(sys.executable))
    return pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

def get_config_path() -> pathlib.Path:
    return get_base_path() / CONFIG_FILE

def load_config() -> dict:
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
    return {}

def save_config(config: dict) -> None:
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving config: {e}")

def get_backup_suffix() -> str:
    config = load_config()
    suffix = config.get("backup_suffix", DEFAULT_SUFFIX)
    if not suffix:
        suffix = DEFAULT_SUFFIX
    return suffix

def set_backup_suffix(new_suffix: str) -> None:
    config = load_config()
    config["backup_suffix"] = new_suffix.strip() or DEFAULT_SUFFIX
    save_config(config)
    logging.info(f"Backup suffix set to: '{config['backup_suffix']}'")

def get_local_backup_path() -> pathlib.Path:
    config = load_config()
    custom_path = config.get("local_backup_path")

    if custom_path:
        backup_path = pathlib.Path(custom_path)
    else:
        backup_path = get_base_path() / DEFAULT_LOCAL_BACKUP_FOLDER

    if not backup_path.exists():
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating backup directory at {backup_path}: {e}")

    return backup_path

def set_local_backup_path(new_path: Union[str, pathlib.Path]) -> None:
    config = load_config()
    config["local_backup_path"] = str(new_path)
    save_config(config)
    logging.info(f"Local backup path set to: {new_path}")

def get_recycle_path() -> pathlib.Path:
    path = get_local_backup_path() / RECYCLE_BIN_FOLDER
    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating recycle bin directory: {e}")
    return path

def move_to_recycle(backup_name: str) -> bool:
    local = get_local_backup_path()
    src = local / backup_name
    recycle = get_recycle_path()

    if backup_name == RECYCLE_BIN_FOLDER:
        logging.error("Error: Cannot delete the Recycle Bin itself.")
        return False

    if not src.exists():
        logging.error(f"Error: Backup '{backup_name}' not found.")
        return False

    dst = recycle / backup_name
    counter = 1
    while dst.exists():
        dst = recycle / f"{backup_name}_{counter}"
        counter += 1

    try:
        src.rename(dst)
        logging.info(f"Moved '{backup_name}' to recycle bin.")
        return True
    except Exception as e:
        logging.error(f"Error moving to recycle: {e}")
        try:
            shutil.rmtree(src)
            logging.info(f"Backup '{backup_name}' permanently deleted (fallback).")
            return True
        except Exception as e2:
            logging.error(f"Error deleting backup: {e2}")
            return False

def restore_from_recycle(backup_name: str) -> bool:
    recycle = get_recycle_path()
    src = recycle / backup_name
    local = get_local_backup_path()

    if not src.exists():
        logging.error(f"Error: '{backup_name}' not found in recycle bin.")
        return False

    dst = local / backup_name
    counter = 1
    while dst.exists():
        dst = local / f"{backup_name}_{counter}"
        counter += 1

    try:
        src.rename(dst)
        logging.info(f"Restored '{backup_name}' from recycle bin.")
        return True
    except Exception as e:
        logging.error(f"Error restoring from recycle: {e}")
        return False

def permanently_delete(backup_name: str) -> bool:
    path = get_recycle_path() / backup_name
    if not path.exists():
        logging.error(f"Error: '{backup_name}' not found in recycle bin.")
        return False
    try:
        shutil.rmtree(path)
        logging.info(f"Permanently deleted '{backup_name}'.")
        return True
    except Exception as e:
        logging.error(f"Error permanently deleting: {e}")
        return False

def total_backup(backup_name: str) -> bool:
    source_path = parser.get_save_path()
    if not source_path:
        logging.error("Error: Could not locate R.E.P.O save folder.")
        return False

    backup_name = _sanitize_backup_name(backup_name)
    dest_path = get_local_backup_path() / backup_name

    if dest_path.exists():
        logging.warning(f"Backup '{backup_name}' already exists. Overwriting...")
        shutil.rmtree(dest_path)

    try:
        shutil.copytree(source_path, dest_path)
        logging.info(f"Successfully backed up saves to '{backup_name}'")
        return True
    except Exception as e:
        logging.error(f"Error backing up saves: {e}")
        return False

def restore_saves(backup_name: str) -> bool:
    backup_path = get_local_backup_path() / backup_name

    if not backup_path.exists():
        logging.error(f"Error: Backup '{backup_name}' not found.")
        return False

    target_path = parser.get_save_path()
    if not target_path:
        target_path = parser.get_default_save_path()

    parent = target_path.parent
    staging_path = parent / (target_path.name + "_RESTORING")
    old_path: Optional[pathlib.Path] = None

    try:
        if staging_path.exists():
            shutil.rmtree(staging_path)
        shutil.copytree(backup_path, staging_path)

        if target_path.exists():
            old_path = parent / (target_path.name + "_RESTORE_OLD")
            if old_path.exists():
                shutil.rmtree(old_path)
            target_path.rename(old_path)

        staging_path.rename(target_path)

        if old_path and old_path.exists():
            shutil.rmtree(old_path)

        logging.info(f"Successfully restored saves from '{backup_name}'")
        return True

    except Exception as e:
        logging.critical(f"CRITICAL ERROR during restore: {e}")

        if staging_path.exists():
            shutil.rmtree(staging_path)

        if old_path and old_path.exists():
            try:
                old_path.rename(target_path)
                logging.info("Rollback successful. Original state restored.")
            except Exception as rollback_err:
                logging.critical(
                    f"FATAL: Rollback failed! Original saves at {old_path}. Error: {rollback_err}"
                )

        return False

def rename_backup(old_name: str, new_name: str) -> bool:
    local_path = get_local_backup_path()
    old_path = local_path / old_name

    if not old_path.exists():
        logging.error(f"Error: Backup '{old_name}' not found.")
        return False

    new_name = _sanitize_backup_name(new_name)
    new_path = local_path / new_name

    if new_path.exists():
        logging.error(f"Error: A backup named '{new_name}' already exists.")
        return False

    try:
        old_path.rename(new_path)
        logging.info(f"Renamed '{old_name}' to '{new_name}'")
        return True
    except Exception as e:
        logging.error(f"Error renaming backup: {e}")
        return False

def set_backup_state(
    target_path: Union[str, pathlib.Path], active: bool
) -> pathlib.Path:
    target_path = pathlib.Path(target_path)
    suffix = get_backup_suffix()
    suffix_len = len(suffix)

    if not target_path.exists():
        logging.error(f"Error: Path '{target_path}' does not exist.")
        return target_path

    name = target_path.name
    parent = target_path.parent

    if active:
        if name.endswith(suffix):
            new_name = name[:-suffix_len]
            new_path = parent / new_name
            target_path.rename(new_path)
            logging.info(f"State set to ACTIVE: Renamed '{name}' to '{new_name}'")
            return new_path
        else:
            logging.info(f"State is already ACTIVE: '{name}'")
            return target_path
    else:
        if not name.endswith(suffix):
            new_name = f"{name}{suffix}"
            new_path = parent / new_name
            target_path.rename(new_path)
            logging.info(f"State set to BACKUP (Disabled): Renamed '{name}' to '{new_name}'")
            return new_path
        else:
            logging.info(f"State is already BACKUP: '{name}'")
            return target_path

if __name__ == "__main__":
    setup_logging()
    logging.info(f"Local backup path: {get_local_backup_path()}")
