#!/usr/bin/env python3
"""Script to evaluate purple agent and generate leaderboard results."""

from __future__ import annotations

import asyncio
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentbeats.agent import Agent, EvalRequest


async def evaluate_purple_agent(agent_url: str, output_file: Path | None = None) -> dict:
    """Evaluate purple agent and generate results in leaderboard format.

    Args:
        agent_url: URL of the purple agent to evaluate
        output_file: Optional path to write results JSON

    Returns:
        Dictionary containing evaluation results
    """
    # Create evaluation request
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
    print(f"Evaluating agent at {agent_url}...")
    result = await agent.run(request)

    # Generate leaderboard-compatible results
    purple_agent_id = str(uuid.uuid4())  # Generate UUID for purple agent
    timestamp = datetime.now(UTC).isoformat()

    # Extract metrics from evaluation results
    leaderboard_result = {
        "agent_id": purple_agent_id,
        "agent_url": agent_url,
        "evaluation_timestamp": timestamp,
        "task_id": result.task_id,
        "status": result.status,
        "duration_seconds": result.duration_seconds,
        "metrics": {},
    }

    # Add tier-specific metrics if evaluation succeeded
    if result.results:
        # Tier 1: Graph metrics
        if "tier1_graph" in result.results:
            tier1 = result.results["tier1_graph"]
            if "error" not in tier1:
                leaderboard_result["metrics"]["graph_node_count"] = tier1.get("node_count", 0)
                leaderboard_result["metrics"]["graph_edge_count"] = tier1.get("edge_count", 0)
                leaderboard_result["metrics"]["graph_avg_centrality"] = tier1.get("average_centrality", 0.0)
            else:
                leaderboard_result["metrics"]["graph_error"] = tier1.get("error")

        # Tier 2: LLM judge
        if "tier2_llm_judge" in result.results:
            tier2 = result.results["tier2_llm_judge"]
            if "error" not in tier2:
                leaderboard_result["metrics"]["coordination_quality_score"] = tier2.get("quality_score", 0.0)
                leaderboard_result["metrics"]["coordination_assessment"] = tier2.get("assessment", "")
            else:
                leaderboard_result["metrics"]["llm_judge_error"] = tier2.get("error")

        # Tier 3: Text metrics
        if "tier3_text_metrics" in result.results:
            tier3 = result.results["tier3_text_metrics"]
            if "error" not in tier3:
                leaderboard_result["metrics"]["response_similarity_score"] = tier3.get("similarity_score", 0.0)
            else:
                leaderboard_result["metrics"]["text_metrics_error"] = tier3.get("error")

    # Add error if evaluation failed
    if result.error:
        leaderboard_result["error"] = result.error

    # Write to file if specified
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w") as f:
            json.dump(leaderboard_result, f, indent=2)
        print(f"Results written to {output_file}")

    return leaderboard_result


def main() -> None:
    """Main entry point for evaluation script."""
    # Default configuration
    agent_url = "http://localhost:9010"  # Default purple agent URL
    output_dir = Path("leaderboard-results")

    # Generate output filename with timestamp
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"purple-agent-{timestamp}.json"

    # Parse command line arguments
    if len(sys.argv) > 1:
        agent_url = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])

    print("Purple Agent Evaluation Script")
    print("================================")
    print(f"Agent URL: {agent_url}")
    print(f"Output: {output_file}")
    print()

    # Run evaluation
    try:
        result = asyncio.run(evaluate_purple_agent(agent_url, output_file))
        print()
        print("Evaluation Results:")
        print(json.dumps(result, indent=2))
        print()
        print("✅ Evaluation completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
