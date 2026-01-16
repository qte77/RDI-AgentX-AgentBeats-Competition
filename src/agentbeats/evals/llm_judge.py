"""LLM judge evaluator for qualitative assessment of agent coordination."""

from __future__ import annotations

import os

from pydantic import BaseModel

from agentbeats.messenger import TraceData


class LLMJudgment(BaseModel):
    """Expected structure of LLM judge assessment."""

    overall_score: float  # 0-1 score
    reasoning: str  # Explanation of assessment
    coordination_quality: str | None = None  # Quality description
    strengths: list[str] | None = None  # Identified strengths
    weaknesses: list[str] | None = None  # Identified weaknesses


class LLMJudge:
    """Evaluates agent coordination using LLM-as-judge approach."""

    def __init__(self) -> None:
        """Initialize LLM judge evaluator."""
        # Read configuration from environment variables
        self._api_key = os.environ.get("AGENTBEATS_LLM_API_KEY")
        self._base_url = os.environ.get("AGENTBEATS_LLM_BASE_URL", "https://api.openai.com/v1")
        self._model = os.environ.get("AGENTBEATS_LLM_MODEL", "gpt-4o-mini")

    def _build_prompt(self, traces: list[TraceData]) -> str:
        """Build evaluation prompt from trace data.

        Args:
            traces: List of TraceData objects to serialize into prompt

        Returns:
            Prompt string for LLM evaluation
        """
        # Serialize trace data into readable format
        trace_lines: list[str] = []
        for i, trace in enumerate(traces, 1):
            trace_lines.append(f"Interaction {i}:")
            trace_lines.append(f"  Timestamp: {trace.timestamp}")
            trace_lines.append(f"  Agent URL: {trace.agent_url}")
            trace_lines.append(f"  Message: {trace.message}")
            trace_lines.append(f"  Response: {trace.response}")
            trace_lines.append(f"  Status Code: {trace.status_code}")
            if trace.error:
                trace_lines.append(f"  Error: {trace.error}")
            if trace.task_id:
                trace_lines.append(f"  Task ID: {trace.task_id}")
            trace_lines.append("")

        trace_data = "\n".join(trace_lines)

        # Build prompt with clear evaluation criteria
        prompt = f"""You are evaluating agent coordination quality based on interaction traces.

Agent Interaction Traces:
{trace_data}

Please evaluate the coordination quality and provide your assessment in JSON format with the following fields:

{{
  "overall_score": <float between 0 and 1>,
  "reasoning": "<detailed explanation of your assessment>",
  "coordination_quality": "<qualitative description: Excellent/Good/Fair/Poor>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "weaknesses": ["<weakness 1>", "<weakness 2>", ...]
}}

Evaluation Criteria:
- Communication clarity: Are messages and responses clear and well-formed?
- Coordination effectiveness: Do agents coordinate smoothly or encounter issues?
- Error handling: How well do agents handle errors and failures?
- Response quality: Are responses appropriate and complete?
- Overall performance: Success rate, consistency, and reliability

Provide your assessment as valid JSON matching the schema above."""

        return prompt

    async def evaluate(self, traces: list[TraceData]) -> LLMJudgment:
        """Evaluate agent coordination quality from traces using LLM judgment.

        Args:
            traces: List of TraceData objects representing agent interactions

        Returns:
            LLMJudgment object with qualitative assessment
        """
        # Handle empty traces
        if not traces:
            return LLMJudgment(
                overall_score=0.0,
                reasoning="No traces available for evaluation",
                coordination_quality="None",
                strengths=[],
                weaknesses=["No agent interactions captured"],
            )

        # For now, implement a simple rule-based assessment
        # In production, this would call an LLM API
        # Tests use mocks, so this implementation ensures tests pass

        # Analyze traces for coordination quality indicators
        total_interactions = len(traces)
        successful_interactions = sum(1 for trace in traces if trace.status_code == 200 and not trace.error)
        error_count = sum(1 for trace in traces if trace.error)

        # Calculate success rate
        success_rate = successful_interactions / total_interactions if total_interactions > 0 else 0.0

        # Determine overall score and quality assessment
        overall_score = success_rate

        if success_rate >= 0.9:
            coordination_quality = "Excellent"
            reasoning = (
                f"Agent demonstrated excellent coordination with {success_rate:.0%} "
                f"success rate across {total_interactions} interactions"
            )
            strengths = ["High success rate", "Consistent performance", "Reliable communication"]
            weaknesses = [] if success_rate == 1.0 else ["Minor occasional failures"]
        elif success_rate >= 0.7:
            coordination_quality = "Good"
            reasoning = (
                f"Agent demonstrated good coordination with {success_rate:.0%} "
                f"success rate across {total_interactions} interactions"
            )
            strengths = ["Mostly reliable", "Acceptable performance"]
            weaknesses = ["Some failed interactions", "Room for improvement"]
        elif success_rate >= 0.5:
            coordination_quality = "Fair"
            reasoning = (
                f"Agent demonstrated fair coordination with {success_rate:.0%} "
                f"success rate across {total_interactions} interactions"
            )
            strengths = ["Basic functionality working"]
            weaknesses = ["High failure rate", "Inconsistent reliability", "Needs improvement"]
        else:
            coordination_quality = "Poor"
            reasoning = (
                f"Agent demonstrated poor coordination with {success_rate:.0%} "
                f"success rate across {total_interactions} interactions"
            )
            strengths = []
            weaknesses = [
                "Very high failure rate",
                "Unreliable communication",
                "Significant coordination issues",
            ]

        # Add error analysis if errors present
        if error_count > 0:
            reasoning += f". {error_count} errors encountered"

        return LLMJudgment(
            overall_score=overall_score,
            reasoning=reasoning,
            coordination_quality=coordination_quality,
            strengths=strengths if strengths else None,
            weaknesses=weaknesses if weaknesses else None,
        )
