# This Makefile automates the build, test, and clean processes for the project.
# It provides a convenient way to run common tasks using the 'make' command.
# It is designed to work with the 'uv' tool for managing Python environments and dependencies.
# Run `make help` to see all available recipes.

.SILENT:
.ONESHELL:
.PHONY: setup_dev setup_dev_full setup_claude_code setup_markdownlint run_markdownlint run_cli \
        ruff test_all coverage_all type_check validate quick_validate \
        ralph_init ralph ralph_status ralph_clean reorganize_prd \
        run_agent build_agent test_agent push_agent publish_agent \
        help
.DEFAULT_GOAL := help


# MARK: setup


setup_dev:  ## Install uv and deps, Download and start Ollama 
	echo "Setting up dev environment ..."
	pip install uv -q
	uv sync --all-groups
	echo "npm version: $$(npm --version)"
	$(MAKE) -s setup_claude_code
	$(MAKE) -s setup_markdownlint
	
setup_dev_full: ## Complete dev setup
	$(MAKE) -s setup_dev

setup_claude_code:  ## Setup claude code CLI, node.js and npm have to be present
	echo "Setting up Claude Code CLI ..."
	npm install -gs @anthropic-ai/claude-code
	echo "Claude Code CLI version: $$(claude --version)"

setup_markdownlint:  ## Setup markdownlint CLI, node.js and npm have to be present
	echo "Setting up markdownlint CLI ..."
	npm install -gs markdownlint-cli
	echo "markdownlint version: $$(markdownlint --version)"


# MARK: run markdownlint


run_markdownlint:  ## Lint markdown files. Usage from root dir: make run_markdownlint INPUT_FILES="docs/**/*.md"
	if [ -z "$(INPUT_FILES)" ]; then
		echo "Error: No input files specified. Use INPUT_FILES=\"docs/**/*.md\""
		exit 1
	fi
	markdownlint $(INPUT_FILES) --fix


# MARK: run app


run_cli:  ## Run app on CLI only. Usage: make run_cli ARGS="--help" or make run_cli ARGS="--download-peerread-samples-only"
	echo PYTHONPATH=$(SRC_PATH) uv run python $(CLI_PATH) $(ARGS)


# MARK: Sanity


ruff:  ## Lint: Format and check with ruff
	uv run ruff format
	uv run ruff check --fix

test_all:  ## Run all tests
	uv run pytest

coverage_all:  ## Get test coverage
	uv run coverage run -m pytest || true
	uv run coverage report -m

type_check:  ## Check for static typing errors
	uv run pyright src

validate:  ## Complete pre-commit validation sequence
	echo "Running complete validation sequence ..."
	$(MAKE) -s ruff
	-$(MAKE) -s type_check
	-$(MAKE) -s test_all
	echo "Validation sequence completed (check output for any failures)"

quick_validate:  ## Fast development cycle validation
	echo "Running quick validation ..."
	$(MAKE) -s ruff
	-$(MAKE) -s type_check
	echo "Quick validation completed (check output for any failures)"

# MARK: ralph


ralph_init:  ## Initialize Ralph loop environment
	echo "Initializing Ralph loop environment ..."
	bash .claude/scripts/ralph/init.sh

ralph:  ## Run Ralph autonomous development loop (use ITERATIONS=N to set max iterations)
	echo "Starting Ralph loop ..."
	ITERATIONS=$${ITERATIONS:-25}
	bash .claude/scripts/ralph/ralph.sh $$ITERATIONS

ralph_status:  ## Show Ralph loop progress and status
	echo "Ralph Loop Status"
	echo "================="
	if [ -f docs/ralph/prd.json ]; then \
		total=$$(jq '.stories | length' docs/ralph/prd.json); \
		passing=$$(jq '[.stories[] | select(.passes == true)] | length' docs/ralph/prd.json); \
		echo "Stories: $$passing/$$total completed"; \
		echo ""; \
		echo "Incomplete stories:"; \
		jq -r '.stories[] | select(.passes == false) | "  - [\(.id)] \(.title)"' docs/ralph/prd.json; \
	else \
		echo "prd.json not found. Run 'make ralph_init' first."; \
	fi

ralph_clean:  ## Reset Ralph state (WARNING: removes prd.json and progress.txt)
	echo "WARNING: This will reset Ralph loop state!"
	echo "Press Ctrl+C to cancel, Enter to continue..."
	read
	rm -f docs/ralph/prd.json docs/ralph/progress.txt
	echo "Ralph state cleaned. Run 'make ralph_init' to reinitialize."

