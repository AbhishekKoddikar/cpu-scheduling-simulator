from dataclasses import dataclass
from collections import deque
from typing import List, Dict, Tuple

@dataclass(frozen=True)
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def _segment(pid: str, start: int, end: int) -> Dict:
    return {"pid": pid, "start": start, "end": end, "duration": end - start}


def _metrics(processes: List[Process], segments: List[Dict]) -> Dict:
    completion = {}
    for s in segments:
        if s["pid"] != "IDLE":
            completion[s["pid"]] = max(completion.get(s["pid"], 0), s["end"])
    rows = []
    for p in processes:
        ct = completion[p.pid]
        tat = ct - p.arrival
        wt = tat - p.burst
        rows.append({"pid": p.pid, "arrival": p.arrival, "burst": p.burst, "priority": p.priority,
                     "completion": ct, "turnaround": tat, "waiting": wt})
    avg_wt = sum(r["waiting"] for r in rows) / len(rows) if rows else 0
    avg_tat = sum(r["turnaround"] for r in rows) / len(rows) if rows else 0
    return {"processes": rows, "gantt": _merge_segments(segments),
            "average_waiting_time": avg_wt, "average_turnaround_time": avg_tat,
            "makespan": max((s["end"] for s in segments), default=0)}


def _merge_segments(segments: List[Dict]) -> List[Dict]:
    merged = []
    for s in segments:
        if s["end"] <= s["start"]:
            continue
        if merged and merged[-1]["pid"] == s["pid"] and merged[-1]["end"] == s["start"]:
            merged[-1]["end"] = s["end"]
            merged[-1]["duration"] = merged[-1]["end"] - merged[-1]["start"]
        else:
            merged.append(dict(s))
    return merged


def fcfs(processes: List[Process]) -> Dict:
    ps = sorted(processes, key=lambda p: (p.arrival, p.pid))
    t, seg = 0, []
    for p in ps:
        if t < p.arrival:
            seg.append(_segment("IDLE", t, p.arrival)); t = p.arrival
        seg.append(_segment(p.pid, t, t + p.burst)); t += p.burst
    return _metrics(processes, seg)


def sjf(processes: List[Process]) -> Dict:
    remaining = {p.pid: p for p in processes}
    t, seg = 0, []
    while remaining:
        ready = [p for p in remaining.values() if p.arrival <= t]
        if not ready:
            nxt = min(remaining.values(), key=lambda p: (p.arrival, p.pid))
            seg.append(_segment("IDLE", t, nxt.arrival)); t = nxt.arrival; continue
        p = min(ready, key=lambda p: (p.burst, p.arrival, p.pid))
        seg.append(_segment(p.pid, t, t + p.burst)); t += p.burst
        del remaining[p.pid]
    return _metrics(processes, seg)


def priority_scheduling(processes: List[Process]) -> Dict:
    remaining = {p.pid: p for p in processes}
    t, seg = 0, []
    while remaining:
        ready = [p for p in remaining.values() if p.arrival <= t]
        if not ready:
            nxt = min(remaining.values(), key=lambda p: (p.arrival, p.pid))
            seg.append(_segment("IDLE", t, nxt.arrival)); t = nxt.arrival; continue
        # Lower numeric priority means higher priority.
        p = min(ready, key=lambda p: (p.priority, p.arrival, p.pid))
        seg.append(_segment(p.pid, t, t + p.burst)); t += p.burst
        del remaining[p.pid]
    return _metrics(processes, seg)


def round_robin(processes: List[Process], quantum: int) -> Dict:
    if quantum <= 0:
        raise ValueError("Round Robin time quantum must be a positive integer.")
    ps = sorted(processes, key=lambda p: (p.arrival, p.pid))
    rem = {p.pid: p.burst for p in ps}
    q = deque()
    t, i, seg = 0, 0, []
    while q or i < len(ps):
        if not q:
            if t < ps[i].arrival:
                seg.append(_segment("IDLE", t, ps[i].arrival)); t = ps[i].arrival
            while i < len(ps) and ps[i].arrival <= t:
                q.append(ps[i]); i += 1
        p = q.popleft()
        run = min(quantum, rem[p.pid])
        seg.append(_segment(p.pid, t, t + run)); t += run; rem[p.pid] -= run
        while i < len(ps) and ps[i].arrival <= t:
            q.append(ps[i]); i += 1
        if rem[p.pid] > 0:
            q.append(p)
    return _metrics(processes, seg)


def simulate(processes: List[Process], quantum: int = 2) -> Dict:
    if not processes:
        raise ValueError("At least one process is required.")
    results = {
        "FCFS": fcfs(processes),
        "SJF": sjf(processes),
        "Round Robin": round_robin(processes, quantum),
        "Priority": priority_scheduling(processes),
    }
    comparison = [
        {"algorithm": name, "average_waiting_time": data["average_waiting_time"],
         "average_turnaround_time": data["average_turnaround_time"], "makespan": data["makespan"]}
        for name, data in results.items()
    ]
    return {"quantum": quantum, "results": results, "comparison": comparison}
