# Static Synthetic Narrated Presentation

This narrated demo is static and synthetic. It demonstrates the shape of
narrated outputs without making a provider call.

The output uses the intentionally synthetic `examples/generated-catalog`
fixture and a local stub narrative. It did not use `ANTHROPIC_API_KEY`, contact
Anthropic or another provider, or invoke a model. The provenance model value
`synthetic-static-stub` and zero token counts make that boundary explicit.

The folder contains:

- `overview.html`: deterministic catalog facts with the stubbed narrative
  placed above them.
- `narrative.md`: the clearly labeled static demonstration narrative.
- `narrative-provenance.json`: the normal provenance shape populated with
  fixed synthetic demonstration values.

These files are safe to commit only because their source is synthetic. Real
narrated output can repeat sensitive artifact names, paths, warnings, and
overlap information. Do not commit or publicly share presentations generated
from private catalogs.

A real narrated run uses the optional provider path:

```bash
python -m pip install -e ".[narrate]"
agent-librarian present examples/generated-catalog --out OUT_DIR --narrate
```

That command requires `ANTHROPIC_API_KEY` and contacts Anthropic. It was not
used to create this committed demo. Model narrative remains a secondary review
aid; deterministic catalog facts are the source of truth.
