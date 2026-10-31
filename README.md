# Concurrent System Resource Monitor

Academic project developed for the Concurrent and Distributed Programming course. The application monitors system resource usage through a concurrent producer-consumer architecture and presents information in a Tkinter interface.

## Features
- Collects CPU, memory (RAM) and disk usage metrics.
- Uses producer and consumer worker threads.
- Transfers measurements through a bounded, thread-safe queue.
- Uses a shared stop event to coordinate shutdown.
- Includes a supervisor that checks worker futures and attempts to restart completed workers.
- Displays monitoring information through Tkinter.

## Technology stack
- Python 3.10+ (recommended)
- `threading` and `concurrent.futures`
- `queue`
- Tkinter
- `psutil`

## Setup
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

Optional arguments:
```bash
python main.py --consumers 2 --queue-size 100 --duration 60 --verbose
```

On Linux, select a valid disk path, for example `--disk-path /`. On Windows, the default path is `C:\`. Tkinter must be available in the Python installation.

## Project structure
- `main.py` — application entry point, thread pools and supervisor.
- `producers.py` — resource metric producers.
- `consumers.py` — queue consumers.
- `resource_monitor_gui.py` — graphical interface.
- `resource_monitor_utils.py` — supporting utilities.

## Academic context
Developed for the Concurrent and Distributed Programming course (TP1).
