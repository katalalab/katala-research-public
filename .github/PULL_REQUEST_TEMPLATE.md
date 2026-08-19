## Summary

-

## Verification

- [ ] `uv sync --locked --extra dev`
- [ ] `scripts/verify.sh`
- [ ] GitHub Actions: CI
- [ ] Workflow/runtime changes keep `.python-version`, `pyproject.toml`, `uv.lock`, and `tests/test_ci_workflows.py` aligned

## Boundary

- [ ] No live API run, external research run, scraping flow, or session-materializing smoke was run unless explicitly required

## Risk / Rollback

- Risk:
- Rollback:

## Notes

- Unverified scope:
