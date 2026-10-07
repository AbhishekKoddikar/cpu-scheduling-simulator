# CPU Scheduling Algorithm Simulator

A full-stack Operating Systems project that simulates and compares four classic CPU scheduling algorithms: **FCFS, SJF, Round Robin, and Priority Scheduling**.

The application accepts a set of processes with arrival time, burst time, and priority, executes every algorithm on the same workload, generates interactive Gantt-style timelines, and calculates average waiting time, average turnaround time, and makespan.

## Features

- FCFS (First-Come, First-Served)
- SJF (Shortest Job First, non-preemptive)
- Round Robin with configurable time quantum
- Priority Scheduling (non-preemptive; lower number = higher priority)
- Process arrival-time handling, including CPU idle periods
- Gantt charts for every algorithm
- Per-process completion, waiting, and turnaround times
- Average waiting-time and turnaround-time comparison
- Makespan comparison
- Input validation and useful API error messages
- Responsive frontend
- Automated unit tests for the scheduling engine
- No external dataset or database required

## Technology Stack

**Frontend:** HTML5, CSS3, Vanilla JavaScript

**Backend:** Python, Flask

**Testing:** Python `unittest`

**Architecture:** Browser → Flask REST API → Scheduling Engine → JSON Results → Browser visualization

## Project Structure

```text
cpu-scheduling-simulator/
├── backend/
│   ├── app.py              # Flask application and REST API
│   └── scheduler.py        # Scheduling algorithms and metrics
├── frontend/
│   ├── index.html          # User interface
│   ├── style.css           # UI styling
│   └── app.js              # Frontend logic and Gantt rendering
├── tests/
│   └── test_scheduler.py   # Automated scheduler tests
├── requirements.txt
├── .gitignore
└── README.md
```

## Scheduling Algorithms

### FCFS
Processes are executed in ascending arrival order. Once a process starts, it runs until completion.

### SJF
Among processes that have arrived, the process with the shortest burst time is selected. This implementation is non-preemptive.

### Round Robin
Processes share the CPU in circular order. Each process receives at most the configured time quantum before returning to the ready queue if work remains.

### Priority Scheduling
Among ready processes, the process with the highest priority is selected. **A smaller numerical priority value means higher priority.** This implementation is non-preemptive.

## Metrics

For every algorithm the simulator calculates:

- **Completion Time (CT):** time at which a process finishes.
- **Turnaround Time (TAT):** `CT - Arrival Time`.
- **Waiting Time (WT):** `TAT - Burst Time`.
- **Average Waiting Time:** mean waiting time across all processes.
- **Average Turnaround Time:** mean turnaround time across all processes.
- **Makespan:** total elapsed schedule time from the start of the timeline to the final completion.

## Run Locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the server

```powershell
python backend\app.py
```

Open `http://127.0.0.1:5000/` in a browser.

Keep the terminal running while using the simulator.

## API

### Health check

```http
GET /api/health
```

### Simulation

```http
POST /api/simulate
Content-Type: application/json
```

Example request:

```json
{
  "quantum": 2,
  "processes": [
    {"pid": "P1", "arrival": 0, "burst": 5, "priority": 2},
    {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
    {"pid": "P3", "arrival": 2, "burst": 1, "priority": 3}
  ]
}
```

## Run Tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

The test suite covers FCFS, SJF, Priority, Round Robin, CPU idle time, and the combined simulation endpoint logic.

## Sample Result

For:

```text
P1: Arrival=0, Burst=5, Priority=2
P2: Arrival=1, Burst=3, Priority=1
P3: Arrival=2, Burst=1, Priority=3
Round Robin Quantum=2
```

SJF produces the lowest average waiting time for this workload.

## Demo Flow

1. Enter processes or load the sample dataset.
2. Set the Round Robin time quantum.
3. Click **Run all algorithms**.
4. Inspect each Gantt chart.
5. Compare average waiting and turnaround times.
6. Explain why the best algorithm can change depending on the workload.

## Limitations

- SJF and Priority are implemented as non-preemptive algorithms.
- The simulator models a single CPU.
- Context-switch overhead is not modeled.
- All process execution times are integer CPU time units.

## Future Enhancements

- Preemptive SJF / SRTF
- Preemptive Priority Scheduling
- Context-switch overhead simulation
- Export results to CSV/PDF
- Interactive timeline zooming
- Additional scheduling algorithms such as Multilevel Queue and Multilevel Feedback Queue

## License

This project is intended for educational and academic use.
