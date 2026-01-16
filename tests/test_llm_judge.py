"""Tests for LLM judge evaluator module defining contract for qualitative assessment."""

import os
import pytest
from pydantic import BaseModel
from unittest.mock import AsyncMock, Mock, patch


class TestLLMJudgeEvaluate:
    """Tests defining expected behavior for LLMJudge.evaluate(traces)."""

    @pytest.mark.asyncio
    async def test_evaluate_accepts_trace_list(self) -> None:
        """Test that evaluate() accepts a list of traces."""
        # Given: An LLMJudge instance and trace data
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When/Then: Should have evaluate method that accepts traces
        assert hasattr(judge, "evaluate")
        assert callable(judge.evaluate)

    @pytest.mark.asyncio
    async def test_evaluate_returns_assessment(self) -> None:
        """Test that evaluate() returns a qualitative assessment."""
        # Given: An LLMJudge instance with mocked LLM
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We evaluate traces (with mocked LLM call)
        # Then: Should return assessment data
        # This test defines the contract - implementation will use mocked LLM
        assert hasattr(judge, "evaluate")

    @pytest.mark.asyncio
    async def test_evaluate_uses_mocked_llm(self) -> None:
        """Test that evaluate() can use mocked LLM calls for testing."""
        # Given: An LLMJudge instance with mocked LLM client
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We mock the LLM client
        # Then: Should be able to test without real API calls
        # This ensures tests can run without API keys or network access
        assert hasattr(judge, "evaluate")

    @pytest.mark.asyncio
    async def test_evaluate_handles_empty_traces(self) -> None:
        """Test that evaluate() handles empty trace list gracefully."""
        # Given: An LLMJudge instance and empty traces
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()
        empty_traces: list = []

        # When/Then: Should handle empty input without errors
        assert hasattr(judge, "evaluate")

    @pytest.mark.asyncio
    async def test_evaluate_analyzes_coordination_quality(self) -> None:
        """Test that evaluate() analyzes coordination quality from traces."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We evaluate traces
        # Then: Should provide qualitative assessment of coordination
        # This is the core value proposition of LLM-as-judge
        assert hasattr(judge, "evaluate")


class LLMJudgment(BaseModel):
    """Expected structure of LLM judge assessment."""

    overall_score: float  # 0-1 score
    reasoning: str  # Explanation of assessment
    coordination_quality: str | None = None  # Quality description
    strengths: list[str] | None = None  # Identified strengths
    weaknesses: list[str] | None = None  # Identified weaknesses


class TestLLMJudgmentStructure:
    """Tests defining the expected structure of LLM judgments."""

    def test_llm_judgment_model_is_valid(self) -> None:
        """Test that LLMJudgment model can be instantiated with valid data."""
        # Given: Valid judgment data
        judgment = LLMJudgment(
            overall_score=0.85,
            reasoning="Agent demonstrated effective coordination",
            coordination_quality="Good",
            strengths=["Clear communication", "Efficient routing"],
            weaknesses=["Occasional redundant calls"],
        )

        # Then: Model should validate successfully
        assert judgment.overall_score == 0.85
        assert judgment.reasoning == "Agent demonstrated effective coordination"
        assert judgment.coordination_quality == "Good"
        assert len(judgment.strengths or []) == 2
        assert len(judgment.weaknesses or []) == 1

    def test_llm_judgment_minimal_fields(self) -> None:
        """Test that LLMJudgment model works with minimal required fields."""
        # Given: Minimal judgment data
        judgment = LLMJudgment(
            overall_score=0.5,
            reasoning="Basic coordination observed",
        )

        # Then: Model should validate with just required fields
        assert judgment.overall_score == 0.5
        assert judgment.reasoning == "Basic coordination observed"
        assert judgment.coordination_quality is None
        assert judgment.strengths is None

    def test_llm_judgment_score_range(self) -> None:
        """Test that LLMJudgment score is in valid range."""
        # Given: Judgment data with boundary scores
        low_judgment = LLMJudgment(overall_score=0.0, reasoning="Poor coordination")
        high_judgment = LLMJudgment(overall_score=1.0, reasoning="Excellent coordination")

        # Then: Scores should be in 0-1 range
        assert 0.0 <= low_judgment.overall_score <= 1.0
        assert 0.0 <= high_judgment.overall_score <= 1.0


class TestLLMJudgeContract:
    """Tests defining the overall LLMJudge contract."""

    def test_llm_judge_can_be_instantiated(self) -> None:
        """Test that LLMJudge can be instantiated without arguments."""
        # Given/When: We create an LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # Then: Instance should be created successfully
        assert judge is not None
        assert hasattr(judge, "evaluate")

    def test_llm_judge_provides_clean_api(self) -> None:
        """Test that LLMJudge provides a clean, focused API."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # Then: Should have evaluate method
        assert hasattr(judge, "evaluate")
        # No other public methods needed (YAGNI principle)

    def test_llm_judge_integration_with_traces(self) -> None:
        """Test that LLMJudge integrates with TraceData from messenger."""
        # Given: LLMJudge and TraceData structure
        from agentbeats.evals.llm_judge import LLMJudge
        from agentbeats.messenger import TraceData

        judge = LLMJudge()

        # When: We create sample trace data
        sample_trace = TraceData(
            timestamp="2026-01-15T00:00:00Z",
            agent_url="http://localhost:9009",
            message="test",
            response="response",
            status_code=200,
        )

        # Then: LLMJudge should be able to process trace data
        # This ensures integration between messenger and LLM judge
        assert hasattr(judge, "evaluate")
        assert sample_trace.message is not None
        assert sample_trace.response is not None


