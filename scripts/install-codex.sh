#!/bin/bash
# install-codex.sh
# Install NFlow for Codex

set -e

echo "Installing NFlow for Codex..."

# Create Codex project
WORKSPACE_DIR="$HOME/.codex/projects/nflow"
mkdir -p "$WORKSPACE_DIR"
cp -r . "$WORKSPACE_DIR"

# Create .codex.json config
cat > "$WORKSPACE_DIR/.codex.json" << EOF
{
  "name": "NFlow",
  "version": "1.0.0",
  "description": "Custom Development Workflow - BMad + Superpowers",
  "commands": {
    "init": "commands/nflow-init.md",
    "requirements": "commands/nflow-requirements.md",
    "design": "commands/nflow-design.md",
    "prototype": "commands/nflow-prototype.md",
    "plan": "commands/nflow-plan.md",
    "dev": "commands/nflow-dev.md",
    "story": "commands/nflow-story.md",
    "review": "commands/nflow-review.md"
  }
}
EOF

# Create instructions file
cat > "$WORKSPACE_DIR/INSTRUCTIONS.md" << 'EOF'
# NFlow - Custom Development Workflow

You have access to NFlow, a structured development workflow.

## Quick Start
1. `/nflow-init` - Initialize project
2. `/nflow-requirements` - Define requirements
3. `/nflow-design` - Design system & wireframes
4. `/nflow-prototype` - Generate UI prototypes
5. `/nflow-plan` - Create backlog & sprint
6. `/nflow-dev` - Start development loop
7. `/nflow-review` - Final code review

## Workflow Overview
See SKILL.md for full documentation.

## Commands
- /nflow-init - Initialize project
- /nflow-requirements - Requirements definition
- /nflow-design - Design system & wireframes
- /nflow-prototype - UI prototypes
- /nflow-plan - Backlog & Sprint planning
- /nflow-dev - Development loop
- /nflow-story - Single story implementation
- /nflow-review - Final review
EOF

echo "NFlow installed to: $WORKSPACE_DIR"
echo ""
echo "Usage in Codex:"
echo "  @nflow/init         - Initialize project"
echo "  @nflow/requirements - Define requirements"
echo "  ..."
