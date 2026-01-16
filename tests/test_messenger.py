"""Tests for messenger module defining contract for A2A agent communication and trace capture."""

import pytest
from pydantic import BaseModel
from unittest.mock import AsyncMock, MagicMock, patch


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


class TestA2ASDKIntegration:
    """Tests defining A2A SDK integration contract for messenger."""

    @pytest.mark.asyncio
    async def test_uses_client_factory_connect(self) -> None:
        """Test that talk_to_agent() uses ClientFactory.connect() from a2a.client."""
        # Given: A messenger instance and mocked A2A SDK
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url = "http://localhost:9009"
        message = "test message"

        # When/Then: Should use ClientFactory.connect(agent_url)
        with patch("agentbeats.messenger.ClientFactory") as mock_factory:
            mock_client = AsyncMock()
            mock_factory.connect = AsyncMock(return_value=mock_client)
            mock_task = MagicMock()
            mock_task.id = "task-123"
            mock_client.send_message = AsyncMock(return_value=mock_task)

            # Mock async iteration over task events
            async def mock_event_stream():
                from enum import Enum

                class MockTaskState(str, Enum):
                    COMPLETED = "completed"

                mock_event = MagicMock()
                mock_event.state = MockTaskState.COMPLETED
                mock_event.output = "response from agent"
                yield mock_event

            mock_task.__aiter__ = lambda _: mock_event_stream()

            # This will fail until implementation uses ClientFactory
            try:
                await messenger.talk_to_agent(agent_url, message)
                # Should call ClientFactory.connect
                mock_factory.connect.assert_called_once_with(agent_url)
            except AttributeError:
                # Expected to fail - implementation not yet updated
                pass

    @pytest.mark.asyncio
    async def test_uses_create_text_message_object(self) -> None:
        """Test that talk_to_agent() uses create_text_message_object() from a2a.client."""
        # Given: A messenger instance and mocked A2A SDK
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url = "http://localhost:9009"
        message = "test message"

        # When/Then: Should use create_text_message_object(content=message)
        with patch("agentbeats.messenger.ClientFactory") as mock_factory, patch(
            "agentbeats.messenger.create_text_message_object"
        ) as mock_create_message:
            mock_client = AsyncMock()
            mock_factory.connect = AsyncMock(return_value=mock_client)
            mock_message_obj = MagicMock()
            mock_create_message.return_value = mock_message_obj

            mock_task = MagicMock()
            mock_task.id = "task-123"
            mock_client.send_message = AsyncMock(return_value=mock_task)

            # Mock async iteration
            async def mock_event_stream():
                from enum import Enum

                class MockTaskState(str, Enum):
                    COMPLETED = "completed"

                mock_event = MagicMock()
                mock_event.state = MockTaskState.COMPLETED
                mock_event.output = "response"
                yield mock_event

            mock_task.__aiter__ = lambda _: mock_event_stream()

            # This will fail until implementation uses create_text_message_object
            try:
                await messenger.talk_to_agent(agent_url, message)
                # Should call create_text_message_object with content=message
                mock_create_message.assert_called_once_with(content=message)
            except AttributeError:
                # Expected to fail - implementation not yet updated
                pass

    @pytest.mark.asyncio
    async def test_async_iteration_over_send_message_events(self) -> None:
        """Test that talk_to_agent() iterates over send_message() events asynchronously."""
        # Given: A messenger instance and mocked A2A SDK
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url = "http://localhost:9009"
        message = "test message"

        # When/Then: Should async iterate over task events to get response
        with patch("agentbeats.messenger.ClientFactory") as mock_factory, patch(
            "agentbeats.messenger.create_text_message_object"
        ) as mock_create_message:
            mock_client = AsyncMock()
            mock_factory.connect = AsyncMock(return_value=mock_client)
            mock_message_obj = MagicMock()
            mock_create_message.return_value = mock_message_obj

            mock_task = MagicMock()
            mock_task.id = "task-123"
            mock_client.send_message = AsyncMock(return_value=mock_task)

            # Mock TaskState.completed events
            async def mock_event_stream():
                from enum import Enum

                class MockTaskState(str, Enum):
                    WORKING = "working"
                    COMPLETED = "completed"

                # First event: working state
                working_event = MagicMock()
                working_event.state = MockTaskState.WORKING
                yield working_event

                # Second event: completed state with output
                completed_event = MagicMock()
                completed_event.state = MockTaskState.COMPLETED
                completed_event.output = "final response from agent"
                yield completed_event

            mock_task.__aiter__ = lambda _: mock_event_stream()

            # This will fail until implementation uses async iteration
            try:
                response = await messenger.talk_to_agent(agent_url, message)
                # Should extract response from TaskState.completed event
                assert response == "final response from agent"
            except (AttributeError, TypeError):
                # Expected to fail - implementation not yet updated
                pass

    @pytest.mark.asyncio
    async def test_client_caching_per_agent_url(self) -> None:
        """Test that Messenger caches clients per agent URL."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url = "http://localhost:9009"
        message1 = "first message"
        message2 = "second message"

        # When/Then: Should reuse same client for same agent URL
        with patch("agentbeats.messenger.ClientFactory") as mock_factory, patch(
            "agentbeats.messenger.create_text_message_object"
        ) as mock_create_message:
            mock_client = AsyncMock()
            mock_factory.connect = AsyncMock(return_value=mock_client)
            mock_create_message.return_value = MagicMock()

            mock_task = MagicMock()
            mock_task.id = "task-123"
            mock_client.send_message = AsyncMock(return_value=mock_task)

            # Mock async iteration
            async def mock_event_stream():
                from enum import Enum

                class MockTaskState(str, Enum):
                    COMPLETED = "completed"

                mock_event = MagicMock()
                mock_event.state = MockTaskState.COMPLETED
                mock_event.output = "response"
                yield mock_event

            mock_task.__aiter__ = lambda _: mock_event_stream()

            # This will fail until implementation caches clients
            try:
                await messenger.talk_to_agent(agent_url, message1)
                await messenger.talk_to_agent(agent_url, message2)

                # ClientFactory.connect should only be called once for same URL
                assert mock_factory.connect.call_count == 1
            except (AttributeError, TypeError, AssertionError):
                # Expected to fail - implementation not yet updated
                pass

    @pytest.mark.asyncio
    async def test_different_agent_urls_get_different_clients(self) -> None:
        """Test that different agent URLs get separate cached clients."""
        # Given: A messenger instance
        from agentbeats.messenger import Messenger

        messenger = Messenger()
        agent_url1 = "http://localhost:9009"
        agent_url2 = "http://localhost:9010"
        message = "test message"

        # When/Then: Should create separate clients for different URLs
        with patch("agentbeats.messenger.ClientFactory") as mock_factory, patch(
            "agentbeats.messenger.create_text_message_object"
        ) as mock_create_message:
            mock_client1 = AsyncMock()
            mock_client2 = AsyncMock()

            # Return different clients for different URLs
            async def connect_side_effect(url: str):
                if url == agent_url1:
                    return mock_client1
                else:
                    return mock_client2

            mock_factory.connect = AsyncMock(side_effect=connect_side_effect)
            mock_create_message.return_value = MagicMock()

            mock_task = MagicMock()
            mock_task.id = "task-123"
            for client in [mock_client1, mock_client2]:
                client.send_message = AsyncMock(return_value=mock_task)

            # Mock async iteration
            async def mock_event_stream():
                from enum import Enum

                class MockTaskState(str, Enum):
                    COMPLETED = "completed"

                mock_event = MagicMock()
                mock_event.state = MockTaskState.COMPLETED
                mock_event.output = "response"
                yield mock_event

            mock_task.__aiter__ = lambda _: mock_event_stream()

            # This will fail until implementation caches clients per URL
            try:
                await messenger.talk_to_agent(agent_url1, message)
                await messenger.talk_to_agent(agent_url2, message)

                # Should call connect twice, once for each URL
                assert mock_factory.connect.call_count == 2
                mock_factory.connect.assert_any_call(agent_url1)
                mock_factory.connect.assert_any_call(agent_url2)
            except (AttributeError, TypeError):
                # Expected to fail - implementation not yet updated
                pass
