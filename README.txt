JUMPING FROGS — BROWSER AUDIO REVISION

Use this as a separate test folder first. Your Python game and artwork are
inside webgame/. The browser now plays music using HTML Audio rather than
Pygame/SDL audio. Desktop music still uses Pygame.

RUN THE GAME
1. Extract the ZIP.
2. Open a terminal in the extracted folder containing webgame/.
3. Activate your usual Python environment with pygame-ce and pygbag installed.
4. Run: python -m pygbag --no_opt webgame
5. Open the localhost address printed in the terminal (usually localhost:8000).
6. Click the page to start. If you see Enable music, click it once.

For desktop: cd webgame, then run python main.py.

WHAT CHANGED
- Browser builds initialize display and fonts without opening SDL's mixer.
- browser_support.py passes bundled music to browser_audio.js.
- Native audio pauses when the tab becomes hidden or receives pagehide;
  it resumes when you return. It does not depend on a Python shutdown loop.
- An MP3 fallback in browser_music_fallback.json supports older browsers
  without native OGG decoding. Keep this file alongside main.py.
- Canvas CSS enforces a centered 16:9 display with room around it as needed.
- Tutorial text is cached rather than re-rendered each frame.
- Previous game-loop improvements and desktop shutdown fade are retained.

Keep main.py, browser_support.py, browser_audio.js, and
browser_music_fallback.json together, along with the original game assets.
No custom Pygbag template is needed. --no_opt keeps asset filenames unchanged.

SMALL AUDIO-ONLY TEST
Open browser_audio_test.html directly in Chrome or Vivaldi, click it,
let music play, then close the window. This page embeds the music and does
not use Python, Pygame, or the Pygbag runtime. If it still makes repeated
zapping noises, report whether the revised full game does too. This helps
separate game/runtime issues from browser or operating-system audio issues.

CHECK ON YOUR MAC
- Chrome, Vivaldi, Safari: selection, jumping, win/next level, tutorial.
- Resize the window: the whole game should remain 16:9; buttons should align.
- Switch tabs and return: music should pause and resume.
- Close the window while music plays: compare against the old version.

VALIDATION AND LIMITS
Python and JavaScript syntax checks passed. The game ran with real Pygame
and your supplied assets using dummy display/audio drivers; level selection,
selection/jump/undo and graceful quit were exercised. The web Python branch
was tested with a mocked JavaScript bridge and did not initialize SDL audio.
JavaScript lifecycle logic passed tests using stand-in DOM/audio objects.
Pygbag packaging was checked separately.
Actual Mac browser playback and audible shutdown have NOT been verified.
The browser test runtime could not be installed in the execution environment.
This is a targeted fix to test, not a guarantee of silence on every device.

The ZIP retains all source artwork, including unused alternatives. Generated
build/cache folders and macOS archive metadata are omitted. Pygbag regenerates
its build folder. No website has been published or changed.
