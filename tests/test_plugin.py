from pathlib import Path

import pytest
from playsound3 import PlaysoundException

from pytest_fahhh_on_fail import plugin


def _failing_test(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("def test_fail():\n    assert False")


@pytest.fixture
def play_spy(pytester, monkeypatch):
    calls: list[Path] = []
    monkeypatch.setattr(plugin, "_play_sound", lambda path: calls.append(Path(path)))
    return calls


def test_bundled_sound_exists():
    assert plugin.DEFAULT_SOUND.is_file()


def test_plays_sound_on_failure(pytester, play_spy):
    _failing_test(pytester)
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    assert len(play_spy) == 1


def test_no_sound_on_success(pytester, play_spy):
    pytester.makepyfile("def test_ok():\n    assert True")
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert play_spy == []


def test_custom_sound_path(pytester, play_spy):
    _failing_test(pytester)
    result = pytester.runpytest("--on-fail-sound", "custom.mp3")
    result.assert_outcomes(failed=1)
    assert play_spy == [Path("custom.mp3")]


def test_no_on_fail_sound_flag(pytester, play_spy):
    _failing_test(pytester)
    result = pytester.runpytest("--no-on-fail-sound")
    result.assert_outcomes(failed=1)
    assert play_spy == []


def test_ini_disables(pytester, play_spy):
    pytester.makeini("[pytest]\nno_on_fail_sound = true\n")
    _failing_test(pytester)
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)
    assert play_spy == []


def test_no_sound_on_no_tests_collected(pytester, play_spy):
    result = pytester.runpytest()
    assert result.ret == pytest.ExitCode.NO_TESTS_COLLECTED
    assert play_spy == []


def test_missing_file_warns_and_run_unaffected(pytester, caplog):
    _failing_test(pytester)
    missing = pytester.path / "nope.mp3"
    result = pytester.runpytest("--on-fail-sound", str(missing))
    result.assert_outcomes(failed=1)
    assert any(
        "file not found" in message for message in caplog.messages
    )


def test_playback_error_does_not_break_run(pytester, monkeypatch):
    def boom(path):
        raise PlaysoundException("No supported audio backends on this system!")

    monkeypatch.setattr(plugin, "_play_sound", boom)
    _failing_test(pytester)
    result = pytester.runpytest()
    result.assert_outcomes(failed=1)


def test_play_sound_missing_file_is_noop(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(plugin, "playsound", lambda *a, **k: calls.append((a, k)))
    plugin._play_sound(tmp_path / "does-not-exist.mp3")
    assert calls == []


def test_play_sound_existing_file_calls_playsound(tmp_path, monkeypatch):
    sound = tmp_path / "buzz.mp3"
    sound.write_bytes(b"data")
    calls = []
    monkeypatch.setattr(plugin, "playsound", lambda *a, **k: calls.append((a, k)))
    plugin._play_sound(sound)
    assert calls == [((str(sound),), {"block": False})]
