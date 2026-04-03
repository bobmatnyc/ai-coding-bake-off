.PHONY: help test-level eval-all eval-quality eval-coverage report setup-agent clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Competition ---

test-level: ## Run provided tests for a level: make test-level LEVEL=1
	pytest challenges/level-$(LEVEL)-*/test_suite/ -v

test-solution: ## Run agent's tests: make test-solution AGENT=claude-mpm LEVEL=1
	pytest harnesses/$(AGENT)/output/level-$(LEVEL)/tests/ -v

test-all-levels: ## Run all provided tests for an agent: make test-all-levels AGENT=claude-mpm
	@for level in 1 2 3 4 5; do \
		echo "\n=== Level $$level ===" ; \
		pytest challenges/level-$$level-*/test_suite/ -v --tb=short 2>/dev/null || true ; \
	done

# --- Evaluation ---

eval-tests: ## Run automated test evaluation across all agents
	python3 evaluation/automated/run_tests.py

eval-quality: ## Run code quality checks across all agents
	python3 evaluation/automated/code_quality.py

eval-coverage: ## Run coverage analysis across all agents
	python3 evaluation/automated/coverage_check.py

eval-all: eval-tests eval-quality eval-coverage ## Run all automated evaluations

report: ## Generate comparison report
	python3 scripts/generate_report.py

metrics: ## Collect all metrics
	python3 scripts/collect_metrics.py

# --- Setup ---

setup-agent: ## Set up workspace for an agent: make setup-agent AGENT=claude-code
	bash scripts/setup_agent_workspace.sh $(AGENT)

setup-venv: ## Create virtual environment with dev tools
	python3 -m venv .venv
	.venv/bin/pip install pytest pytest-cov ruff mypy pylint

clean: ## Remove __pycache__ and .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
