# CPU Scheduling Algorithm Simulator

A full-stack CPU scheduling simulator for an Operating Systems project. It accepts processes with arrival time, burst time, and priority, then runs FCFS, SJF, Round Robin, and Priority scheduling. The UI renders Gantt charts and compares average waiting time, average turnaround time, and makespan.

## Included
- FCFS (non-preemptive)
- SJF (non-preemptive)
- Round Robin with configurable time quantum
- Priority scheduling (non-preemptive; lower number = higher priority)
- CPU idle periods
- Average waiting time and turnaround time
- Completion time per process
- Interactive Gantt charts
- Input validation and API error handling
- Automated tests for textbook scenarios

## Run on Windows
```powershell
cd cpu-scheduling-simulator
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python backend\app.py
```
Open http://127.0.0.1:5000

## Run on macOS/Linux
```bash
cd cpu-scheduling-simulator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```
Open http://127.0.0.1:5000

## Test
```bash
python -m unittest discover -s tests -v
```

## API
`POST /api/simulate`

Example:
```json
{
  "quantum": 2,
  "processes": [
    {"pid":"P1","arrival":0,"burst":7,"priority":2},
    {"pid":"P2","arrival":2,"burst":4,"priority":1},
    {"pid":"P3","arrival":4,"burst":1,"priority":3},
    {"pid":"P4","arrival":5,"burst":4,"priority":2}
  ]
}
```
