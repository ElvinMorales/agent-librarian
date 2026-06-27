# Synthetic Offline Presentation

This public-safe `overview.html` was generated from the intentionally synthetic
catalog in `examples/generated-catalog`.

It is safe to commit only because its source catalog is synthetic and was
reviewed for public use. Presentations generated from real or private catalogs
inherit source sensitivity and must not be committed or publicly shared.

Regenerate from the repository root:

```bash
agent-librarian present examples/generated-catalog --out examples/generated-presentation
```

The default command is deterministic, offline, provider-free, and requires no
API key.
