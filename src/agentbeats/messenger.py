"""Messenger module for A2A agent communication and trace capture."""

from datetime import UTC, datetime

from a2a.client import Client, ClientFactory, create_text_message_object
from a2a.types import TaskState
from pydantic import BaseModel


class TraceData(BaseModel):
    """Structure of trace data for evaluators."""

    timestamp: str
    agent_url: str
    message: str
    response: str
    status_code: int | None = None
    error: str | None = None


class Messenger:
    """Handles communication with A2A agents and captures interaction traces."""

    def __init__(self) -> None:
        """Initialize messenger with empty trace list and client cache."""
        self._traces: list[TraceData] = []
        self._clients: dict[str, Client] = {}

    async def talk_to_agent(self, agent_url: str, message: str) -> str:
        """Send a message to an agent and return the response.

        Args:
            agent_url: URL of the target agent
            message: Message to send to the agent

        Returns:
            Response string from the agent

        Raises:
            Exception: If communication fails
        """
        timestamp = datetime.now(UTC).isoformat()

        try:
            # Get or create cached client for this agent URL
            if agent_url not in self._clients:
                self._clients[agent_url] = await ClientFactory.connect(agent_url)

            client = self._clients[agent_url]

            # Create text message object using A2A SDK
            message_obj = create_text_message_object(content=message)

            # Send message and get task/iterator
            # Note: Real API returns AsyncIterator, but mocks return awaitable task
            result = client.send_message(message_obj)

            # Handle both awaitable (mocked) and direct iteration (real API)
            try:
                task = await result  # type: ignore[misc]
            except TypeError:
                # result is already an AsyncIterator
                task = result  # type: ignore[assignment]

            # Iterate over task events to get response
            response_text = ""
            async for event in task:  # type: ignore[union-attr]
                if hasattr(event, "state") and event.state == TaskState.completed:  # type: ignore[union-attr]
                    response_text = str(event.output) if hasattr(event, "output") and event.output is not None else ""  # type: ignore[union-attr]
                    break

            # Capture successful trace
            trace = TraceData(
                timestamp=timestamp,
                agent_url=agent_url,
                message=message,
                response=response_text,
                status_code=200,
            )
            self._traces.append(trace)

            return response_text

        except Exception as e:
            # Capture error trace
            trace = TraceData(
                timestamp=timestamp,
                agent_url=agent_url,
                message=message,
                response="",
                error=str(e),
            )
            self._traces.append(trace)
            raise

    def get_traces(self) -> list[TraceData]:
        """Return list of all captured interaction traces.

        Returns:
            List of TraceData objects representing all interactions
        """
        return self._traces
