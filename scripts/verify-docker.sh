#!/bin/bash
# Script to verify Docker build and run for AgentBeats GreenAgent
# Usage: ./scripts/verify-docker.sh

set -e

echo "=== Docker Build and Run Verification ==="
echo ""

# Build the image
echo "Step 1/3: Building Docker image..."
docker build -t green-agent .
echo "✓ Build successful"
echo ""

# Run the container in background
echo "Step 2/3: Starting container..."
CONTAINER_ID=$(docker run -d -p 9009:9009 green-agent)
echo "✓ Container started: $CONTAINER_ID"
echo ""

# Wait for server to be ready
echo "Waiting for server to start..."
sleep 5

# Test the agent card endpoint
echo "Step 3/3: Testing agent card endpoint..."
RESPONSE=$(curl -s http://localhost:9009/.well-known/agent-card.json)

if echo "$RESPONSE" | grep -q "AgentBeats GreenAgent"; then
    echo "✓ Agent card endpoint responding correctly"
    echo ""
    echo "Agent Card Response:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
else
    echo "✗ Agent card endpoint not responding as expected"
    echo "Response: $RESPONSE"
    docker logs "$CONTAINER_ID"
    docker stop "$CONTAINER_ID"
    docker rm "$CONTAINER_ID"
    exit 1
fi

# Cleanup
echo ""
echo "Cleaning up..."
docker stop "$CONTAINER_ID"
docker rm "$CONTAINER_ID"

echo ""
echo "=== All verification tests passed! ==="
