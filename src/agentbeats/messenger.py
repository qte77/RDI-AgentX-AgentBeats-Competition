"""Messenger module for A2A agent communication and trace capture."""

from datetime import UTC, datetime

import httpx
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
        """Initialize messenger with empty trace list."""
        self._traces: list[TraceData] = []

    async def talk_to_agent(self, agent_url: str, message: str) -> str:
        """Send a message to an agent and return the response.

        Args:
            agent_url: URL of the target agent
            message: Message to send to the agent

        Returns:
            Response string from the agent

        Raises:
            httpx.HTTPError: If HTTP communication fails
        """
        timestamp = datetime.now(UTC).isoformat()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{agent_url}/message",
                    json={"message": message},
                    timeout=30.0,
                )
                response.raise_for_status()
                response_text = response.text

                # Capture successful trace
                trace = TraceData(
                    timestamp=timestamp,
                    agent_url=agent_url,
                    message=message,
                    response=response_text,
                    status_code=response.status_code,
                )
                self._traces.append(trace)

                return response_text

        except httpx.HTTPError as e:
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
