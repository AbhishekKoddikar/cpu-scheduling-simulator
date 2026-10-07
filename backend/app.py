from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from scheduler import Process, simulate

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
app = Flask(__name__)


def parse_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")
    raw = payload.get("processes")
    if not isinstance(raw, list) or not raw:
        raise ValueError("Provide at least one process.")
    seen = set(); processes = []
    for i, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise ValueError(f"Process {i} must be an object.")
        pid = str(item.get("pid", f"P{i}")).strip()
        if not pid:
            raise ValueError(f"Process {i}: ID is required.")
        if pid in seen:
            raise ValueError(f"Duplicate process ID: {pid}.")
        seen.add(pid)
        try:
            arrival = int(item.get("arrival"))
            burst = int(item.get("burst"))
            priority = int(item.get("priority"))
        except (TypeError, ValueError):
            raise ValueError(f"{pid}: arrival, burst, and priority must be integers.")
        if arrival < 0:
            raise ValueError(f"{pid}: arrival time cannot be negative.")
        if burst <= 0:
            raise ValueError(f"{pid}: burst time must be greater than 0.")
        processes.append(Process(pid, arrival, burst, priority))
    try:
        quantum = int(payload.get("quantum", 2))
    except (TypeError, ValueError):
        raise ValueError("Time quantum must be an integer.")
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than 0.")
    return processes, quantum


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.post("/api/simulate")
def api_simulate():
    try:
        processes, quantum = parse_payload(request.get_json(silent=True))
        return jsonify(simulate(processes, quantum))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Simulation error")
        return jsonify({"error": "Unexpected server error. Please check the input."}), 500


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
