# Lab 5 Reflection

## 1. Which fixes were easiest, and which were hardest?

The spacing issues and the `range(len(expenses))` loop were the easiest:
standard formatting corrected the former, and `enumerate` made the ledger loop
clearer without changing its output. Replacing the hardcoded password and
shell-based file opening took more thought because the safer alternatives had
to remain useful without embedding a secret or passing user-controlled text to
a shell. The temporary-file fix also needed to create the file securely while
keeping it available after the helper returns.

## 2. Were there false positives in Bandit or Pylint?

Bandit flagged the password literal even though it was only a demonstration
credential; that is still a useful warning because source-controlled
credentials can be mistaken for real secrets or reused. Its temporary-directory
warning was triggered by the fixed `/tmp` path; moving to the platform's
temporary directory removes the hardcoded assumption and improves portability.
Pylint's warning about the broad `except Exception` was not a false positive:
the handler hid every failure when the actual case to handle was an empty
expense list. The warnings for camelCase and `range(len(...))` were style or
maintainability findings rather than immediate runtime failures.

## 3. How could these tools be integrated into CI or pre-commit?

Add the linters as development dependencies and run Pylint, Bandit, and Flake8
in a CI workflow on every pull request. Configure the workflow to fail when a
tool reports an issue, and retain or publish reports as build artifacts when
useful. A pre-commit configuration can run the same commands on changed Python
files before each commit, giving developers faster feedback. Pinning tool
versions in the project keeps local and CI results consistent.

## 4. How did the fixes improve robustness and readability?

The largest-expense helper now handles the empty collection directly instead
of hiding arbitrary exceptions. Secure temporary-file creation avoids the
race condition in `mktemp`, and deriving the report directory from the
operating system's temporary location improves portability. Environment-based
password configuration avoids a source-code secret, while `hmac.compare_digest`
compares the configured value safely. Opening a file through its URI avoids
shell parsing and command injection. Finally, snake_case names, `enumerate`,
docstrings, and consistent formatting make the program easier to scan and
maintain. The demo retains the same console output.
