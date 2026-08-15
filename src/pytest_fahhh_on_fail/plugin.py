from __future__ import annotations

import logging
from importlib import resources
from pathlib import Path

import pytest
from playsound3 import playsound, PlaysoundException

logger = logging.getLogger("pytest_fahhh")

DEFAULT_SOUND = resources.files("pytest_fahhh_on_fail") / "sound.mp3"


def _play_sound(path: Path) -> None:
    if not path.is_file():
        logger.warning("on-fail-sound: file not found, skipping: %s", path)
        return
    playsound(path.as_posix(), block=False)


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("fahhh")
    group.addoption(
        "--on-fail-sound",
        action="store",
        dest="on_fail_sound",
        default=None,
        help="Path to a sound file to play when the test session fails (default: bundled sound.mp3).",
    )
    group.addoption(
        "--no-on-fail-sound",
        action="store_true",
        dest="no_on_fail_sound",
        default=False,
        help="Disable the failure sound.",
    )
    parser.addini(
        "on_fail_sound",
        help="Path to a sound file to play when the test session fails.",
        default=None,
    )
    parser.addini(
        "no_on_fail_sound",
        type="bool",
        help="Set to true to disable the failure sound.",
        default=False,
    )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if exitstatus != pytest.ExitCode.TESTS_FAILED:
        return
    if session.config.option.no_on_fail_sound:
        return
    if session.config.getini("no_on_fail_sound"):
        return

    path = session.config.option.on_fail_sound or session.config.getini("on_fail_sound")
    sound_path = Path(path) if path else Path(DEFAULT_SOUND)

    try:
        _play_sound(sound_path)
    except (PlaysoundException, OSError) as exc:
        logger.warning("on-fail-sound: could not play sound: %s", exc)
