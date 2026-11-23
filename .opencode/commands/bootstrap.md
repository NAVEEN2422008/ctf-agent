---
description: Bootstrap, audit, and configure local security agents, MCP servers, and verification loops.
agent: autonomous-hacker
---

# Bootstrap Security Environment

Review the current workspace and global OpenCode configuration at `~/.config/opencode/opencode.json`.

## Phase 1: Configuration Audit
1. Verify opencode.json is valid JSON
2. Check all agent files exist and have valid frontmatter
3. Verify all command files exist
4. Check MCP server configurations

## Phase 2: Tool Verification
1. Check all Go tools are installed and functional
2. Verify Python security packages
3. Check Ruby gems
4. Verify system tools

## Phase 3: Permission Audit
1. Verify bash permissions cover all required tools
2. Check external directory permissions
3. Verify agent permissions are correct

## Phase 4: Self-Configuration
1. If anything is missing, autonomously write or patch the configuration files
2. Install any missing dependencies
3. Update PATH if needed

## Phase 5: Verification Loop
1. Run syntax checks on all configurations
2. Execute tool version checks
3. Verify MCP server connectivity
4. Output verified execution readiness report

## Output Format
```
[BOOTSTRAP] Environment Audit
[CONFIG] opencode.json: VALID/INVALID
[AGENTS] X/X loaded
[COMMANDS] X/X loaded
[SKILLS] X/X loaded
[TOOLS] X/X verified
[MCP] X/X connected
[STATUS] READY/NEEDS_ATTENTION
```
