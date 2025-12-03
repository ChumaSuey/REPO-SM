# R.E.P.O Save Manager Documentation

## Project Overview
The **R.E.P.O Save Manager** is a Python-based utility designed to help players of the game *R.E.P.O* manage their save files. It provides a user-friendly Graphical User Interface (GUI) to backup, restore, and organize save states, ensuring you never lose progress or can easily switch between different save points.

## Features
- **Live Save Monitoring**: Automatically detects and lists the current save files in the game's directory.
- **Local Backup Management**: Create unlimited local backups of your saves.
- **One-Click Backup & Restore**: Easily copy saves from the game to your local storage and vice-versa.
- **Save State Toggling**: Toggle backups between "Active" and "Disabled" states to organize your list.
- **Custom Backup Location**: Choose where you want to store your local backups.
- **Dark Mode UI**: A modern, dark-themed interface using `sv_ttk`.

## Installation & Requirements

### Prerequisites
- **Python 3.x**: Ensure you have Python installed on your system.
- **Dependencies**: The project relies on the following Python packages:
    - `tkinter` (usually comes with Python)
    - `sv_ttk` (for the theme)

### Installation
1. **Clone or Download** the repository to your local machine.
2. **Install Dependencies**:
   Open a terminal in the project folder and run:
   ```bash
   pip install sv_ttk
   ```
   *(Note: If you have a `requirements.txt`, use `pip install -r requirements.txt`)*

## Usage Guide

### Running the Application
1. Navigate to the project directory.
2. Run the main script:
   ```bash
   python GUI.py
   ```

### Interface Overview
- **Left Panel (Steam/REPO Folder)**: Shows the current files in your actual game save directory.
- **Right Panel (Local Backups)**: Displays your stored backups.
- **Buttons**:
    - **Refresh Lists**: Reloads the view of both folders.
    - **Backup (REPO -> Local)**: Prompts for a name and saves the current game state to your local backups.
    - **Restore (Local -> REPO)**: Overwrites the current game save with the selected local backup. **Warning: This action is irreversible.**
    - **Toggle State**: Renames a backup with a `_backup` suffix to "disable" it, or removes the suffix to "enable" it.
    - **Change Local**: Allows you to select a different folder for storing backups.

## Project Structure
- **`GUI.py`**: The main entry point. Contains the Tkinter GUI logic and event handlers.
- **`Manager.py`**: Handles the core logic for file operations (copying, deleting, renaming) and configuration management.
- **`parser.py`**: Utility script to locate the default R.E.P.O save directory on Windows.
- **`REPO-SM.spec`**: PyInstaller specification file for building the executable.

## Troubleshooting
- **"REPO Folder Not Found"**: Ensure the game is installed and has been run at least once to generate the save directory.
- **Permission Errors**: Try running the script as Administrator if you encounter issues accessing the save folders.
