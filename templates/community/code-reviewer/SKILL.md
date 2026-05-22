---
name: code-reviewer
description: >
  This skill should be used when the user asks to "review code",
  "check code quality", "audit code", "find code issues",
  or "perform a code review".
version: 0.1.0
allowed-tools: [Read, Bash, Grep]
---

# Code Reviewer

Reviews source code for quality, security, and best practice issues.

## Usage

Point the skill to files or directories for review. It analyzes code and produces a review report.

### Review Areas

- **Correctness**: logic errors, edge cases, race conditions
- **Security**: injection, auth, data exposure
- **Style**: naming, formatting, complexity
- **Performance**: bottlenecks, resource usage
- **Maintainability**: coupling, cohesion, documentation
