#!/usr/bin/env python3
"""Run test suites against all agent solutions and collect results.

Discovers agent workspaces, runs the provided test suite for each level,
and collects pass/fail results into a structured report.
"""

import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"
CHALLENGES_DIR = PROJECT_ROOT / "challenges"

LEVEL_DIRS = {
    1: "level-1-table-formatter",
    2: "level-2-git-analyzer",
    3: "level-3-weather-alerter",
    4: "level-4-doc-pipeline",
    5: "level-5-task-board",
}


@dataclass
class TestResult:
    """Result of running a test suite for one agent/level combination."""

    agent: str
    level: int
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    total: int = 0
    duration_seconds: float = 0.0
    stdout: str = ""
    stderr: str = ""
    exit_code: int = -1

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passed / self.total

    @property
    def score(self) -> float:
        """Correctness score on 1-5 scale based on pass rate."""
        rate = self.pass_rate
        if rate >= 0.95:
            return 5.0
        if rate >= 0.80:
            return 4.0
        if rate >= 0.60:
            return 3.0
        if rate >= 0.40:
            return 2.0
        return 1.0


@dataclass
class TestReport:
    """Aggregated test results across all agents and levels."""

    generated_at: str = ""
    results: list[TestResult] = field(default_factory=list)


def discover_agents() -> list[str]:
    """Find all agent directories that contain solutions."""
    agents = []
    if not AGENTS_DIR.exists():
        return agents
    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if agent_dir.is_dir() and not agent_dir.name.startswith("."):
            agents.append(agent_dir.name)
    return agents


def run_test_suite(agent: str, level: int) -> TestResult:
    """Run the provided test suite for a specific agent/level."""
    result = TestResult(agent=agent, level=level)

    challenge_dir = CHALLENGES_DIR / LEVEL_DIRS[level]
    test_dir = challenge_dir / "test_suite"
    agent_solution = AGENTS_DIR / agent / f"level-{level}"

    if not agent_solution.exists():
        result.stderr = f"Solution directory not found: {agent_solution}"
        return result

    if not test_dir.exists():
        result.stderr = f"Test suite not found: {test_dir}"
        return result

    # Run pytest with the agent's solution on the Python path
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "--no-header",
        "-q",
    ]

    env_path = f"{agent_solution}:{agent_solution / 'src'}"

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(agent_solution),
            env={**__import__("os").environ, "PYTHONPATH": env_path},
        )
        result.stdout = proc.stdout
        result.stderr = proc.stderr
        result.exit_code = proc.returncode

        # Parse pytest output for counts
        for line in proc.stdout.split("\n"):
            line = line.strip()
            if "passed" in line or "failed" in line or "error" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        result.passed = int(parts[i - 1])
                    elif part == "failed" and i > 0:
                        result.failed = int(parts[i - 1])
                    elif part == "error" in part and i > 0:
                        result.errors = int(parts[i - 1])
                    elif part == "skipped" and i > 0:
                        result.skipped = int(parts[i - 1])

        result.total = result.passed + result.failed + result.errors

    except subprocess.TimeoutExpired:
        result.stderr = "Test suite timed out after 120 seconds"
    except Exception as e:
        result.stderr = f"Error running tests: {e}"

    return result


def main() -> None:
    """Run all test suites and generate report."""
    report = TestReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    agents = discover_agents()
    if not agents:
        print("No agent directories found in agents/")
        sys.exit(1)

    print(f"Discovered agents: {', '.join(agents)}")
    print(f"Running test suites for levels 1-5...\n")

    for agent in agents:
        for level in range(1, 6):
            agent_level_dir = AGENTS_DIR / agent / f"level-{level}"
            if not agent_level_dir.exists():
                continue

            print(f"  Testing {agent} / Level {level}...", end=" ", flush=True)
            result = run_test_suite(agent, level)
            report.results.append(result)

            if result.total > 0:
                print(
                    f"{result.passed}/{result.total} passed "
                    f"(score: {result.score:.1f}/5.0)"
                )
            else:
                print(f"No tests ran. {result.stderr[:80]}")

    # Write report
    output_path = PROJECT_ROOT / "evaluation" / "results" / "test_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(
            {
                "generated_at": report.generated_at,
                "results": [asdict(r) for r in report.results],
            },
            f,
            indent=2,
        )

    print(f"\nReport written to {output_path}")

    # Print summary table
    print("\n" + "=" * 70)
    print(f"{'Agent':<20} {'Level':<8} {'Passed':<10} {'Total':<10} {'Score':<8}")
    print("-" * 70)
    for r in report.results:
        print(f"{r.agent:<20} {r.level:<8} {r.passed:<10} {r.total:<10} {r.score:<8.1f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
