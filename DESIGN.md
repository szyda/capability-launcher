# Design notes

This is a small prototype for a capability platform. The idea is simple: keep a single API, let each capability live in its own folder, and avoid forcing everything to share one Python environment.

## The main idea

I treat each capability as a small, self-contained Python module with a clear contract:

- it has metadata in a manifest
- it exposes a `run(inputs)` function
- it returns JSON-compatible output
- it runs in its own virtual environment

That keeps the platform easy to understand and easy to extend without turning into a large framework.

## Working assumptions

These are the practical assumptions I am making for this prototype:

- A developer adds a capability by creating a new directory under the capabilities folder.
- New capabilities become available after the API is restarted.
- Execution is synchronous and short-running.
- Each capability gets its own virtual environment.
- Inputs and outputs are JSON-compatible.
- Capabilities are trusted internal Python code.
- Authentication is not required for this prototype.
- There is no database; the filesystem is the source of truth.
- The frontend is a generic, schema-driven UI.
- Custom capability-specific UI is a future extension.

## Why this shape

This keeps the design intentionally small.

- The API discovers capabilities from metadata instead of hard-coding them.
- Each capability is isolated from the others at the dependency level.
- The execution boundary is simple: validate input, run, return result.
- The frontend can be generic because the API already exposes capability metadata.

## Trade-offs

I am choosing simplicity over polish.

- No plugin framework, because it would add more structure than this prototype needs.
- No queue system, retries, or job database, because the execution model is simple and short-lived.
- Lightweight validation instead of a full schema engine.
- Subprocess-based isolation rather than a full sandbox, which is enough for local trusted code but not for untrusted workloads.

## What I am intentionally not doing

- authentication
- persistent run history
- queueing or background jobs
- advanced monitoring
- production-grade sandboxing
- custom UI per capability in v1

## What comes next

If this project grows, the obvious next step would be to improve runtime visibility and make capability setup smoother:

- better manifest validation
- clearer runtime logging
- health checks for capability environments
- a more polished generic frontend

For now, the goal is not to build a perfect platform. It is to build a working prototype that shows the core idea clearly.
