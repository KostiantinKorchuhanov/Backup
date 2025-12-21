### Conf-Backtrack

Conf-Backtrack is a lightweight utility for safely editing configuration files on Linux. It automatically creates a temporary backup before opening a file and allows you to instantly restore a working version in case of mistakes.

### _Key Features_
- _Auto Backup_: creates file copies while preserving permissions (chmod/chown) before editing.
- _Smart TTL_: set backup lifetime in minutes, hours, or days.
- _Instant Rollback_: restore the original file with a single command using a unique ID.
- _Auto Cleanup_: automatically removes expired backups.
- _Dual Interface_: work via terminal (CLI) or a convenient graphical interface (GUI).

### Project Structure
```

- core/       — system logic (backup, rollback, cleanup, database management)
- data.json   — registry of all active backups and metadata
- cli_app.py  — entry point for terminal use
- gui_app.py  — graphical backup manager

```


Conf-Backtrack is perfect for system administrators and developers who value safety, speed, and convenience when working with critical Linux configuration files.
