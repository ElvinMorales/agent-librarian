# Package Conformance Checklist

Use this checklist when adding or reviewing package adapters.

## Source of Truth

- Package files state that canonical artifacts under `agent/` and
  deterministic CLI/generated outputs are the source of truth.
- Package files are adapters for platform workspaces and do not define a
  separate agent identity.
- Model-authored summaries are secondary review aids.

## Command-Capable Packages

- Local execution is described only for hosts that provide local tools.
- Runtime-wrapper `propose` is preferred before `run`.
- Wrapper `run` requires exact approval for the visible command and scope.
- Allowed command examples are limited to documented `catalog`, `validate`,
  and `report` forms.
- Wrong or vague approval blocks execution.

## Advisory Packages

- Advisory packages say they do not run the local CLI by default.
- Advisory packages ask the user to run deterministic local commands when
  evidence is missing.
- Advisory packages do not claim filesystem inspection, validation,
  cataloging, or command execution unless a future reviewed Action/API wrapper
  exists.

## Safety Boundaries

- Public demos use only synthetic repository fixtures.
- Package files warn against private scans, private generated outputs, work
  folders, secrets, credentials, private journals, private prompts, private
  traces, memory snapshots, state snapshots, employer/client data, customer
  data, regulated data, and internal URLs.
- Generated outputs inherit source sensitivity.
- Publication requires separate human review.
- Package files do not certify safety, privacy, correctness, completeness,
  approval, compliance, or publication readiness.

## Local Static Checks

Run:

```bash
python scripts/check_packages.py
pytest
git diff --exit-code -- examples/generated-catalog
```

The checker is static. It does not call external providers, OpenAI APIs,
Claude, Codex, network services, GitHub, or MCP servers.
