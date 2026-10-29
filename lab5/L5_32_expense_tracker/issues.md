# Static Analysis Issues

The line numbers below refer to the original `expense_tracker.py` before fixes.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection | Bandit high (B605) | 61 | `os.system` built a shell command using the caller-provided path. | Open the resolved file URI with `webbrowser.open`, without invoking a shell. |
| Hardcoded bank password | Bandit low (B105) | 5 | The demo password was stored directly in source code. | Read the expected value from `BANK_SYNC_PASSWORD` and use constant-time comparison; reject an unset value. |
| Insecure temporary-file creation | Bandit medium (B306) | 55 | `tempfile.mktemp` generated a name without securely creating the file. | Create the file atomically with `NamedTemporaryFile` and `delete=False`. |
| Hardcoded temporary directory | Bandit medium (B108) | 8 | The report directory was pinned to `/tmp`, which is platform-specific and flagged as a temp-path risk. | Derive the report directory from `tempfile.gettempdir()` and create it when exporting. |
| Broad exception handling | Pylint warning (W0718) | 38–42 | `except Exception` concealed unrelated programming and runtime errors while handling an empty list. | Return `None` explicitly for an empty expense list; call `max` only when non-empty. |
| Non-snake-case names | Pylint convention (C0103) | 11–61 | Functions and variables used mixed-case names instead of PEP 8 snake_case. | Rename functions and local variables consistently, and update their call sites. |
| Index-based iteration | Pylint refactor (C0200) | 44–46 | The ledger loop used `range(len(expenses))` to retrieve list items by index. | Iterate with `enumerate(expenses, start=1)`. |
| Whitespace and line formatting | Flake8 (E203, E302, E261, E501) | 15, 44, 74, 77 | Spacing, blank lines, inline comment spacing, and line length violated PEP 8. | Apply standard spacing, separate top-level functions, remove the unnecessary comment, and wrap the long output call. |

