"""Small Pygbag bridge; desktop playback stays in Pygame."""
import base64
import json
from pathlib import Path


def start_music(filename):
    import platform  # Pygbag provides platform.window inside the browser.
    folder = Path(__file__).resolve().parent
    data = base64.b64encode((folder / filename).read_bytes()).decode('ascii')
    source = 'data:audio/ogg;base64,' + data
    script = (folder / 'browser_audio.js').read_text()
    fallback = json.loads((folder / 'browser_music_fallback.json').read_text())
    script = script.replace('__MUSIC_DATA__', json.dumps(source))
    script = script.replace('__MUSIC_FALLBACK__', json.dumps(fallback))
    platform.window.eval(script)


def stop_music():
    import platform
    platform.window.eval('if (window.frogAudio) window.frogAudio.stop();')
