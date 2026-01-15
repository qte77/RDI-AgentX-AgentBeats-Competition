#!/usr/bin/env python3
"""Script to test reproducibility of evaluation results across multiple runs."""

from __future__ import annotations

import asyncio
import json
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentbeats.agent import Agent, EvalRequest


async def run_single_evaluation(agent_url: str, run_number: int) -> dict[str, float | int | str]:
    """Run a single evaluation and extract numeric metrics.

    Args:
        agent_url: URL of the agent to evaluate
        run_number: Run identifier for logging

    Returns:
        Dictionary of numeric metrics
    """
    # Create evaluation request (same as evaluate_purple_agent.py)
    request = EvalRequest(
        agent_url=agent_url,
        messages=[
            "Hello, can you help me coordinate a task?",
            "What are your coordination capabilities?",
            "How would you handle a multi-agent scenario?",
        ],
    )

    # Run evaluation
    agent = Agent()
    print(f"[Run {run_number}] Starting evaluation at {datetime.now(UTC).isoformat()}")
    result = await agent.run(request)

    # Extract numeric metrics
    metrics: dict[str, float | int | str] = {
        "run_number": run_number,
        "status": result.status,
        "duration_seconds": result.duration_seconds,
        "task_id": result.task_id,
    }

    # Add tier-specific metrics
    if result.results:
        # Tier 1: Graph metrics
        if "tier1_graph" in result.results:
            tier1 = result.results["tier1_graph"]
            if "error" not in tier1:
                metrics["graph_node_count"] = tier1.get("node_count", 0)
                metrics["graph_edge_count"] = tier1.get("edge_count", 0)
                metrics["graph_avg_centrality"] = tier1.get("average_centrality", 0.0)

        # Tier 2: LLM judge
        if "tier2_llm_judge" in result.results:
            tier2 = result.results["tier2_llm_judge"]
            if "error" not in tier2:
                metrics["coordination_quality_score"] = tier2.get("quality_score", 0.0)

        # Tier 3: Text metrics
        if "tier3_text_metrics" in result.results:
            tier3 = result.results["tier3_text_metrics"]
            if "error" not in tier3:
                metrics["response_similarity_score"] = tier3.get("similarity_score", 0.0)

    print(f"[Run {run_number}] Completed: {metrics}")
    return metrics


async def test_reproducibility(agent_url: str, num_runs: int = 5, output_file: Path | None = None) -> dict:
    """Run multiple evaluations and compute variance statistics.

    Args:
        agent_url: URL of the agent to evaluate
        num_runs: Number of evaluation runs to perform
        output_file: Optional path to write results JSON

    Returns:
        Dictionary containing all runs and variance analysis
    """
    print("=" * 80)
    print("REPRODUCIBILITY TEST")
    print("=" * 80)
    print(f"Agent URL: {agent_url}")
    print(f"Number of runs: {num_runs}")
    print(f"Start time: {datetime.now(UTC).isoformat()}")
    print()

    # Run evaluations
    all_runs = []
    for i in range(1, num_runs + 1):
        try:
            metrics = await run_single_evaluation(agent_url, i)
            all_runs.append(metrics)
            print()
        except Exception as e:
            print(f"[Run {i}] ERROR: {e}")
            all_runs.append({"run_number": i, "error": str(e)})
            print()

    # Compute statistics for numeric metrics
    numeric_keys = [
        "duration_seconds",
        "graph_node_count",
        "graph_edge_count",
        "graph_avg_centrality",
        "coordination_quality_score",
        "response_similarity_score",
    ]

    variance_analysis = {}
    for key in numeric_keys:
        values = [run[key] for run in all_runs if key in run and isinstance(run[key], (int, float))]

        if len(values) >= 2:
            variance_analysis[key] = {
                "mean": statistics.mean(values),
                "stdev": statistics.stdev(values),
                "min": min(values),
                "max": max(values),
                "range": max(values) - min(values),
                "num_samples": len(values),
                "values": values,
            }

    # Create final report
    report = {
        "test_timestamp": datetime.now(UTC).isoformat(),
        "agent_url": agent_url,
        "num_runs": num_runs,
        "successful_runs": len([r for r in all_runs if "error" not in r]),
        "failed_runs": len([r for r in all_runs if "error" in r]),
        "all_runs": all_runs,
        "variance_analysis": variance_analysis,
    }

    # Write to file if specified
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w") as f:
            json.dump(report, f, indent=2)
        print(f"Results written to {output_file}")

    return report


def print_variance_summary(report: dict) -> None:
    """Print a human-readable summary of variance analysis."""
    print()
    print("=" * 80)
    print("VARIANCE ANALYSIS SUMMARY")
    print("=" * 80)
    print()
    print(f"Successful runs: {report['successful_runs']}/{report['num_runs']}")
    print()

    for metric, stats in report["variance_analysis"].items():
        print(f"{metric}:")
        print(f"  Mean:     {stats['mean']:.4f}")
        print(f"  Std Dev:  {stats['stdev']:.4f}")
        print(f"  Range:    {stats['min']:.4f} - {stats['max']:.4f}")
        print(f"  Span:     {stats['range']:.4f}")
        print(f"  Values:   {stats['values']}")

        # Coefficient of variation (CV) for relative variability
        if stats["mean"] != 0:
            cv = (stats["stdev"] / stats["mean"]) * 100
            print(f"  CV:       {cv:.2f}%")

        print()


def main() -> None:
    """Main entry point for reproducibility testing."""
    # Configuration
    agent_url = "http://localhost:9010"  # Purple agent URL
    num_runs = 5  # Default: 5 runs
    output_dir = Path("reproducibility-results")

    # Parse command line arguments
    if len(sys.argv) > 1:
        agent_url = sys.argv[1]
    if len(sys.argv) > 2:
        num_runs = int(sys.argv[2])

    # Generate output filename with timestamp
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"reproducibility-{timestamp}.json"

    # Run reproducibility test
    try:
        report = asyncio.run(test_reproducibility(agent_url, num_runs, output_file))
        print_variance_summary(report)

        # Check for high variability (CV > 10%)
        high_variance_metrics = []
        for metric, stats in report["variance_analysis"].items():
            if stats["mean"] != 0:
                cv = (stats["stdev"] / stats["mean"]) * 100
                if cv > 10:
                    high_variance_metrics.append((metric, cv))

        if high_variance_metrics:
            print()
            print("⚠️  WARNING: High variance detected in:")
            for metric, cv in high_variance_metrics:
                print(f"  - {metric}: {cv:.2f}% CV")
            print()
        else:
            print()
            print("✅ All metrics show low variance (CV < 10%)")
            print()

        print(f"Full report: {output_file}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Reproducibility test failed: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
