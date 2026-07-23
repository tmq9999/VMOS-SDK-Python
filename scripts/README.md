# Regeneration toolchain

The SDK is generated from the official VMOS OpenAPI documentation, so it can be
refreshed whenever VMOS ships new endpoints:

```bash
# 1. Save a markdown dump of the official docs page
#    https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html
#    (e.g. via https://r.jina.ai/https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html)
curl -sL "https://r.jina.ai/https://cloud.vmoscloud.com/vmoscloud/doc/en/server/OpenAPI.html" -o OpenAPI.md

# 2. Parse it into a machine-readable spec (scripts/data/endpoints.json)
python3 scripts/parse_spec.py OpenAPI.md

# 3. Regenerate the API modules + tests manifest
python3 scripts/gen_sdk.py

# 4. Regenerate docs/en + docs/vi
python3 scripts/gen_docs.py

# 5. Verify everything
python3 -m pytest tests/ -q
```

`scripts/data/endpoints.json` is the committed snapshot of the parsed spec —
`tests/data/endpoints_manifest.json` (used by the test suite) is derived from it.
Hand-written core files (`client.py`, `auth.py`, `exceptions.py`, `models.py`,
`callbacks.py`, `api/_base.py`) are never overwritten by the generator.
