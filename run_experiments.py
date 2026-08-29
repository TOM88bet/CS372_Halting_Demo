import csv
import sys
from pathlib import Path

from analyzer import analyze_program


ROOT = Path(__file__).resolve().parent
TEST_CASES_DIR = ROOT / "test_cases"
RESULTS_DIR = ROOT / "results"
CSV_PATH = RESULTS_DIR / "results.csv"
TIMEOUT_SECONDS = 2.0


def build_experiments():
    return [
        {
            "case": "Immediate termination",
            "script": TEST_CASES_DIR / "case1_immediate.py",
            "args": [],
            "known_behavior": "Halts",
            "description": "Very short program that terminates immediately.",
            "input": "N/A",
        },
        {
            "case": "Finite loop",
            "script": TEST_CASES_DIR / "case2_finite_loop.py",
            "args": [],
            "known_behavior": "Halts",
            "description": "A finite loop with a bounded computation.",
            "input": "N/A",
        },
        {
            "case": "Slow termination",
            "script": TEST_CASES_DIR / "case3_slow_halt.py",
            "args": [],
            "known_behavior": "Halts after about 3 s",
            "description": "Program terminates, but only after exceeding the 2-second observation window.",
            "input": "N/A",
        },
        {
            "case": "Infinite loop",
            "script": TEST_CASES_DIR / "case4_infinite_loop.py",
            "args": [],
            "known_behavior": "Does not halt",
            "description": "Program was written to run forever.",
            "input": "N/A",
        },
        {
            "case": "Input-dependent program",
            "script": TEST_CASES_DIR / "case5_input_dependent.py",
            "args": ["1"],
            "known_behavior": "Halts",
            "description": "Same program as case 5B, but with a positive input that terminates.",
            "input": "1",
        },
        {
            "case": "Input-dependent program",
            "script": TEST_CASES_DIR / "case5_input_dependent.py",
            "args": ["0"],
            "known_behavior": "Does not halt",
            "description": "Same program as case 5A, but with zero input that triggers an infinite loop.",
            "input": "0",
        },
    ]


def write_results_csv(rows):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "case",
                "input",
                "known_behavior",
                "timeout_seconds",
                "observed_status",
                "elapsed_seconds",
                "exit_code",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def print_report(experiments):
    print("=" * 60)
    print("HALTING PROBLEM: FINITE OBSERVATION DEMONSTRATION")
    print(f"Observation timeout: {TIMEOUT_SECONDS} seconds")
    print("=" * 60)

    rows = []
    for index, exp in enumerate(experiments, start=1):
        result = analyze_program(exp["script"], exp["args"], TIMEOUT_SECONDS)
        label = f"Case {index}: {exp['case']}"
        print(f"\n{label}")
        print(f"Known behavior : {exp['known_behavior']}")
        print(f"Observed result: {result['status']}")
        print(f"Elapsed time   : {result['elapsed_seconds']:.6f} seconds")
        if result["exit_code"] is not None:
            print(f"Exit code      : {result['exit_code']}")
        else:
            print("Exit code      : N/A")
        print(f"Purpose        : {exp['description']}")
        print("-" * 60)

        rows.append(
            {
                "case": exp["case"],
                "input": exp["input"],
                "known_behavior": exp["known_behavior"],
                "timeout_seconds": TIMEOUT_SECONDS,
                "observed_status": result["status"],
                "elapsed_seconds": round(result["elapsed_seconds"], 6),
                "exit_code": result["exit_code"],
                "notes": exp["description"],
            }
        )

    print("\nSummary")
    print(f"{'Case':<28} {'Known Behavior':<22} {'Observed':<10} {'Elapsed(s)':>12}")
    print("-" * 76)
    for exp in experiments:
        result = analyze_program(exp["script"], exp["args"], TIMEOUT_SECONDS)
        print(
            f"{exp['case']:<28} {exp['known_behavior']:<22} {result['status']:<10} {result['elapsed_seconds']:>12.6f}"
        )

    return rows


def main():
    experiments = build_experiments()
    rows = print_report(experiments)
    write_results_csv(rows)
    print(f"\nResults saved to: {CSV_PATH}")


if __name__ == "__main__":
    main()
