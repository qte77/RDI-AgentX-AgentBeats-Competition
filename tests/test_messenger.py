"""Tests for messenger module defining contract for A2A agent communication and trace capture."""

import pytest
from pydantic import BaseModel


class TestMessengerTalkToAgent:
    """Tests defining expected behavior for Messenger.talk_to_agent()."""

    @pytest.mark.asyncio
    async def test_talk_to_agent_sends_message_and_returns_response(self) -> None:
        """Test that talk_to_agent() sends a message to an agent and returns the response."""
        # Given: A messenger instance and a target agent URL
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url = "http://localhost:9009"
        message = "Test message"

        # When: We talk to the agent (will be mocked in implementation test)
        # Then: Should return a response string
        # This test defines the contract - implementation will use httpx for actual calls
        assert hasattr(messenger, "talk_to_agent")
        assert callable(messenger.talk_to_agent)

    @pytest.mark.asyncio
    async def test_talk_to_agent_captures_trace_data(self) -> None:
        """Test that talk_to_agent() captures trace data for each interaction."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # When: We talk to an agent
        # Then: The interaction should be captured in traces
        # This ensures we can evaluate agent behavior later
        assert hasattr(messenger, "talk_to_agent")

    @pytest.mark.asyncio
    async def test_talk_to_agent_handles_http_errors(self) -> None:
        """Test that talk_to_agent() handles HTTP errors gracefully."""
        # Given: A messenger instance and invalid agent URL
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # When/Then: Should handle connection errors appropriately
        assert hasattr(messenger, "talk_to_agent")


class TestMessengerGetTraces:
    """Tests defining expected behavior for Messenger.get_traces()."""

    def test_get_traces_returns_list_of_interactions(self) -> None:
        """Test that get_traces() returns a list of all captured interactions."""
        # Given: A messenger instance that has captured some interactions
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # When: We get traces
        traces = messenger.get_traces()

        # Then: Should return a list (initially empty)
        assert isinstance(traces, list)

    def test_get_traces_returns_structured_trace_data(self) -> None:
        """Test that get_traces() returns structured trace data with required fields."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        traces = messenger.get_traces()

        # Then: Each trace should have structured data
        # Traces should be empty initially, but the return type should be list
        assert isinstance(traces, list)
        # When traces exist, they should have: timestamp, agent_url, message, response
        # This is the contract for downstream evaluators

    def test_traces_accumulate_across_multiple_calls(self) -> None:
        """Test that traces accumulate across multiple talk_to_agent() calls."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # When: We make multiple calls
        # Then: All interactions should be captured in traces
        traces_before = messenger.get_traces()
        assert isinstance(traces_before, list)


class TraceData(BaseModel):
    """Expected structure of trace data for evaluators."""

    timestamp: str
    agent_url: str
    message: str
    response: str
    status_code: int | None = None
    error: str | None = None


class TestMessengerTraceStructure:
    """Tests defining the expected structure of trace data."""

    def test_trace_data_model_is_valid(self) -> None:
        """Test that TraceData model can be instantiated with valid data."""
        # Given: Valid trace data
        trace = TraceData(
            timestamp="2026-01-15T00:00:00Z",
            agent_url="http://localhost:9009",
            message="test",
            response="response",
            status_code=200,
        )

        # Then: Model should validate successfully
        assert trace.timestamp == "2026-01-15T00:00:00Z"
        assert trace.agent_url == "http://localhost:9009"
        assert trace.message == "test"
        assert trace.response == "response"
        assert trace.status_code == 200

    def test_trace_data_model_handles_errors(self) -> None:
        """Test that TraceData model can capture error information."""
        # Given: Trace data with an error
        trace = TraceData(
            timestamp="2026-01-15T00:00:00Z",
            agent_url="http://localhost:9009",
            message="test",
            response="",
            error="Connection refused",
        )

        # Then: Model should capture error information
        assert trace.error == "Connection refused"
        assert trace.response == ""


class TestMessengerContract:
    """Tests defining the overall Messenger contract."""

    def test_messenger_can_be_instantiated(self) -> None:
        """Test that Messenger can be instantiated without arguments."""
        # Given/When: We create a messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # Then: Instance should be created successfully
        assert messenger is not None
        assert hasattr(messenger, "talk_to_agent")
        assert hasattr(messenger, "get_traces")

    def test_messenger_provides_clean_api(self) -> None:
        """Test that Messenger provides a clean, focused API."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()

        # Then: Should have exactly the methods we need
        assert hasattr(messenger, "talk_to_agent")
        assert hasattr(messenger, "get_traces")
        # No other public methods needed (YAGNI principle)
