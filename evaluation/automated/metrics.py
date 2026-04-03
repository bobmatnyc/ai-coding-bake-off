#!/usr/bin/env python3
"""Collect timing and token metrics from agent metadata files."""

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "harnesses"


@dataclass
class AgentMetrics:
    """Metrics for one agent/level from metadata.json."""

    agent: str
    level: int
    wall_clock_minutes: float | None = None
    estimated_tokens: int | None = None
    start_time: str = ""
    end_time: str = ""
    notes: str = ""


def collect_metrics() -> list[AgentMetrics]:
    """Collect metrics from all agent metadata files."""
    metrics: list[AgentMetrics] = []

    if not AGENTS_DIR.exists():
        return metrics

    for agent_dir in sorted(AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name.startswith("."):
            continue

        for level in range(1, 6):
            metadata_path = agent_dir / "output" / f"level-{level}" / "metadata.json"
            if not metadata_path.exists():
                continue

            try:
                with open(metadata_path) as f:
                    data = json.load(f)

                m = AgentMetrics(
                    agent=agent_dir.name,
                    level=level,
                    wall_clock_minutes=data.get("wall_clock_minutes"),
                    estimated_tokens=data.get("estimated_tokens"),
                    start_time=data.get("start_time", ""),
                    end_time=data.get("end_time", ""),
                    notes=data.get("notes", ""),
                )
                metrics.append(m)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  Warning: Could not parse {metadata_path}: {e}")
            except Exception as e:
                print(f"  Error reading {metadata_path}: {e}")

    return metrics


def analyze_metrics(metrics: list[AgentMetrics]) -> None:
    """Provide analysis of collected metrics."""
    if not metrics:
        print("No metrics to analyze.")
        return

    print("\n=== METRICS ANALYSIS ===")
    
    # Group by agent
    agent_metrics = {}
    for m in metrics:
        if m.agent not in agent_metrics:
            agent_metrics[m.agent] = []
        agent_metrics[m.agent].append(m)
    
    # Calculate averages per agent
    print("\nAgent Averages:")
    print(f"{'Agent':<20} {'Avg Time (min)':<15} {'Avg Tokens':<15} {'Levels Completed':<15}")
    print("-" * 65)
    
    for agent, agent_data in agent_metrics.items():
        times = [m.wall_clock_minutes for m in agent_data if m.wall_clock_minutes is not None]
        tokens = [m.estimated_tokens for m in agent_data if m.estimated_tokens is not None]
        
        avg_time = sum(times) / len(times) if times else 0
        avg_tokens = sum(tokens) / len(tokens) if tokens else 0
        levels_completed = len(agent_data)
        
        print(f"{agent:<20} {avg_time:<15.1f} {avg_tokens:<15.0f} {levels_completed:<15}")


def main() -> None:
    """Collect and report metrics."""
    metrics = collect_metrics()

    if not metrics:
        print("No metadata.json files found in agent directories.")
        sys.exit(0)

    print(f"{'Agent':<20} {'Level':<8} {'Time (min)':<12} {'Tokens':<12} {'Notes'}")
    print("-" * 80)

    for m in metrics:
        time_str = f"{m.wall_clock_minutes:.0f}" if m.wall_clock_minutes else "N/A"
        token_str = f"{m.estimated_tokens:,}" if m.estimated_tokens else "N/A"
        notes = (m.notes[:30] + "...") if len(m.notes) > 30 else m.notes
        print(f"{m.agent:<20} {m.level:<8} {time_str:<12} {token_str:<12} {notes}")

    # Provide analysis
    analyze_metrics(metrics)

    # Write report
    output_path = PROJECT_ROOT / "evaluation" / "results" / "metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "metrics": [asdict(m) for m in metrics],
            },
            f,
            indent=2,
        )

    print(f"\nReport written to {output_path}")


if __name__ == "__main__":
    main()
