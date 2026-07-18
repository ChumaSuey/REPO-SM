# R.E.P.O Save Manager Documentation

## Project Overview

The **R.E.P.O Save Manager** is a Python-based utility designed to help players of the game *R.E.P.O* manage their save files. It provides a user-friendly Graphical User Interface (GUI) to backup, restore, and organize save states, ensuring you never lose progress or can easily switch between different save points.

## Features

- **Live Save Monitoring**: Automatically detects and lists the current save files in the game's directory.
- **Local Backup Management**: Create unlimited local backups of your saves.
- **One-Click Backup & Restore**: Easily copy saves from the game to your local storage and vice-versa.
- **Safe Restore with Rollback**: Uses a staging-directory + atomic rename strategy. If anything fails during restore, the original state is recovered automatically.
- **Recycle Bin**: Deleted backups move to an in-app `Recycle Bin/` folder. Restore them or permanently delete later.
- **Rename Backups**: Change backup folder names without leaving the app.
- **Save State Toggling**: Toggle backups between "Active" and "Disabled" states (configurable suffix, default `_backup`).
- **Custom Backup Location**: Choose where to store your local backups.
- **Settings Dialog** (⚙): Configure the backup suffix and local folder path in one place.
- **Open Saves / Open Local**: Quick buttons to open the REPO save folder or your backup folder in File Explorer.
- **Context Menus**: Right-click on any backup or REPO file for quick actions.
- **Keyboard Shortcuts**: `F5` to refresh, `Delete` to delete selected backup.
- **Cross-Platform**: Detects save paths on Windows, macOS, Linux (native), and Linux (Steam Proton/Steam Deck).
- **High-DPI Aware**: Crisp rendering on 4K/high-DPI displays on Windows.
- **Responsive UI**: Backup, restore, and delete operations run in background threads so the interface never freezes.
- **Detailed Logging**: Logs application events and errors to `app.log` for easier troubleshooting.
- **Dark Mode UI**: A modern, dark-themed interface using `sv_ttk`.

## Installation & Requirements

### Prerequisites

- **Python 3.x**: Ensure you have Python installed on your system.
- **Dependencies**:
  - `tkinter` (usually comes with Python)
  - `sv_ttk` (for the theme)

### Installation

1. **Clone or Download** the repository to your local machine.
2. **Install Dependencies**:
   Open a terminal in the project folder and run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage Guide

### Running the Application

1. Navigate to the project directory.
2. Run the main script:

   ```bash
   python main.py
   ```

### Interface Overview

- **Left Panel (Steam/REPO Folder)**: Shows the current files in your actual game save directory.
- **Right Panel (Local Backups / Recycle Bin)**: Displays your stored backups, or deleted items when Recycle view is active.

### Button Reference

| Button | Description |
|---|---|
| **Refresh** | Reloads both folder views. |
| **Backup** | Prompts for a name and saves the current game state to your local backups. |
| **Restore** | Overwrites the current game save with the selected local backup. **Warning: This action is irreversible.** In Recycle Bin mode, restores the item back to the active list. |
| **Toggle** | Adds or removes the configured suffix (default `_backup`) to enable/disable a backup. |
| **Rename** | Prompts for a new name and renames the selected backup folder. |
| **Delete** | Moves the selected backup to the Recycle Bin. In Recycle Bin mode, permanently deletes. |
| **🗑 Recycle Bin** | Toggles between normal backup view and the Recycle Bin. In Recycle mode, some buttons are disabled and behavior changes. |
| **Open Saves** | Opens the REPO save folder in your OS file manager. |
| **Open Local** | Opens the local backup folder (or Recycle Bin) in your OS file manager. |
| **⚙ Settings** | Opens a dialog to configure the backup suffix and local backup folder path. |

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `F5` | Refresh lists |
| `Delete` | Delete selected backup (or permanently delete in Recycle Bin) |

### Right-Click Menus

**Local Backups (normal mode):** Restore, Toggle State, Rename, Delete
**Local Backups (Recycle Bin mode):** Restore, Delete Forever
**REPO Files:** Open in Explorer

## Project Structure

- **`main.py`**: Application entry point. Sets up DPI awareness, logging, and launches the GUI.
- **`GUI.py`**: The Tkinter GUI logic, event handlers, and modal dialogs.
- **`manager.py`**: Core logic for file operations (backup, restore, rename, recycle, delete) and configuration management.
- **`parser.py`**: Cross-platform utility to locate the R.E.P.O save directory (Windows/macOS/Linux/Proton).
- **`requirements.txt`**: Python dependencies list.

## Troubleshooting

- **"REPO Folder Not Found"**: Ensure the game is installed and has been run at least once to generate the save directory.
- **Check Logs**: If you encounter issues, check the `app.log` file in the application directory for detailed error messages.
- **Permission Errors**: Try running the script as Administrator if you encounter issues accessing the save folders.
