# Release and CI

MiniLangCompiler uses a single verification script to keep local and CI
behavior aligned.

## Verification script

`./scripts/verify.sh` is the canonical entry point. It performs:

- Environment setup
- Dependency installation
- Unit tests
- Smoke test

Any failure causes a non-zero exit code.

## GitHub Actions

The CI workflow in `.github/workflows/ci.yml` runs on push and pull request
events. It executes the same verification script to ensure CI matches local
behavior.

## Recommended release steps

1. Run `./scripts/verify.sh` locally.
2. Ensure documentation is updated.
3. Tag a release in Git with a semantic version.

## Versioning

The Python package version is defined in `src/minilang_compiler/__init__.py`.
Update it when releasing.

## CI troubleshooting

If CI fails:

- Review the workflow logs for the failing step.
- Re-run `./scripts/verify.sh` locally to reproduce.
- Ensure the required Python version (3.11) is available.
