// node render.js            -> rend la vidéo complète (out/video.mp4)
// node render.js 3.2 10 25  -> rend des images fixes aux temps donnés (out/still_*.jpg)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const FPS = 30;
(async () => {
  fs.mkdirSync('out', { recursive: true });
  const timings = JSON.parse(fs.readFileSync('timings.json', 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve('scene.html'));
  await page.evaluate(async t => { await document.fonts.load('900 90px Mont'); await document.fonts.load('90px Anton'); init(t); }, timings);
  const stills = process.argv.slice(2).map(Number);
  if (stills.length) {
    for (const t of stills) {
      const d = await page.evaluate(t => frame(t), t);
      fs.writeFileSync(`out/still_${t}.jpg`, Buffer.from(d.split(',')[1], 'base64'));
    }
    await browser.close(); return;
  }
  const n = Math.ceil(timings.duration * FPS);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', 'audio_mix.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-shortest', '-movflags', '+faststart', 'out/video.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const d = await page.evaluate(t => frame(t, .92), i / FPS);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  await browser.close(); console.log('OK out/video.mp4');
})();
