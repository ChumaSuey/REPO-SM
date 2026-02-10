import os
import shutil
import pathlib
import json
import sys
import logging
import parser

# Terminology:
# REPO backups (or Steam backups) = The actual game save folder managed by Steam/Game.
# Local backups = The backups managed by this script in "REPO Local backup".

DEFAULT_LOCAL_BACKUP_FOLDER = "REPO Local backup"
CONFIG_FILE = "config.json"
LOG_FILE = "app.log"

def setup_logging():
    """Configures logging to file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(get_base_path() / LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_base_path():
    """
    Returns the base path of the application.
    If frozen (exe), returns the directory of the executable.
    If script, returns the directory of the script.
    """
    if getattr(sys, 'frozen', False):
        return pathlib.Path(os.path.dirname(sys.executable))
    else:
        return pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

def get_config_path():
    """Returns the path to the config file in the base directory."""
    return get_base_path() / CONFIG_FILE

def load_config():
    """Loads the configuration from config.json."""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
    return {}

def save_config(config):
    """Saves the configuration to config.json."""
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving config: {e}")

def get_local_backup_path():
    """
    Returns the absolute path to the local backup folder.
    Reads from config if available, otherwise uses default.
    Creates the folder if it does not exist.
    """
    config = load_config()
    custom_path = config.get("local_backup_path")
    
    if custom_path:
        backup_path = pathlib.Path(custom_path)
    else:
        # Use base path (exe or script dir)
        backup_path = get_base_path() / DEFAULT_LOCAL_BACKUP_FOLDER
    
    if not backup_path.exists():
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating backup directory at {backup_path}: {e}")
            # Fallback to default if custom fails? For now just return it and let caller handle error
        
    return backup_path

def set_local_backup_path(new_path):
    """
    Sets the custom local backup path in the configuration.
    Args:
        new_path (str or pathlib.Path): The new path for backups.
    """
    config = load_config()
    config["local_backup_path"] = str(new_path)
    save_config(config)
    logging.info(f"Local backup path set to: {new_path}")

def total_backup(backup_name):
    """
    Backs up the current R.E.P.O saves to the local backup folder under the given name.
    Returns True if successful, False otherwise.
    """
    source_path = parser.get_save_path()
    if not source_path:
        logging.error("Error: Could not locate R.E.P.O save folder.")
        return False
    
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

def restore_saves(backup_name):
    """
    Restores a specific backup from the local backup folder to the R.E.P.O save location.
    Returns True if successful, False otherwise.
    """
    backup_path = get_local_backup_path() / backup_name
    
    if not backup_path.exists():
        logging.error(f"Error: Backup '{backup_name}' not found.")
        return False
        
    target_path = parser.get_save_path()
    
    if not target_path:
        # Try to construct it manually if get_save_path fails (e.g. folder deleted)
        user_home = pathlib.Path(os.path.expanduser("~"))
        target_path = user_home / parser.SAVE_PATH_SUFFIX
    
    temp_backup_path = None
    
    # --- SAFE RESTORE MECHANISM ---
    try:
        if target_path.exists():
            # Create a temporary backup of the current state before wiping it
            temp_backup_path = target_path.parent / (target_path.name + "_TEMP_RESTORE_BACKUP")
            if temp_backup_path.exists():
                shutil.rmtree(temp_backup_path)
            shutil.copytree(target_path, temp_backup_path)
            
            shutil.rmtree(target_path)
            
        shutil.copytree(backup_path, target_path)
        
        # If successful, remove the temp backup
        if temp_backup_path and temp_backup_path.exists():
            shutil.rmtree(temp_backup_path)
            
        logging.info(f"Successfully restored saves from '{backup_name}'")
        return True
        
    except Exception as e:
        logging.critical(f"CRITICAL ERROR during restore: {e}")
        # Attempt to rollback from temp backup
        if temp_backup_path and temp_backup_path.exists():
            logging.info("Attempting to rollback changes...")
            if target_path.exists():
                 shutil.rmtree(target_path)
            try:
                shutil.copytree(temp_backup_path, target_path)
                logging.info("Rollback successful. Original state restored.")
                shutil.rmtree(temp_backup_path)
            except Exception as rollback_error:
                logging.critical(f"FATAL: Rollback failed! Original saves may be in {temp_backup_path}. Error: {rollback_error}")
        
        return False

def set_backup_state(target_path, active: bool):
    """
    Toggles the state of a backup folder by adding or removing the '_backup' suffix.
    
    Args:
        target_path (pathlib.Path or str): The path to the folder.
        active (bool): 
            If True, ensures the folder does NOT have '_backup' suffix (Enabled).
            If False, ensures the folder HAS '_backup' suffix (Disabled).
            
    Returns:
        pathlib.Path: The new path of the folder.
    """
    target_path = pathlib.Path(target_path)
    
    if not target_path.exists():
        logging.error(f"Error: Path '{target_path}' does not exist.")
        return target_path

    name = target_path.name
    parent = target_path.parent
    
    if active:
        # We want it ACTIVE, so REMOVE "_backup" if present
        if name.endswith("_backup"):
            new_name = name[:-7] # Remove last 7 chars "_backup"
            new_path = parent / new_name
            target_path.rename(new_path)
            logging.info(f"State set to ACTIVE: Renamed '{name}' to '{new_name}'")
            return new_path
        else:
            logging.info(f"State is already ACTIVE: '{name}'")
            return target_path
    else:
        # We want it INACTIVE (Backup), so ADD "_backup" if NOT present
        if not name.endswith("_backup"):
            new_name = f"{name}_backup"
            new_path = parent / new_name
            target_path.rename(new_path)
            logging.info(f"State set to BACKUP (Disabled): Renamed '{name}' to '{new_name}'")
            return new_path
        else:
            logging.info(f"State is already BACKUP: '{name}'")
            return target_path

if __name__ == "__main__":
    setup_logging()
    # Simple manual test interaction
    logging.info(f"Local backup path: {get_local_backup_path()}")
