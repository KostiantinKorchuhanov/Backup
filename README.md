### Conf-Backtrack

Conf-Backtrack is a lightweight utility for safely editing configuration files on Linux. It automatically creates a temporary backup before opening a file and allows you to instantly restore a working version in case of mistakes.

### How to use code
To start a gui use this in a parent directory:
```
python -m app.gui
```
To use CLI use this as an example to create a backup:
```
python -m app.cli -b /home/user/Desktop/something
```

### Dependencies
Additional libraries: 
```
customtkinter
Pillow
argparse
```

### _Key Features_
- _Auto Backup_: creates file copies while preserving permissions (chmod/chown) before editing.
- _Smart TTL_: set backup lifetime in minutes, hours, or days.
- _Instant Rollback_: restore the original file with a single command using a unique ID.
- _Auto Cleanup_: automatically removes expired backups.
- _Dual Interface_: work via terminal (CLI) or a convenient graphical interface (GUI).

### Project Structure
```

- core/       — system logic (backup, rollback, cleanup, database management)
  - backup.py
  - list.py
  - restore.py
- app
  - images
  - widgets
    - create_backup_widget.py
    - create_restore_widget.py
  - cli_app.py  — entry point for terminal use
  - gui_app.py  — graphical backup manager
- database
  - data.json   — registry of all active backups and metadata

```
