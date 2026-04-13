## ADDED Requirements

### Requirement: Standard Directory Structure
The system SHALL strictly follow a hierarchical directory structure to separate concerns. This structure MUST include:
- `docs/` for primary documentation.
- `docs/assets/` for visual resources and diagrams.
- `scripts/` for build and maintenance automation.
- `sandbox/` for user-generated temporary files (Git-ignored).

#### Scenario: Verify docs movement
- **WHEN** a user or developer adds a new manual or guide
- **THEN** it MUST be placed within the `docs/` directory or its subdirectories.

### Requirement: Agent Hygiene Enforcement
All AI agents interacting with the project SHALL NOT generate ephemeral tool-related files (e.g., JSON outputs, status logs) in the project root. Instead, they SHALL redirect all such output to `.agent/scratch/`.

#### Scenario: Tool output redirection
- **WHEN** an agent runs a command with JSON output redirection
- **THEN** it MUST use a path prefixed with `.agent/scratch/`.

### Requirement: Resource Path Resolution
The application SHALL resolve paths to documentation and visual assets relative to the new `docs/` and `docs/assets/` directories.

#### Scenario: Loading the application logo
- **WHEN** the GUI initializes
- **THEN** it MUST successfully load the logo from `docs/assets/logo.png`.
