# Shared Package Foundation

This directory defines the shared package manifest and conformance expectations
for future `agent-librarian` platform adapters.

The shared files do not create live Claude, Codex, GPT, or ChatGPT package
implementations. They define the contract those adapters must follow.

## Files

- `package-manifest.schema.json`: JSON Schema for package manifests.
- `package-manifest.example.yaml`: public-safe example mapping canonical
  artifacts to planned platform files.
- `conformance/`: shared behavior expectations for safety, approval, refusal,
  evidence, and review-summary behavior.

## Source of Truth

Canonical behavior remains under `agent/`. If a future package adapter and a
canonical artifact disagree, the canonical artifact wins.

