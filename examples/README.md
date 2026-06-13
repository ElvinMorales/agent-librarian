# Synthetic Example Collection

The files under `sample-collection` are fabricated, public-safe design-time
artifacts for exercising the CLI. They are not production configurations,
runtime records, private prompts, or complete protocol implementations.

The collection contains:

- two intentionally overlapping summarization skills
- one distinct research-assistant definition
- one intentionally incomplete weekly-review prompt
- one local tool manifest
- one synthetic MCP-style manifest

Generate the committed example outputs with:

```bash
agent-librarian catalog examples/sample-collection --out examples/generated-catalog
```

The files under `generated-catalog` are generated from this synthetic
collection and are committed for documentation and review.
