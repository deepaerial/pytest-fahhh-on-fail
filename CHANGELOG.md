# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- CI pipeline split into separate jobs: `lint` (ruff) → `test` → `tag` →
  `build` → `publish`. Lint and tests also run on pull requests.
- The build job uploads `dist/` as an artifact; the publish job runs on a
  fresh runner, downloads it, and publishes to PyPI.
- `ruff` added as a dev dependency.

## [1.0.0] - 2026-08-15

### Added

- Pytest plugin (published as `pytest-fahhh-on-fail`) that plays the bundled
  `sound.mp3` when a test session fails.
- Options:
  - `--on-fail-sound PATH` to play a custom sound file.
  - `--no-on-fail-sound` to disable the sound.
  - `on_fail_sound` and `no_on_fail_sound` ini options.
- Automatic registration via the `pytest11` entry point.
- Audio errors never break the test run.
- Python 3.10–3.14 support.
- `tox` + `tox-uv` matrix testing (`uv run tox`).
- `run.sh` script that installs `uv`, syncs dependencies, and runs the
  intentionally-failing `test_fail.py` demo.
- CI workflow that runs the test matrix and publishes to PyPI.
