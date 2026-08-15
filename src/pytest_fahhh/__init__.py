"""pytest-fahhh: a pytest plugin that plays FAHHH meme sound when a test session fails.

The plugin registers itself via the ``pytest11`` entry point and is loaded
automatically. On session failure it plays the bundled ``sound.mp3`` (or a
custom file given via ``--on-fail-sound``) using ``playsound3`` in the
background, without ever breaking the test run.
"""
