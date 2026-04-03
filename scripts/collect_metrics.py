#!/usr/bin/env python3
"""Master script that runs all evaluation components and aggregates results.

Orchestrates: run_tests.py, code_quality.py, coverage_check.py, metrics.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = PROJECT_ROOT / "evaluation" / "automated"

SCRIPTS = [
    ("Test Suites", EVAL_DIR / "run_tests.py"),
    ("Code Quality", EVAL_DIR / "code_quality.py"),
    ("Coverage", EVAL_DIR / "coverage_check.py"),
    ("Timing Metrics", EVAL_DIR / "metrics.py"),
]


def main() -> None:
    """Run all evaluation scripts in sequence."""
    print("=" * 70)
    print("AI Coding Bake-Off: Collecting All Metrics")
    print("=" * 70)

    failures: list[str] = []

    for name, script_path in SCRIPTS:
        print(f"\n{'=' * 70}")
        print(f"Running: {name}")
        print(f"{'=' * 70}\n")

        if not script_path.exists():
            print(f"  Script not found: {script_path}")
            failures.append(name)
            continue

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(PROJECT_ROOT),
        )

        if result.returncode != 0:
            print(f"\n  WARNING: {name} exited with code {result.returncode}")
            failures.append(name)

    print(f"\n{'=' * 70}")
    print("Collection Complete")
    print(f"{'=' * 70}")

    if failures:
        print(f"\nWarnings in: {', '.join(failures)}")
    else:
        print("\nAll evaluations completed successfully.")

    print(f"\nResults written to: {PROJECT_ROOT / 'evaluation' / 'results'}/")
    print("Run scripts/generate_report.py to create the comparison report.")


if __name__ == "__main__":
    main()