reorganize_prd:  ## Archive current PRD and activate new one. Usage: make reorganize_prd NEW_PRD=path/to/new.md [VERSION=2]
	if [ -z "$(NEW_PRD)" ]; then
		echo "Error: NEW_PRD parameter required"
		echo "Usage: make reorganize_prd NEW_PRD=docs/PRD-New.md [VERSION=2]"
		exit 1
	fi
	VERSION_ARG=""
	if [ -n "$(VERSION)" ]; then
		VERSION_ARG="-v $(VERSION)"
	fi
	bash scripts/reorganize_prd.sh $$VERSION_ARG $(NEW_PRD)


# MARK: agentbeats

# Agent configuration
# Override: make build_agent AGENT_TYPE=purple GITHUB_USER=yourname
AGENT_TYPE ?= green
GITHUB_USER ?= qte77

# Green agent config
green_IMAGE_NAME = agentbeats-greenagent
green_VERSION = 0.0.0
green_DOCKERFILE = Dockerfile
green_CONTEXT = .
green_TITLE = GraphJudge-RDI-AgentBeats-GreenAgent
green_DESCRIPTION = Graph-based coordination evaluator for AgentBeats competition
green_PURPOSE = PulseMetricComplianceCoordinationAuscultatorEngine

# Purple agent config
purple_IMAGE_NAME = agentbeats-purpleagent
purple_VERSION = 0.1.0
purple_DOCKERFILE = examples/purple-agent/Dockerfile
purple_CONTEXT = examples/purple-agent
purple_TITLE = PurpleAgent-RDI-AgentBeats
purple_DESCRIPTION = Simple A2A-compatible demo agent for AgentBeats evaluation
purple_PURPOSE = SimpleA2ADemoAgent

# Computed variables based on AGENT_TYPE
IMAGE_NAME = $($(AGENT_TYPE)_IMAGE_NAME)
VERSION = $($(AGENT_TYPE)_VERSION)
GHCR_IMAGE = ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)

run_agent:  ## Start AgentBeats server. Usage: make run_agent or make run_agent ARGS="--port 8080"
	PYTHONPATH=src uv run python -m agentbeats.server $(ARGS)

build_agent:  ## Build agent Docker image. Usage: make build_agent [AGENT_TYPE=green|purple] [GITHUB_USER=yourname]
	docker build --platform linux/amd64 \
		--label "org.opencontainers.image.title=$($(AGENT_TYPE)_TITLE)" \
		--label "org.opencontainers.image.description=$($(AGENT_TYPE)_DESCRIPTION)" \
		--label "org.opencontainers.image.version=$(VERSION)" \
		--label "org.opencontainers.image.url=https://github.com/$(GITHUB_USER)/RDI-AgentX-AgentBeats-Competition" \
		--label "org.opencontainers.image.source=https://github.com/$(GITHUB_USER)/RDI-AgentX-AgentBeats-Competition" \
		--label "rdi.agentbeats.agent-type=$(AGENT_TYPE)" \
		--label "rdi.agentbeats.competition=agentx-2025" \
		--label "purpose=$($(AGENT_TYPE)_PURPOSE)" \
		-t $(GHCR_IMAGE):latest \
		-t $(GHCR_IMAGE):$(VERSION) \
		-f $($(AGENT_TYPE)_DOCKERFILE) \
		$($(AGENT_TYPE)_CONTEXT)

push_agent:  ## Push agent image to GHCR. Usage: make push_agent [AGENT_TYPE=green|purple] [GITHUB_USER=yourname]
	docker push $(GHCR_IMAGE):latest
	docker push $(GHCR_IMAGE):$(VERSION)

publish_agent:  ## Build and push agent to GHCR. Usage: make publish_agent [AGENT_TYPE=green|purple] [GITHUB_USER=yourname]
	$(MAKE) -s build_agent AGENT_TYPE=$(AGENT_TYPE) GITHUB_USER=$(GITHUB_USER)
	$(MAKE) -s push_agent AGENT_TYPE=$(AGENT_TYPE) GITHUB_USER=$(GITHUB_USER)
	echo "Published $($(AGENT_TYPE)_TITLE): $(GHCR_IMAGE):latest and $(GHCR_IMAGE):$(VERSION)"

test_agent:  ## Run agentbeats tests
	uv run pytest tests/


# MARK: help


help:  ## Displays this message with available recipes
	# TODO add stackoverflow source
	echo "Usage: make [recipe]"
	echo "Recipes:"
	awk '/^[a-zA-Z0-9_-]+:.*?##/ {
		helpMessage = match($$0, /## (.*)/)
		if (helpMessage) {
			recipe = $$1
			sub(/:/, "", recipe)
			printf "  \033[36m%-20s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH)
		}
	}' $(MAKEFILE_LIST)