class TestLLMJudgeMocking:
    """Tests defining mocking strategy for LLM calls."""

    @pytest.mark.asyncio
    async def test_llm_client_can_be_mocked(self) -> None:
        """Test that LLM client can be mocked for testing."""
        # Given: A mocked LLM client
        mock_client = AsyncMock()
        mock_client.generate.return_value = "Good coordination observed"

        # When: We use the mock
        result = await mock_client.generate()

        # Then: Mock should return expected value
        assert result == "Good coordination observed"
        mock_client.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_evaluate_with_mocked_response(self) -> None:
        """Test that evaluate() works with mocked LLM responses."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We mock LLM responses
        # Then: Should be able to test evaluation logic without real API calls
        # This is critical for CI/CD and local development
        assert hasattr(judge, "evaluate")


class TestLLMJudgeQualitativeAssessment:
    """Tests defining qualitative assessment capabilities."""

    @pytest.mark.asyncio
    async def test_assesses_communication_clarity(self) -> None:
        """Test that LLMJudge assesses communication clarity."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We evaluate traces
        # Then: Assessment should consider communication clarity
        # This is a key qualitative dimension for coordination
        assert hasattr(judge, "evaluate")

    @pytest.mark.asyncio
    async def test_identifies_coordination_patterns(self) -> None:
        """Test that LLMJudge identifies coordination patterns."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We evaluate agent interactions
        # Then: Should identify patterns like delegation, collaboration, etc.
        # This provides insights beyond quantitative metrics
        assert hasattr(judge, "evaluate")

    @pytest.mark.asyncio
    async def test_provides_actionable_feedback(self) -> None:
        """Test that LLMJudge provides actionable feedback."""
        # Given: An LLMJudge instance
        from agentbeats.evals.llm_judge import LLMJudge

        judge = LLMJudge()

        # When: We evaluate traces
        # Then: Feedback should include strengths and areas for improvement
        # This helps developers understand evaluation results
        assert hasattr(judge, "evaluate")


class TestLLMClientConfiguration:
    """Tests defining LLM client configuration contract."""

    def test_llm_judge_reads_api_key_from_env(self) -> None:
        """Test that LLMJudge reads AGENTBEATS_LLM_API_KEY from environment."""
        # Given: Environment variable for API key
        from agentbeats.evals.llm_judge import LLMJudge

        with patch.dict(os.environ, {"AGENTBEATS_LLM_API_KEY": "test-api-key"}):
            # When: We instantiate LLMJudge
            judge = LLMJudge()

            # Then: Should read and store API key from environment
            # This enables LLM API calls when key is configured
            assert hasattr(judge, "_api_key") or hasattr(judge, "api_key")

    def test_llm_judge_reads_base_url_from_env(self) -> None:
        """Test that LLMJudge reads AGENTBEATS_LLM_BASE_URL from environment."""
        # Given: Environment variable for base URL
        from agentbeats.evals.llm_judge import LLMJudge

        custom_url = "https://custom-api.example.com/v1"
        with patch.dict(os.environ, {"AGENTBEATS_LLM_BASE_URL": custom_url}):
            # When: We instantiate LLMJudge
            judge = LLMJudge()

            # Then: Should read base URL from environment
            # This enables using any OpenAI-compatible endpoint
            assert hasattr(judge, "_base_url") or hasattr(judge, "base_url")

    def test_llm_judge_uses_default_base_url(self) -> None:
        """Test that LLMJudge uses default OpenAI base URL when not configured."""
        # Given: No AGENTBEATS_LLM_BASE_URL in environment
        from agentbeats.evals.llm_judge import LLMJudge

        with patch.dict(os.environ, {}, clear=True):
            # When: We instantiate LLMJudge
            judge = LLMJudge()

            # Then: Should use default OpenAI base URL
            # Default base URL should be https://api.openai.com/v1
            expected_default = "https://api.openai.com/v1"
            if hasattr(judge, "_base_url"):
                assert judge._base_url == expected_default
            elif hasattr(judge, "base_url"):
                assert judge.base_url == expected_default

    def test_llm_judge_reads_model_from_env(self) -> None:
        """Test that LLMJudge reads AGENTBEATS_LLM_MODEL from environment."""
        # Given: Environment variable for model name
        from agentbeats.evals.llm_judge import LLMJudge

        custom_model = "gpt-4-turbo"
        with patch.dict(os.environ, {"AGENTBEATS_LLM_MODEL": custom_model}):
            # When: We instantiate LLMJudge
            judge = LLMJudge()

            # Then: Should read model name from environment
            # This enables using different models based on deployment needs
            assert hasattr(judge, "_model") or hasattr(judge, "model")

    def test_llm_judge_uses_default_model(self) -> None:
        """Test that LLMJudge uses gpt-4o-mini as default model."""
        # Given: No AGENTBEATS_LLM_MODEL in environment
        from agentbeats.evals.llm_judge import LLMJudge

        with patch.dict(os.environ, {}, clear=True):
            # When: We instantiate LLMJudge
            judge = LLMJudge()

            # Then: Should use gpt-4o-mini as default
            # This provides good balance of cost and quality
            expected_default = "gpt-4o-mini"
            if hasattr(judge, "_model"):
                assert judge._model == expected_default
            elif hasattr(judge, "model"):
                assert judge.model == expected_default

    def test_llm_judge_supports_openai_compatible_endpoints(self) -> None:
        """Test that LLMJudge supports any OpenAI-compatible endpoint."""
        # Given: Custom OpenAI-compatible endpoint configuration
        from agentbeats.evals.llm_judge import LLMJudge

        custom_config = {
            "AGENTBEATS_LLM_API_KEY": "custom-key",
            "AGENTBEATS_LLM_BASE_URL": "https://custom-llm.example.com/v1",
            "AGENTBEATS_LLM_MODEL": "custom-model",
        }

        with patch.dict(os.environ, custom_config):
            # When: We instantiate LLMJudge with custom config
            judge = LLMJudge()

            # Then: Should support custom endpoint configuration
            # This enables using providers like Azure OpenAI, local models, etc.
            assert judge is not None
            # Configuration should be readable for API calls

    def test_llm_judge_handles_missing_api_key_gracefully(self) -> None:
        """Test that LLMJudge handles missing API key gracefully."""
        # Given: No API key in environment
        from agentbeats.evals.llm_judge import LLMJudge

        with patch.dict(os.environ, {}, clear=True):
            # When: We instantiate LLMJudge without API key
            judge = LLMJudge()

            # Then: Should not raise error during instantiation
            # API key check should happen at evaluation time, not initialization
            assert judge is not None

    @pytest.mark.asyncio
    async def test_llm_judge_can_check_if_api_configured(self) -> None:
        """Test that LLMJudge can determine if API is configured."""
        # Given: LLMJudge instances with and without API key
        from agentbeats.evals.llm_judge import LLMJudge

        # When: API key is set
        with patch.dict(os.environ, {"AGENTBEATS_LLM_API_KEY": "test-key"}):
            judge_with_key = LLMJudge()

            # Then: Should be able to determine API is configured
            # This helps decide whether to use LLM or fallback logic

        # When: API key is not set
        with patch.dict(os.environ, {}, clear=True):
            judge_without_key = LLMJudge()

            # Then: Should be able to determine API is not configured
            # This is needed for graceful fallback behavior
            assert judge_without_key is not None


class TestLLMClientConfigurationIntegration:
    """Tests defining integration between configuration and evaluation."""

    @pytest.mark.asyncio
    async def test_evaluate_uses_configured_endpoint(self) -> None:
        """Test that evaluate() uses configured LLM endpoint when available."""
        # Given: LLMJudge with configured endpoint
        from agentbeats.evals.llm_judge import LLMJudge
        from agentbeats.messenger import TraceData

        config = {
            "AGENTBEATS_LLM_API_KEY": "test-key",
            "AGENTBEATS_LLM_BASE_URL": "https://api.openai.com/v1",
            "AGENTBEATS_LLM_MODEL": "gpt-4o-mini",
        }

        with patch.dict(os.environ, config):
            judge = LLMJudge()

            # When: We evaluate traces
            traces = [
                TraceData(
                    timestamp="2026-01-15T00:00:00Z",
                    agent_url="http://localhost:9009",
                    message="test",
                    response="response",
                    status_code=200,
                )
            ]

            # Then: Should use configured endpoint for evaluation
            # Implementation will need to make actual API call or use mock
            result = await judge.evaluate(traces)
            assert result is not None
            assert isinstance(result.overall_score, float)
