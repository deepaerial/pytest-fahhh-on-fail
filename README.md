# pytest-fahhh

A pytest plugin that plays [FAHHH sound](https://www.youtube.com/watch?v=nh49oWrwFhM) from meme whenever a test session ends in failure.

## Installation

```bash
uv add --dev pytest-fahhh
# or
pip install pytest-fahhh
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
