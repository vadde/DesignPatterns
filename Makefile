# ==============================================================================
# Design Patterns Autonomous Command Deck Makefile
# Unified automation for building, testing, linting, and serving
# ==============================================================================

.DEFAULT_GOAL := help
SHELL := /usr/bin/env bash

# Terminal Colors
CYAN   := \033[0;36m
GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
NC     := \033[0m

.PHONY: help docs-build docs-serve docs-test test-boxes format-boxes test-links test-details test-badges test lint ci clean

help: ## Show this interactive help menu
	@printf "\n$(CYAN)🏛️ Design Patterns Architecture Bible — Autonomous Command Deck$(NC)\n\n"
	@printf "Usage:\n  make $(CYAN)<target>$(NC)\n\nTargets:\n"
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(CYAN)%-18s$(NC) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@printf "\n"

docs-build: ## Compile 28 chapters catalog and package static site into _site/
	@printf "$(CYAN)📚 Compiling Design Patterns Living Documentation into _site/...$(NC)\n"
	@bash scripts/build-docs.sh

docs-serve: docs-build ## Serve living documentation portal on http://localhost:4000
	@printf "$(CYAN)🚀 Serving Design Patterns Living Documentation on http://localhost:4000...$(NC)\n"
	@if command -v python3 >/dev/null; then \
		python3 -m http.server 4000 --directory _site; \
	elif command -v npx >/dev/null; then \
		npx -y serve _site -p 4000; \
	else \
		echo "$(RED)❌ Neither python3 nor npx found to serve static documentation.$(NC)"; \
		exit 1; \
	fi

docs-test: ## Run 15-gate automated headless verification suite
	@bash scripts/test-docs.sh

test-boxes: ## Audit ASCII and Unicode box-drawing tables and cards alignment
	@printf "$(CYAN)📐 Auditing ASCII/Unicode box-drawing alignment...$(NC)\n"
	@python3 scripts/audit_ascii_boxes.py --check

format-boxes: ## Realign and format all ASCII/Unicode boxes across the repository in place
	@printf "$(CYAN)✨ Formatting and realigning all ASCII/Unicode boxes...$(NC)\n"
	@python3 scripts/audit_ascii_boxes.py --fix

test-links: ## Audit universal hyperlink integrity, SPA containment, and zero local path leaks
	@printf "$(CYAN)🔗 Auditing hyperlink integrity & zero local path leaks...$(NC)\n"
	@python3 scripts/audit_links_and_anchors.py

test-details: ## Audit collapsible details and raw HTML block invariants
	@printf "$(CYAN)📂 Auditing collapsible details and raw HTML block invariants...$(NC)\n"
	@python3 scripts/audit_collapsible_elements.py

test-badges: ## Audit monospace semantic badges and implementation labels
	@printf "$(CYAN)🏷️ Auditing monospace semantic badges...$(NC)\n"
	@python3 scripts/audit_monospace_badging.py

test: test-boxes ## Run Python AST syntax and compilation checks across all patterns
	@printf "$(CYAN)🧪 Compiling all Python design pattern implementations...$(NC)\n"
	@python3 -m compileall -q .
	@printf "$(GREEN)✅ All Python files compiled successfully without SyntaxErrors.$(NC)\n"

lint: test-boxes ## Lint codebase with ruff and validate box alignment
	@printf "$(CYAN)🔍 Running ruff linter...$(NC)\n"
	@if command -v ruff >/dev/null; then \
		ruff check . --select=E9,F63,F7,F82; \
	else \
		printf "$(YELLOW)⚠️ ruff not installed in local environment, skipping.$(NC)\n"; \
	fi

ci: test lint docs-test ## Run full continuous integration audit suite locally
	@printf "\n$(GREEN)🎉 Full CI audit suite passed locally with 100%% compliance!$(NC)\n\n"

clean: ## Clean build output directory and pycache
	@printf "$(CYAN)🧹 Cleaning build artifacts...$(NC)\n"
	@rm -rf _site/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@printf "$(GREEN)✅ Clean complete.$(NC)\n"
