# Bug Tracker
## About the Project

Bug Tracker is a Python command-line application designed to create and manage bug reports.

Users can create reports, view existing reports, update their status, search and filter reports, and delete them. All reports are saved locally using JSON, allowing data to persist between sessions.


## Features

- Create bug reports with a title, description, and severity.
- View all existing bug reports.
- Update bug statuses.
- Search and filter reports by ID, severity, or status.
- Delete bug reports with confirmation.
- Automatically save and load reports using JSON.

## How to Run

1. Clone the GitHub repository
2. Open a terminal in the project folder
3. Run this command `python Main.py` 

## Testing

This project includes a file named `test_main.py`, which contains 18 automated tests using pytest.

These tests check whether the main functions behave correctly, helping detect errors after changes to the code.

To run the tests:

Install `pytest` using your terminal:

```bash
python -m pip install pytest
```

Open a terminal in the project folder and run:

```bash
python -m pytest
```

If everything works correctly, you should see a result similar to:

```text
18 passed in 0.32s
```

The execution time may vary depending on your computer.

## Requirements

- Python 3.10 or newer (required for `match/case` syntax).
- `pytest` (only required to run the automated tests).


## Future Plans

*Hypothetical Application:* My long-term goal is to adapt this project into a "Report a Bug" window within a game or desktop application, allowing users to report issues directly through its interface.

