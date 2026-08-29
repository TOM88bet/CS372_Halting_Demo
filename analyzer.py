import subprocess
import sys
import time
from pathlib import Path


def analyze_program(script_path, args=None, timeout=2.0):
    """Run a Python script in a child process and classify only by timeout.

    If the process exits before timeout, the observed status is HALTS.
    If the timeout expires, the status is UNKNOWN and the child process is terminated.
    """
    script_path = Path(script_path)
    if not script_path.exists():
        return {
            "status": "ERROR",
            "elapsed_seconds": 0.0,
            "exit_code": None,
            "stdout": "",
            "stderr": f"Script not found: {script_path}",
            "timed_out": False,
        }

    command = [sys.executable, str(script_path)]
    if args is None:
        args = []
    elif isinstance(args, str):
        args = [args]
    command.extend(str(arg) for arg in args)

    start = time.perf_counter()
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return {
            "status": "ERROR",
            "elapsed_seconds": round(time.perf_counter() - start, 6),
            "exit_code": None,
            "stdout": "",
            "stderr": f"Failed to launch process: {exc}",
            "timed_out": False,
        }

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        elapsed = time.perf_counter() - start
        return {
            "status": "HALTS",
            "elapsed_seconds": round(elapsed, 6),
            "exit_code": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            stdout, stderr = process.communicate()
        except Exception:
            stdout, stderr = "", ""

        elapsed = time.perf_counter() - start
        return {
            "status": "UNKNOWN",
            "elapsed_seconds": round(elapsed, 6),
            "exit_code": None,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": True,
        }
    except Exception as exc:
        try:
            process.kill()
        except Exception:
            pass
        return {
            "status": "ERROR",
            "elapsed_seconds": round(time.perf_counter() - start, 6),
            "exit_code": None,
            "stdout": "",
            "stderr": f"Analyzer failure: {exc}",
            "timed_out": False,
        }


if __name__ == "__main__":
    sample = analyze_program("test_cases/case1_immediate.py", timeout=2.0)
    print(sample)
