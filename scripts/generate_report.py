#!/usr/bin/env python3
"""Generate a Markdown comparison report from all evaluation results.

Reads JSON results from evaluation/results/ and produces a human-readable
comparison report with tables and analysis.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "evaluation" / "results"


def load_json(filename: str) -> dict | None:
    """Load a JSON results file, returning None if not found."""
    path = RESULTS_DIR / filename
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def generate_test_table(test_data: dict) -> str:
    """Generate a Markdown table from test results."""
    lines = [
        "### Test Suite Results\n",
        "| Agent | Level | Passed | Failed | Total | Score |",
        "|-------|-------|--------|--------|-------|-------|",
    ]

    for r in test_data.get("results", []):
        total = r.get("total", 0)
        passed = r.get("passed", 0)
        failed = r.get("failed", 0)
        score = 5.0 if total > 0 and passed == total else (
            4.0 if total > 0 and passed / total >= 0.8 else (
                3.0 if total > 0 and passed / total >= 0.6 else (
                    2.0 if total > 0 and passed / total >= 0.4 else 1.0
                )
            )
        )
        lines.append(
            f"| {r['agent']} | {r['level']} | {passed} | {failed} | {total} | {score:.1f} |"
        )

    return "\n".join(lines)


def generate_quality_table(quality_data: dict) -> str:
    """Generate a Markdown table from quality results."""
    lines = [
        "### Code Quality Results\n",
        "| Agent | Level | Ruff Issues | Mypy Errors | Score |",
        "|-------|-------|-------------|-------------|-------|",
    ]

    for r in quality_data.get("results", []):
        ruff = r.get("ruff_issues", "N/A")
        mypy = r.get("mypy_errors", "N/A")
        total = (ruff if isinstance(ruff, int) else 0) + (mypy if isinstance(mypy, int) else 0)
        score = 5.0 if total == 0 else (4.0 if total <= 3 else (3.0 if total <= 10 else 2.0))
        lines.append(f"| {r['agent']} | {r['level']} | {ruff} | {mypy} | {score:.1f} |")

    return "\n".join(lines)


def generate_metrics_table(metrics_data: dict) -> str:
    """Generate a Markdown table from timing metrics."""
    lines = [
        "### Timing and Token Metrics\n",
        "| Agent | Level | Time (min) | Est. Tokens |",
        "|-------|-------|------------|-------------|",
    ]

    for m in metrics_data.get("metrics", []):
        time_str = f"{m['wall_clock_minutes']:.0f}" if m.get("wall_clock_minutes") else "N/A"
        token_str = f"{m['estimated_tokens']:,}" if m.get("estimated_tokens") else "N/A"
        lines.append(f"| {m['agent']} | {m['level']} | {time_str} | {token_str} |")

    return "\n".join(lines)


def generate_summary_table(test_data: dict | None, quality_data: dict | None) -> str:
    """Generate an overall summary table aggregating scores per agent."""
    # Collect all agents
    agents: dict[str, dict[str, float]] = {}

    if test_data:
        for r in test_data.get("results", []):
            agent = r["agent"]
            if agent not in agents:
                agents[agent] = {"test_scores": [], "quality_scores": []}
            total = r.get("total", 0)
            passed = r.get("passed", 0)
            rate = passed / total if total > 0 else 0
            score = 5.0 if rate >= 0.95 else (4.0 if rate >= 0.8 else (3.0 if rate >= 0.6 else 2.0))
            agents[agent]["test_scores"].append(score)

    if quality_data:
        for r in quality_data.get("results", []):
            agent = r["agent"]
            if agent not in agents:
                agents[agent] = {"test_scores": [], "quality_scores": []}
            total_issues = r.get("ruff_issues", 0) + r.get("mypy_errors", 0)
            score = 5.0 if total_issues == 0 else (4.0 if total_issues <= 3 else 3.0)
            agents[agent]["quality_scores"].append(score)

    lines = [
        "### Overall Summary\n",
        "| Agent | Avg Test Score | Avg Quality Score | Combined |",
        "|-------|---------------|-------------------|----------|",
    ]

    for agent, scores in sorted(agents.items()):
        avg_test = (
            sum(scores["test_scores"]) / len(scores["test_scores"])
            if scores["test_scores"] else 0
        )
        avg_qual = (
            sum(scores["quality_scores"]) / len(scores["quality_scores"])
            if scores["quality_scores"] else 0
        )
        combined = (avg_test * 0.6 + avg_qual * 0.4) if avg_test and avg_qual else 0
        lines.append(f"| {agent} | {avg_test:.2f} | {avg_qual:.2f} | {combined:.2f} |")

    return "\n".join(lines)


def main() -> None:
    """Generate the comparison report."""
    test_data = load_json("test_results.json")
    quality_data = load_json("quality_results.json")
    coverage_data = load_json("coverage_results.json")
    metrics_data = load_json("metrics.json")

    report_lines = [
        "# AI Coding Bake-Off: Evaluation Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "---",
        "",
    ]

    if test_data:
        report_lines.append(generate_summary_table(test_data, quality_data))
        report_lines.append("")
        report_lines.append(generate_test_table(test_data))
        report_lines.append("")

    if quality_data:
        report_lines.append(generate_quality_table(quality_data))
        report_lines.append("")

    if metrics_data:
        report_lines.append(generate_metrics_table(metrics_data))
        report_lines.append("")

    if not any([test_data, quality_data, metrics_data]):
        report_lines.append("No evaluation results found. Run `scripts/collect_metrics.py` first.")

    report = "\n".join(report_lines)

    # Write report
    output_path = RESULTS_DIR / "comparison_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(report)

    print(report)
    print(f"\nReport written to {output_path}")


if __name__ == "__main__":
    main()
