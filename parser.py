import os
import pathlib

# The standard path suffix for R.E.P.O saves on Windows
SAVE_PATH_SUFFIX = r"AppData\LocalLow\semiwork\Repo\saves"

def get_save_path():
    """
    Locates the R.E.P.O save directory.
    Returns the Path object if found, otherwise None.
    """
    user_home = pathlib.Path(os.path.expanduser("~"))
    save_path = user_home / SAVE_PATH_SUFFIX

    if save_path.exists() and save_path.is_dir():
        return save_path
    else:
        print(f"Warning: R.E.P.O save folder not found at {save_path}")
        return None

if __name__ == "__main__":
    path = get_save_path()
    if path:
        print(f"Save path found: {path}")
