# pytest-fahhh-on-fail

A pytest plugin that plays [FAHHH sound](https://www.youtube.com/watch?v=nh49oWrwFhM) from meme whenever a test session ends in failure.

## Installation

```bash
uv add --dev pytest-fahhh-on-fail
# or
pip install pytest-fahhh-on-fail
```

The plugin registers itself via the `pytest11` entry point, so it is
auto-loaded on the next pytest run — no `conftest.py` changes required.

## Usage

Just run pytest. If the session fails, the bundled `sound.mp3` plays in the
background once the run finishes.

```bash
pytest
```

To try the sound immediately after cloning the repo:

```bash
uv sync
uv run pytest test_fail.py
```

The repo includes an intentionally-failing `test_fail.py`, so the run fails on
purpose and the plugin plays the bundled `sound.mp3` as soon as it finishes.

### Options

| Option | Description |
| --- | --- |
| `--on-fail-sound PATH` | Play a custom sound file on failure. |
| `--no-on-fail-sound` | Disable the failure sound. |
| `on_fail_sound = PATH` (ini) | Same, set in `pyproject.toml` or `pytest.ini`. |
| `no_on_fail_sound = true` (ini) | Disable the failure sound from config. |

```bash
pytest --on-fail-sound /path/to/beep.mp3
pytest --no-on-fail-sound
```

### Configuration file

```toml
# pyproject.toml
[tool.pytest.ini_options]
on_fail_sound = "assets/beep.mp3"
```

```ini
# pytest.ini
[pytest]
on_fail_sound = assets/beep.mp3
```

You can also disable the sound from a config file:

```toml
[tool.pytest.ini_options]
no_on_fail_sound = true
```

## How it works

The plugin implements `pytest_sessionfinish` and plays the sound only when
`exitstatus == pytest.ExitCode.TESTS_FAILED` (i.e. at least one test failed).
Sound playback uses [`playsound3`](https://pypi.org/project/playsound3/) in
non-blocking mode, so it starts playing in the background right before the
session exits.

Audio problems never break the test run: if the configured file is missing or
no audio backend is available, a warning is logged and pytest continues
normally.

## Development

```bash
uv sync
uv run pytest
```

The test suite uses pytest's `pytester` fixture to run fake sessions and verify
that the sound is triggered on failure, but not on success, missing files, or
disabling switches.

### Supported Python versions

The plugin supports Python 3.10+. Run the full matrix locally with tox (powered
by `tox-uv`, so uv handles the virtualenvs and the lockfile):

```bash
uv run tox
```

CI runs the same matrix (Python 3.10–3.14) on every push to `main`.

## Releasing

The CI pipeline is a chain of separate jobs, each running only after the
previous one succeeds:

1. **lint** — `ruff check` + `ruff format --check`
2. **test** — the full Python 3.10–3.14 matrix
3. **tag** — reads the version from `pyproject.toml`; if no `v<version>` tag
   exists yet, creates and pushes it
4. **build** — builds the wheel and sdist, uploads `dist/` as a run artifact
5. **publish** — on a fresh runner, downloads that artifact and publishes it
   to PyPI

`lint` and `test` also run on every pull request. The `tag`, `build`, and
`publish` jobs run only on push to `main`, and publishing happens only when the
`tag` job actually created a new tag (i.e. the version was bumped). Building
and publishing are separate jobs, so the publish step never reuses the build
machine — it uploads exactly what was built.

So a release is just bumping the version:

```bash
# 1. bump `version` in pyproject.toml
git add pyproject.toml uv.lock
git commit -m "release v1.0.1"
git push origin main
```

Requires a trusted publisher configured on the PyPI project
(`pytest-fahhh-on-fail`). If a publish run fails after the tag was already
created, delete the tag (`git push origin :refs/tags/v1.0.0`) and push again,
or bump the version.
