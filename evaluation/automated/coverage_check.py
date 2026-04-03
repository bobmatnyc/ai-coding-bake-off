#!/usr/bin/env python3
"""Run pytest --cov for each agent solution and collect coverage metrics."""

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "harnesses"


@dataclass
class CoverageResult:
    """Coverage result for one agent/level."""

    agent: str
    level: int
    coverage_percent: float = 0.0
    total_statements: int = 0
    covered_statements: int = 0
    missing_statements: int = 0
    output: str = ""

    @property
    def score(self) -> float:
        """Coverage score on 1-5 scale."""
        pct = self.coverage_percent
        if pct >= 90:
            return 5.0
        if pct >= 75:
            return 4.0
        if pct >= 60:
            return 3.0
        if pct >= 40:
            return 2.0
        return 1.0


def run_coverage(agent: str, level: int, solution_dir: Path) -> CoverageResult:
    """Run pytest --cov on an agent's solution and their own tests."""
    result = CoverageResult(agent=agent, level=level)

    test_dirs = []
    for candidate in [solution_dir / "tests", solution_dir / "test"]:
        if candidate.exists():
            test_dirs.append(str(candidate))

    if not test_dirs:
        result.output = "No test directory found"
        return result

    # Determine source directory for coverage
    src_dirs = []
    for candidate in ["src", ".", agent.replace("-", "_")]:
        if (solution_dir / candidate).exists():
            src_dirs.append(candidate)

    cov_source = src_dirs[0] if src_dirs else "."

    cmd = [
        sys.executable, "-m", "pytest",
        *test_dirs,
        f"--cov={cov_source}",
        "--cov-report=json",
        "--cov-report=term-missing",
        "-q", "--no-header",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(solution_dir),
        )
        result.output = proc.stdout

        # Try to parse coverage JSON
        cov_json = solution_dir / "coverage.json"
        if cov_json.exists():
            with open(cov_json) as f:
                cov_data = json.load(f)
            totals = cov_data.get("totals", {})
            result.coverage_percent = totals.get("percent_covered", 0.0)
            result.total_statements = totals.get("num_statements", 0)
            result.covered_statements = totals.get("covered_lines", 0)
            result.missing_statements = totals.get("missing_lines", 0)
            cov_json.unlink()  # Clean up
        else:
            # Parse from terminal output
            for line in proc.stdout.split("\n"):
                if "TOTAL" in line:
                    parts = line.split()
                    for part in parts:
                        if part.endswith("%"):
                            result.coverage_percent = float(part.rstrip("%"))
                            break

    except subprocess.TimeoutExpired:
        result.output = "Coverage analysis timed out"
    except Exception as e:
        result.output = f"Error: {e}"

    return result


def main() -> None:
    """Run coverage analysis on all solutions."""
    results: list[CoverageResult] = []

    if not AGENTS_DIR.exists():
        print("No harnesses/ directory found")
        sys.exit(1)

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("."):
            continue
        for level in range(1, 6):
            level_dir = agent_dir / "output" / f"level-{level}"
            if not level_dir.exists():
                continue

            print(f"  Coverage: {agent_dir.name} / Level {level}...", end=" ", flush=True)
            cr = run_coverage(agent_dir.name, level, level_dir)
            results.append(cr)
            print(f"{cr.coverage_percent:.1f}% (score: {cr.score:.1f}/5.0)")

    # Write report
    output_path = PROJECT_ROOT / "evaluation" / "results" / "coverage_results.json"
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
