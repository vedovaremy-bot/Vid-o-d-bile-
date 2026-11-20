// Helpers partagés par les scènes (chargés après engine.js)
window.lw = (re, scene, n = 0) => wordTime(re, n, scene) - sceneStart(scene);
window.popText = function (s, x, y, size, col, t0, lt, rot = -.06, until = 1e9) {
  if (lt < t0 || lt > until) return;
  const k = easeOutBack((lt - t0) / .3);
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(rot); txt(s, 0, 0, size, col, 'Anton', 'center', size * .13); ctx.restore();
};
window.bubble = function (x, y, w, h, s, size, tailX = 0, t0 = 0, lt = 1, until = 1e9) {
  if (lt < t0 || lt > until) return; const k = easeOutBack((lt - t0) / .3);
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
  rr(-w / 2, -h / 2, w, h, 40, '#fff'); poly([[tailX - 24, h / 2 - 4], [tailX + 24, h / 2 - 4], [tailX - 4, h / 2 + 56]], '#fff'); line(tailX - 20, h / 2 - 2, tailX + 20, h / 2 - 2, '#fff', 10);
  txt(s, 0, 4, size, OUT, 'Anton'); ctx.restore();
};
window.heart = function (x, y, r, fill, lw2 = 8) {
  ctx.beginPath(); ctx.moveTo(x, y + r * .9);
  ctx.bezierCurveTo(x - r * 1.6, y - r * .1, x - r * .9, y - r * 1.3, x, y - r * .45);
  ctx.bezierCurveTo(x + r * .9, y - r * 1.3, x + r * 1.6, y - r * .1, x, y + r * .9); shape(fill, lw2);
};
window.hearts = function (g, x, y, n = 5) { for (let i = 0; i < n; i++) { const k = (g * .7 + i / n) % 1; ctx.globalAlpha = 1 - k; txt('♥', x + Math.sin(i * 2 + g * 2) * 80, y - k * 400, 60 + (i % 3) * 20, '#ff4757', 'serif', 'center', 6); } ctx.globalAlpha = 1; };
window.confetti = function (g, n = 60) { const R = rnd(13); for (let i = 0; i < n; i++) { const x = R() * W, sp = 200 + R() * 300, y = ((g * sp + R() * H) % (H + 100)) - 50; ctx.save(); ctx.translate(x, y); ctx.rotate(g * 4 + i); rr(-12, -6, 24, 12, 3, ['#ff4757', '#ffd32a', '#2ed573', '#1e90ff', '#ff6b81'][i % 5], 0); ctx.restore(); } };
window.likeButton = function (lt, lk, g, y = 300) {
  if (lt < lk - .3) return;
  const k = easeOutBack((lt - lk + .3) / .35), beat = 1 + Math.max(0, Math.sin(g * 9)) * .08;
  ctx.save(); ctx.translate(540, y); ctx.scale(k * beat * .85, k * beat * .85); ell(0, 0, 200, 200, '#fff', 10); heart(0, 10, 110, '#ff3838', 10); ctx.restore();
  const tap = Math.abs(Math.sin(g * 6)) * 30; ctx.save(); ctx.translate(760 + tap * .5, y + 150 + tap); ctx.rotate(-.6); rr(-36, 0, 72, 260, 36, '#f3c9a4'); rr(-22, 8, 44, 46, 14, '#fbe3d2', 4); ctx.restore();
};
window.subscribe = function (lt, y = 330) { const p = easeOutBack((lt - .1) / .4); if (p > 0) { ctx.save(); ctx.translate(540, y); ctx.scale(p, p); rr(-300, -80, 600, 160, 80, '#ff3838', 0); txt("S'ABONNER", 0, 6, 90, '#fff', 'Anton'); ctx.restore(); } };
window.apartment = function (wall = '#ffeaa7', floor = '#b5835a') {
  ctx.fillStyle = wall; ctx.fillRect(-400, -400, W + 800, 1800);
  rr(640, 260, 320, 260, 10, '#6d4c41'); rr(660, 280, 280, 220, 4, '#74b9ff', 0);
  ctx.fillStyle = floor; ctx.fillRect(-400, 1400, W + 800, 900);
};
window.HANDLE = '@histoires.debiles';
