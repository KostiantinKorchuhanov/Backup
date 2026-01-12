# BackTrack

BackTrack is a safe configuration backup and restore utility for Linux.  
It supports both CLI and GUI, providing temporary and permanent backups, file rollback, and easy management of configuration files.

---

## Features

- **Temporary backups** while editing files with rollback capability
- **Permanent backups** with configurable storage time (hours or days)
- CLI commands for creating, restoring, and listing backups
- GUI interface for visual management
- Automatic cleanup of old backups
- Works with any text file and configuration file

---
## Third-party assets
Source code is licensed under the GNU GPL v3.0.

**Icons are provided by Icons8 (https://icons8.com) and are licensed separately.
Icons are NOT covered by the GPL and may not be used, copied, or redistributed
except in accordance with the Icons8 license.**
---

## Requirements

- Python 3.10+  
- Linux 
- CustomTkinter (if GUI is used)

**Install dependencies on Arch Linux:**

```bash
sudo pacman -S python tk
pip install customtkinter
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/KostiantinKorchuhanov/Backup.git
cd Backup
```

2. Make the install script executable and run it:

```bash
chmod +x install.sh
./install.sh
```

**The install.sh script will:**

 - Create a Python virtual environment in .venv (if not already exists)
 - Activate the virtual environment
 - Upgrade pip
 - Install the BackTrack package into the virtual environment

**After installation, activate the environment:**

```bash
source .venv/bin/activate
```
---

## Run the program:
**To run the CLI:**
```
Show the help
bt --help

Create a backup
bt -b example.txt

Edit a file safely
bt edit vim example.txt

List backups
bt --show

Restore backup by ID
bt -r 12345
```

**To run the GUI:**
```
bt-gui
```
---

## Project Structure
```
app/
  cli.py                             # CLI entry point
  gui.py                             # GUI entry point
  logging_config.py                  # Logging setup
  widgets/
    crate_warning_widget.py          # Warning widget to confirm deletion or restoring
    create_backup_widget.py          # A bottun ADD to create a new backup
    create_items_widget.py           # The main widget to create a list of all of the backups
    create_settings_widget.py        # A settings widget to change some main settings
  image/                             # GUI icons
  database/                          # Internal database for backups
core/
  backup.py                          # Permanent backup creation
  restore.py                         # Backup restoration
  cleaner.py                         # Cleanup old backups
  temp_backup.py                     # Temporary backups for edits
  list.py                            # Display backups
  utils.py                           # Helper functions for interaction with the data
tests/                               # Pytest test cases
install.sh                           # Local installation script
pyproject.toml                       
README.md              
LICENSE                              
```
