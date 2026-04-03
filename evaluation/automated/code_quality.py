#!/usr/bin/env python3
"""Run code quality checks (ruff, mypy) against agent solutions and score results.

Scores are based on the number and severity of issues found.
"""

import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "harnesses"


@dataclass
class QualityResult:
    """Code quality result for one agent/level."""

    agent: str
    level: int
    ruff_issues: int = 0
    ruff_output: str = ""
    mypy_errors: int = 0
    mypy_output: str = ""
    pylint_score: float = 0.0
    pylint_output: str = ""

    @property
    def score(self) -> float:
        """Quality score on 1-5 scale."""
        total_issues = self.ruff_issues + self.mypy_errors
        if total_issues == 0:
            return 5.0
        if total_issues <= 3:
            return 4.0
        if total_issues <= 10:
            return 3.0
        if total_issues <= 25:
            return 2.0
        return 1.0


def run_ruff(solution_dir: Path) -> tuple[int, str]:
    """Run ruff linter and return issue count and output."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", str(solution_dir),
             "--select", "E,F,W,I,N,UP", "--quiet"],
            capture_output=True, text=True, timeout=60,
        )
        output = result.stdout.strip()
        issue_count = len([l for l in output.split("\n") if l.strip()]) if output else 0
        return issue_count, output
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return -1, f"ruff not available: {e}"


def run_mypy(solution_dir: Path) -> tuple[int, str]:
    """Run mypy and return error count and output."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mypy", str(solution_dir),
             "--ignore-missing-imports", "--no-error-summary"],
            capture_output=True, text=True, timeout=120,
        )
        output = result.stdout.strip()
        error_count = len([
            l for l in output.split("\n")
            if l.strip() and ": error:" in l
        ]) if output else 0
        return error_count, output
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return -1, f"mypy not available: {e}"


def discover_solutions() -> list[tuple[str, int, Path]]:
    """Find all agent/level solution directories."""
    solutions = []
    if not AGENTS_DIR.exists():
        return solutions
    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("."):
            continue
        for level in range(1, 6):
            level_dir = agent_dir / "output" / f"level-{level}"
            if level_dir.exists():
                solutions.append((agent_dir.name, level, level_dir))
    return solutions


def main() -> None:
    """Run code quality checks on all solutions."""
    solutions = discover_solutions()
    if not solutions:
        print("No solutions found in harnesses/")
        sys.exit(1)

    results: list[QualityResult] = []

    for agent, level, solution_dir in solutions:
        print(f"  Checking {agent} / Level {level}...", end=" ", flush=True)

        qr = QualityResult(agent=agent, level=level)
        qr.ruff_issues, qr.ruff_output = run_ruff(solution_dir)
        qr.mypy_errors, qr.mypy_output = run_mypy(solution_dir)
        results.append(qr)

        print(f"ruff: {qr.ruff_issues} issues, mypy: {qr.mypy_errors} errors (score: {qr.score:.1f}/5.0)")

    # Write report
    output_path = PROJECT_ROOT / "evaluation" / "results" / "quality_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "results": [asdict(r) for r in results],
            },
            f,
            indent=2,
        )

    print(f"\nReport written to {output_path}")


if __name__ == "__main__":
    main()
