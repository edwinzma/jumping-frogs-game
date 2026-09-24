/* Browser-native music: no SDL/Pygame audio device on the web. */
(() => {
    if (window.frogAudio) window.frogAudio.dispose();
    const style = document.getElementById('frog-layout') || document.createElement('style');
    style.id = 'frog-layout';
    style.textContent = `
      html, body { margin:0; padding:0; overflow:hidden; background:#183f3c; }
      canvas#canvas.emscripten {
        position:fixed !important; left:50% !important; top:50% !important;
        right:auto !important; bottom:auto !important; margin:0 !important;
        padding:0 !important; border:0 !important;
        width:min(100vw, 177.77777778vh) !important;
        height:min(100vh, 56.25vw) !important;
        transform:translate(-50%, -50%) !important;
        object-fit:contain; aspect-ratio:16/9;
      }
      #frog-audio-start {position:fixed;bottom:12px;left:12px;z-index:1000000;
        padding:10px 16px;border-radius:12px;border:0;background:#fff9de;color:#204b31;}
    `;
    document.head.appendChild(style);
    const audio = new Audio();
    // Native OGG support varies on older Safari; use MP3 there.
    audio.src = audio.canPlayType('audio/ogg; codecs="vorbis"')
        ? __MUSIC_DATA__ : __MUSIC_FALLBACK__;
    audio.loop = true;
    audio.volume = 0.3;
    audio.preload = 'auto';
    let wanted = true, suspended = document.hidden, disposed = false, starting = false;
    const button = document.createElement('button');
    button.id = 'frog-audio-start'; button.textContent = 'Enable music'; button.hidden = true;
    document.body.appendChild(button);
    async function play() {
        if (disposed || !wanted || suspended || document.hidden || starting || !audio.paused) return;
        starting = true;
        try {
            await audio.play();
            // A play promise can resolve after pagehide; do not restart on a hidden page.
            if (disposed || !wanted || suspended || document.hidden) audio.pause();
            else button.hidden = true;
        } catch (error) {
            if (!disposed && wanted && !suspended && !document.hidden) button.hidden = false;
            if (error.name !== 'NotAllowedError' && error.name !== 'AbortError')
                console.warn('Jumping Frogs music:', error);
        } finally { starting = false; }
    }
    function pause() { suspended = true; audio.pause(); }
    function visible() { suspended = document.hidden; if (suspended) audio.pause(); else play(); }
    function shown() { suspended = document.hidden; if (!suspended) play(); }
    function gesture() { play(); }
    function audioError() { button.textContent = 'Music unavailable'; button.disabled = true; button.hidden = false; }
    document.addEventListener('visibilitychange', visible);
    window.addEventListener('pagehide', pause);
    window.addEventListener('pageshow', shown);
    window.addEventListener('pointerdown', gesture);
    window.addEventListener('keydown', gesture);
    audio.addEventListener('error', audioError);
    button.addEventListener('click', gesture);
    window.frogAudio = {
        audio,
        stop() { wanted = false; audio.pause(); button.hidden = true; },
        dispose() {
            disposed = true; wanted = false; audio.pause();
            document.removeEventListener('visibilitychange', visible);
            window.removeEventListener('pagehide', pause);
            window.removeEventListener('pageshow', shown);
            window.removeEventListener('pointerdown', gesture);
            window.removeEventListener('keydown', gesture);
            audio.removeEventListener('error', audioError);
            button.remove(); audio.removeAttribute('src'); audio.load();
        }
    };
    play();
})();
