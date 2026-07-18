# Changelog

## V2.0

### Added
- **Cross-platform save path detection** — Windows, macOS, Linux native, Steam Proton/Deck
- **Recycle Bin** — in-app soft-delete with restore and permanent delete
- **Rename backups** directly from the UI
- **Open Saves / Open Local** buttons to quickly open folders in File Explorer
- **Settings dialog** (⚙) — configure backup suffix and local folder path in one place
- **Right-click context menus** on both listboxes
- **Keyboard shortcuts** — `F5` refresh, `Delete` to delete selected backup
- **Async operations** — backup, restore, delete run in background threads (UI never freezes)
- **Backup name sanitization** — strips invalid filename characters
- **Configurable backup suffix** — toggle state uses suffix from config (default `_backup`)
- **High-DPI awareness** — crisp rendering on 4K/HiDPI displays
- **`requirements.txt`** for dependency installs
- **`main.py`** as the single entry point

### Changed
- **Safe restore** — staging directory + atomic rename swap strategy (was copy-delete-copy)
- **Toggle State** — now uses configurable suffix instead of hardcoded `_backup`
- **Button layout** — grouped with vertical separators for clarity
- **Window** — now opens centered on screen with responsive width
- **Project structure** — `GUI.py` is now a pure module, launched via `main.py`

### Fixed
- `.gitignore` now covers runtime artifacts (`app.log`, `config.json`, `REPO Local backup/`)
- Tests use `unittest.mock.patch` consistently, no manual `sys.path` hacks
- Recycle Bin folder can no longer be accidentally deleted from the normal list
- DPI awareness call moved inside `__main__` guard with try/except

### Removed
- `app.log` untracked from repository (now gitignored)
- Old `_DELETED_<timestamp>` rename pattern (replaced by Recycle Bin)
