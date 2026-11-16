
const W = 1080, H = 1920;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const OUT = '#2a1f1a';            // couleur des contours "cartoon"
let T = null;                     // timings injectés

// ---------------------------------------------------------------- utilitaires
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const easeOutBack = x => { x = clamp(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, k) => a + (b - a) * k;
function rnd(seed) { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

function shape(fill, lw = 6, stroke = OUT) {
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (lw) { ctx.lineWidth = lw; ctx.strokeStyle = stroke; ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.stroke(); }
}
function ell(x, y, rx, ry, fill, lw = 6, rot = 0) { ctx.beginPath(); ctx.ellipse(x, y, Math.abs(rx), Math.abs(ry), rot, 0, Math.PI * 2); shape(fill, lw); }
function rr(x, y, w, h, r, fill, lw = 6) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); shape(fill, lw); }
function poly(pts, fill, lw = 6) { ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]); for (const p of pts.slice(1)) ctx.lineTo(p[0], p[1]); ctx.closePath(); shape(fill, lw); }
function line(x1, y1, x2, y2, col = OUT, lw = 6) { ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineWidth = lw; ctx.strokeStyle = col; ctx.lineCap = 'round'; ctx.stroke(); }
function txt(s, x, y, size, col, font = 'Anton', align = 'center', stroke = 0, sc = OUT) {
  ctx.font = `${size}px ${font}`; ctx.textAlign = align; ctx.textBaseline = 'middle';
  if (stroke) { ctx.lineWidth = stroke; ctx.strokeStyle = sc; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y); }
  ctx.fillStyle = col; ctx.fillText(s, x, y);
}
function shadow(x, y, rx) { ctx.save(); ctx.globalAlpha = .18; ell(x, y, rx, rx * .22, '#000', 0); ctx.restore(); }

// ---------------------------------------------------------------- personnages
// Pigeon. o: {flip, blink, smug, beak, suitcase, phone, tie, hat, bob, look, party}
function pigeon(x, y, s, t, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.flip ? -1 : 1), s);
  const bob = o.bob ?? Math.sin(t * 6) * 4;
  shadow(0, 0, 90);
  // pattes
  line(-22, -40, -28, 0, '#e0707a', 9); line(22, -40, 26, 0, '#e0707a', 9);
  line(-44, 0, -12, 0, '#e0707a', 8); line(8, 0, 42, 0, '#e0707a', 8);
  ctx.translate(0, bob);
  // queue
  poly([[-70, -95], [-150, -60], [-140, -40], [-60, -60]], '#5f6772');
  // corps
  ell(0, -110, 92, 78, '#9aa3ae');
  // ventre clair
  ctx.save(); ctx.beginPath(); ctx.ellipse(0, -110, 92, 78, 0, 0, 7); ctx.clip(); ell(30, -80, 70, 55, '#b6bec8', 0); ctx.restore();
  ell(0, -110, 92, 78, null);
  // aile
  ctx.beginPath(); ctx.moveTo(-60, -140); ctx.quadraticCurveTo(10, -175, 50, -110); ctx.quadraticCurveTo(0, -60, -80, -75); ctx.closePath(); shape('#7d8693');
  line(-40, -100, 10, -100, '#454c56', 7); line(-35, -82, 15, -86, '#454c56', 7);
  if (o.tie) { poly([[48, -150], [62, -150], [70, -95], [55, -80], [42, -95]], '#c0392b', 5); }
  if (o.suit) { // veste de procès
    ctx.save(); ctx.beginPath(); ctx.ellipse(0, -110, 92, 78, 0, 0, 7); ctx.clip();
    ctx.beginPath(); ctx.rect(-120, -200, 160, 200); ctx.fillStyle = '#2c3e50'; ctx.fill(); ctx.restore();
    ell(0, -110, 92, 78, null);
    poly([[48, -150], [62, -150], [70, -95], [55, -80], [42, -95]], '#c0392b', 5);
  }
  // cou irisé + tête
  ctx.save(); ctx.translate(55, -170 + (o.headBob || 0));
  ell(-5, 18, 46, 40, '#5b8f7a', 6);
  ell(-5, 30, 40, 22, '#7a5b9a', 0);
  ell(0, -20, 48, 46, '#7d8693');
  // oeil
  const lk = o.look ?? 1;
  ell(16 * lk, -28, 17, 17, '#f39c12', 5);
  ell(18 * lk, -28, 8, 8, '#111', 0);
  ell(21 * lk, -31, 3, 3, '#fff', 0);
  if (o.blink) { ell(16 * lk, -28, 18, 18, '#7d8693', 5); line(0, -28, 34 * lk, -28, OUT, 5); }
  else if (o.smug) { ctx.save(); ctx.beginPath(); ctx.ellipse(16 * lk, -28, 18, 18, 0, Math.PI, 0); shape('#6c7480', 5); ctx.restore(); }
  if (o.angry) line(0, -55, 34 * lk, -44, OUT, 7);
  // bec
  const bo = o.beak || 0;
  poly([[40, -16], [78, -8 - bo * 4], [40, 0]], '#3a3a3a', 5);
  if (bo > 0) poly([[40, 2], [72, 8 + bo * 10], [40, 10]], '#3a3a3a', 5);
  ell(42, -16, 10, 6, '#f2f2f2', 3);
  if (o.hat === 'party') { poly([[-30, -58], [10, -150], [30, -50]], '#e84393', 5); ell(10, -152, 12, 12, '#fdcb6e', 4); }
  if (o.hat === 'sun') { rr(-40, -80, 100, 24, 10, '#111', 4); }
  ctx.restore();
  if (o.phone) { // téléphone dans l'aile
    ctx.save(); ctx.translate(95, -150); ctx.rotate(-.3); rr(-18, -36, 36, 70, 8, '#222', 4); rr(-12, -28, 24, 48, 4, '#74b9ff', 0); ctx.restore();
    ctx.beginPath(); ctx.moveTo(30, -110); ctx.quadraticCurveTo(90, -100, 95, -140); shape(null, 14, '#7d8693'); line(30, -110, 95, -140, OUT, 0);
  }
  ctx.restore();
  if (o.suitcase) { // valise posée à côté
    const sx = x + (o.flip ? 120 : -170) * s, sy = y;
    ctx.save(); ctx.translate(sx, sy); ctx.scale(s, s);
    rr(-10, -150, 160, 150, 14, '#c0763b'); rr(40, -175, 60, 30, 10, null);
    line(-10, -95, 150, -95, OUT, 5); rr(20, -130, 34, 22, 4, '#f5e6a8', 4); rr(90, -60, 40, 30, 4, '#74b9ff', 4);
    ctx.restore();
  }
}

// Humain "toi" : t-shirt blanc, jean bleu. o: {pose, expr, blink, flip}
function human(x, y, s, t, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.flip ? -1 : 1), s);
  const pose = o.pose || 'stand';
  shadow(0, 0, 110);
  const skin = '#f3c9a4';
  // jambes
  if (pose === 'run') {
    const a = Math.sin(t * 14) * .6;
    ctx.save(); ctx.translate(-20, -330); ctx.rotate(a); rr(-28, 0, 56, 320, 22, (o.pants || '#2f5aa8')); rr(-34, 300, 80, 34, 16, '#222'); ctx.restore();
    ctx.save(); ctx.translate(20, -330); ctx.rotate(-a); rr(-28, 0, 56, 320, 22, (o.pants || '#2f5aa8')); rr(-34, 300, 80, 34, 16, '#222'); ctx.restore();
  } else {
    if (o.skirt) { rr(-50, -300, 34, 280, 16, skin); rr(16, -300, 34, 280, 16, skin); poly([[-90, -360], [90, -360], [120, -200], [-120, -200]], o.skirt); }
    else { rr(-62, -340, 58, 310, 22, (o.pants || '#2f5aa8')); rr(4, -340, 58, 310, 22, (o.pants || '#2f5aa8')); }
    rr(-74, -40, 76, 40, 18, '#222'); rr(0, -40, 76, 40, 18, '#222');
  }
  // torse
  const shirt = o.shirt || '#f7f7f5';
  rr(-90, -640, 180, 330, 50, shirt);
  // bras
  const armL = o.armL ?? (pose === 'shock' ? -2.6 : pose === 'broom' ? -1.2 : 0.15);
  const armR = o.armR ?? (pose === 'shock' ? 2.6 : pose === 'broom' ? -0.9 : -0.15);
  const arm = (ax, ang) => { ctx.save(); ctx.translate(ax, -600); ctx.rotate(ang); rr(-26, -10, 52, 140, 24, shirt); rr(-22, 120, 44, 130, 22, skin); ell(0, 260, 30, 30, skin); if (o.gloves) ell(0, 262, 48, 44, o.gloves, 6);
    if (o.phone && ax > 0) { rr(-22, 230, 44, 86, 8, '#222', 4); rr(-15, 240, 30, 60, 4, '#74b9ff', 0); }
    ctx.restore(); };
  arm(-100, armL); arm(100, armR);
  if (pose === 'broom') { // balai brandi
    ctx.save(); ctx.translate(30, -760); ctx.rotate(.25 + Math.sin(t * 9) * .25);
    rr(-12, -260, 24, 520, 10, '#a0522d'); poly([[-70, -260], [70, -260], [100, -400], [-100, -400]], '#e1b12c');
    for (let i = -80; i <= 80; i += 26) line(i * .9, -270, i * 1.15, -395, '#b8860b', 4);
    ctx.restore();
  }
  // cou + tête
  rr(-26, -690, 52, 60, 10, skin);
  if (o.collar) { rr(-44, -664, 88, 30, 12, '#e74c3c', 5); ell(0, -626, 16, 16, '#f1c40f', 4); }
  ctx.save(); ctx.translate(0, -790);
  ell(0, 0, 105, 120, skin);
  // cheveux
  if (o.bun) ell(0, -140, 60, 50, o.hair || '#5a3a22');
  if (!o.bald) { ctx.beginPath(); ctx.ellipse(0, -30, 108, 100, 0, Math.PI * 1.02, Math.PI * 1.98); ctx.quadraticCurveTo(60, -40, 0, -50); ctx.quadraticCurveTo(-60, -40, -105, -40); shape(o.hair || '#5a3a22'); }
  if (o.longHair) { rr(-118, -40, 46, 200, 22, o.hair || '#5a3a22'); rr(72, -40, 46, 200, 22, o.hair || '#5a3a22'); }
  ell(-102, 10, 16, 26, skin); ell(102, 10, 16, 26, skin);
  if (o.cap) { ctx.beginPath(); ctx.ellipse(0, -60, 108, 80, 0, Math.PI, 0); shape(o.cap); rr(-10, -78, 170, 30, 14, o.cap); }
  const e = o.expr || 'neutral';
  if (o.mask) { ctx.save(); ctx.beginPath(); ctx.ellipse(0, 0, 105, 120, 0, 0, 7); ctx.clip(); ctx.fillStyle = o.mask; ctx.fillRect(-110, -130, 220, 120); ctx.restore(); }
  // yeux
  if (o.blink || e === 'sleep') { line(-55, 5, -25, 5, OUT, 6); line(25, 5, 55, 5, OUT, 6); }
  else {
    const r = e === 'shock' ? 22 : 15;
    ell(-40, 0, r, r + 4, '#fff', 5); ell(40, 0, r, r + 4, '#fff', 5);
    const px = o.lookX ?? 0;
    ell(-40 + px, 4, 8, 9, '#222', 0); ell(40 + px, 4, 8, 9, '#222', 0);
  }
  if (o.glasses) { ell(-40, 2, 34, 30, 'rgba(200,230,255,.25)', 6); ell(40, 2, 34, 30, 'rgba(200,230,255,.25)', 6); line(-6, 0, 6, 0, OUT, 6); }
  // sourcils
  if (e === 'angry') { line(-65, -40, -18, -22, OUT, 9); line(65, -40, 18, -22, OUT, 9); }
  else if (e === 'sad') { line(-65, -25, -20, -40, OUT, 8); line(65, -25, 20, -40, OUT, 8); }
  else if (e === 'shock') { line(-62, -48, -20, -50, OUT, 8); line(62, -48, 20, -50, OUT, 8); }
  else { line(-60, -35, -22, -38, OUT, 7); line(60, -35, 22, -38, OUT, 7); }
  // bouche
  if (e === 'shock') ell(0, 62, 22, 30, '#7a2b2b', 5);
  else if (e === 'angry') { ctx.beginPath(); ctx.roundRect(-40, 45, 80, 30, 8); shape('#fff', 5); line(-40, 60, 40, 60, OUT, 3); }
  else if (e === 'sad') { ctx.beginPath(); ctx.arc(0, 85, 30, Math.PI * 1.15, Math.PI * 1.85); shape(null, 6); }
  else if (e === 'sleep') { ell(0, 60, 10, 8, '#7a2b2b', 4); }
  else { ctx.beginPath(); ctx.arc(0, 40, 30, Math.PI * .15, Math.PI * .85); shape(null, 6); }
  if (e === 'sad' || e === 'cry') { ell(-48, 40 + (t * 120 % 60), 7, 11, '#74b9ff', 3); }
  ctx.restore();
  ctx.restore();
}

// Goéland avocat
function seagull(x, y, s, t, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.flip ? -1 : 1), s);
  shadow(0, 0, 100);
  line(-25, -60, -30, 0, '#f0a35e', 10); line(25, -60, 28, 0, '#f0a35e', 10);
  ctx.translate(0, Math.sin(t * 5) * 3);
  poly([[-80, -140], [-170, -110], [-160, -90], [-70, -100]], '#2d3436');
  ell(0, -150, 95, 100, '#fdfdfd');
  // costume
  ctx.save(); ctx.beginPath(); ctx.ellipse(0, -150, 95, 100, 0, 0, 7); ctx.clip();
  ctx.beginPath(); ctx.rect(-120, -260, 120, 260); ctx.fillStyle = '#1e272e'; ctx.fill();
  ctx.beginPath(); ctx.rect(0, -260, 120, 260); ctx.fillStyle = '#1e272e'; ctx.fill();
  poly([[-30, -240], [30, -240], [0, -120]], '#fff', 0);
  poly([[-10, -225], [10, -225], [16, -150], [0, -130], [-16, -150]], '#e17055', 4);
  ctx.restore(); ell(0, -150, 95, 100, null);
  // tête
  ctx.save(); ctx.translate(30, -290);
  ell(0, 0, 70, 64, '#fdfdfd');
  ell(22, -12, 12, 12, '#f5d76e', 4); ell(25, -12, 6, 6, '#111', 0);
  line(5, -36, 45, -26, OUT, 7);
  const bo = o.beak || 0;
  poly([[55, -6], [140, 4 - bo * 6], [55, 18]], '#f9ca24', 5);
  if (bo) poly([[55, 20], [125, 26 + bo * 14], [55, 30]], '#f9ca24', 5);
  ell(120, 14, 6, 6, '#e74c3c', 0);
  ctx.restore();
  // mallette
  if (o.briefcase !== false) { rr(-150, -110, 110, 80, 10, '#6d4c41'); rr(-115, -128, 40, 22, 6, null); }
  ctx.restore();
}

// Hibou juge
function owl(x, y, s, t, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ell(0, -150, 120, 140, '#1b1b1b'); // robe
  rr(-40, -260, 80, 50, 10, '#fff', 4);
  ctx.save(); ctx.translate(0, -300);
  ell(0, 0, 120, 105, '#8d6e63');
  poly([[-100, -60], [-80, -140], [-40, -80]], '#8d6e63'); poly([[100, -60], [80, -140], [40, -80]], '#8d6e63');
  // perruque de juge
  for (let i = -3; i <= 3; i++) ell(i * 34, -90, 22, 20, '#ecf0f1', 4);
  for (let k of [-1, 1]) for (let j = 0; j < 3; j++) ell(k * 118, -50 + j * 38, 22, 20, '#ecf0f1', 4);
  ell(-45, 0, 42, 42, '#f5f0e1'); ell(45, 0, 42, 42, '#f5f0e1');
  const bl = o.blink ? 1 : 0;
  if (bl) { line(-70, 0, -20, 0, OUT, 6); line(20, 0, 70, 0, OUT, 6); }
  else { ell(-45, 0, 20, 20, '#f39c12', 4); ell(45, 0, 20, 20, '#f39c12', 4); ell(-45, 2, 10, 10, '#111', 0); ell(45, 2, 10, 10, '#111', 0); }
  line(-85, -40, -15, -28, OUT, 9); line(85, -40, 15, -28, OUT, 9);
  poly([[-14, 30], [14, 30], [0, 62]], '#f39c12', 4);
  ctx.restore();
  ctx.restore();
}

// ---------------------------------------------------------------- décors
function sky(top = '#7ec8f2', bot = '#d6f0ff') { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(-400, -400, W + 800, H + 800); }
function clouds(t) { for (let i = 0; i < 4; i++) { const cx = ((i * 380 + t * 18) % 1700) - 300, cy = 160 + i * 90; ctx.globalAlpha = .9; ell(cx, cy, 110, 45, '#fff', 0); ell(cx + 70, cy - 20, 80, 50, '#fff', 0); ell(cx - 70, cy + 5, 70, 35, '#fff', 0); ctx.globalAlpha = 1; } }

function buildingWall(night) {
  ctx.fillStyle = night ? '#4a4560' : '#e8c9a0'; ctx.fillRect(-400, -400, W + 800, 1700 + 400);
  ctx.globalAlpha = .12; for (let y = -400; y < 1300; y += 60) { ctx.fillStyle = '#000'; ctx.fillRect(-400, y, W + 800, 3); } ctx.globalAlpha = 1;
}
function windowFrame(x, y, w, h, night, open = 0) {
  rr(x - 24, y - 24, w + 48, h + 48, 12, night ? '#c8c2d8' : '#fff');
  rr(x, y, w, h, 4, night ? '#ffd56b' : '#6e5a7e');
  if (!night) { ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    rr(x + 40, y + h - 260, 300, 200, 30, '#b5523b', 0); rr(x + w - 200, y + 80, 140, 110, 6, '#f1c40f', 0); ctx.restore(); }
  // battants
  const bw = w / 2;
  ctx.save(); ctx.globalAlpha = .35;
  rr(x + 4, y + 4, bw * (1 - open) - 8, h - 8, 4, '#bfe6ff', 4);
  rr(x + w - bw * (1 - open) + 4, y + 4, bw * (1 - open) - 8, h - 8, 4, '#bfe6ff', 4);
  ctx.restore();
  rr(x, y, w, h, 4, null, 10);
  if (open < .5) line(x + w / 2, y, x + w / 2, y + h, '#fff', 14);
}
function balconyFloor(night) {
  ctx.fillStyle = night ? '#5b5470' : '#b9a690'; ctx.fillRect(-400, 1300, W + 800, 1000);
  for (let i = -6; i < 16; i++) line(i * 120, 1300, i * 120 - (i - 4.5) * 90, 2300, night ? '#4a4460' : '#a39079', 4);
}
function railing(night) {
  const c = night ? '#1d1b29' : '#2d3436';
  rr(-200, 1480, W + 400, 26, 10, c, 0);
  for (let x = -100; x < W + 200; x += 70) rr(x, 1500, 14, 300, 6, c, 0);
}
function room() {
  ctx.fillStyle = '#c9a66b'; ctx.fillRect(-400, -400, W + 800, 1800);
  ctx.fillStyle = '#8b5a3c'; ctx.fillRect(-400, 1400, W + 800, 900);
  for (let y = 1430; y < 2300; y += 70) line(-400, y, W + 400, y, '#7a4c31', 4);
  rr(300, 420, 480, 320, 8, '#2b2b2b'); rr(330, 450, 420, 260, 4, '#e6b84f', 0);
  ell(540, 1700, 520, 170, '#d35b45', 0);
}
function sofa(x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  rr(-300, -330, 600, 230, 60, '#7b3f2b'); rr(-330, -200, 660, 200, 50, '#8e4a33');
  rr(-360, -260, 110, 270, 50, '#7b3f2b'); rr(250, -260, 110, 270, 50, '#7b3f2b');
  ctx.restore();
}
function courtroom() {
  ctx.fillStyle = '#6d4c41'; ctx.fillRect(-400, -400, W + 800, 2800);
  for (let x = -400; x < W + 400; x += 180) { rr(x + 15, 150, 150, 900, 10, '#7b5a4d', 4); }
  // blason
  ell(540, 260, 110, 110, '#f1c40f'); txt('⚖', 540, 265, 120, OUT, 'serif');
  ctx.fillStyle = '#4e342e'; ctx.fillRect(-400, 1350, W + 800, 1200);
}

// ---------------------------------------------------------------- sous-titres (style "mot par mot")
let GROUPS = [];
function buildGroups() {
  GROUPS = [];
  for (const s of T.segments) {
    // rattache la ponctuation isolée au mot précédent
    const ws = [];
    for (const w of s.words) { if (/^[?!:;…]+$/.test(w.w) && ws.length) { ws[ws.length - 1].w += ' ' + w.w; ws[ws.length - 1].e = w.e; } else ws.push({ ...w }); }
    let cur = [];
    const flush = () => { if (cur.length) GROUPS.push(cur); cur = []; };
    for (const w of ws) {
      const len = cur.reduce((a, b) => a + b.w.length + 1, 0);
      if (cur.length && (len + w.w.length > 16 || cur.length >= 3)) flush();
      cur.push(w);
      if (/[.!?…]$/.test(w.w) || (/,$/.test(w.w) && cur.length > 1)) flush();
    }
    flush();
  }
  // chaque groupe reste affiché jusqu'au début du suivant (max +0.6s)
  GROUPS.forEach((g, i) => { g.s = g[0].s; const nx = GROUPS[i + 1]; g.e = nx ? Math.min(nx[0].s, g[g.length - 1].e + .6) : g[g.length - 1].e + .6; });
}
function subtitles(t) {
  const g = GROUPS.find(g => t >= g.s && t < g.e);
  if (!g) return;
  const size = 98;
  ctx.font = `900 ${size}px Mont`;
  const words = g.map(w => w.w);
  // découpe en 2 lignes si trop large
  const maxW = 900; let lines = [[]], lw = 0;
  for (const w of g) { const ww = ctx.measureText(w.w + ' ').width + 22; if (lw + ww > maxW && lines[lines.length - 1].length) { lines.push([]); lw = 0; } lines[lines.length - 1].push(w); lw += ww; }
  const pop = easeOutBack((t - g.s) / .12);
  const y0 = 1240 - (lines.length - 1) * size * .55;
  ctx.save(); ctx.translate(540, y0); ctx.scale(lerp(.7, 1, pop), lerp(.7, 1, pop));
  lines.forEach((ln, li) => {
    const widths = ln.map(w => ctx.measureText(w.w).width), sp = ctx.measureText(' ').width + 22;
    const tot = widths.reduce((a, b) => a + b, 0) + sp * (ln.length - 1);
    let x = -tot / 2;
    ln.forEach((w, i) => {
      const active = t >= w.s && t < w.e + .05;
      const col = w.hl ? '#ffd32a' : '#ffffff';
      ctx.save(); ctx.translate(x + widths[i] / 2, li * size * 1.1);
      if (active) ctx.scale(1.12, 1.12);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.lineWidth = 20; ctx.strokeStyle = '#000'; ctx.lineJoin = 'round'; ctx.strokeText(w.w, 0, 0);
      ctx.fillStyle = (t < w.s) ? (w.hl ? '#ffd32a' : '#ffffff') : col; ctx.fillText(w.w, 0, 0);
      ctx.restore();
      x += widths[i] + sp;
    });
  });
  ctx.restore();
}

// ---------------------------------------------------------------- rendu d'une frame
function sceneSpans() {
  const spans = [];
  for (const s of T.segments) {
    const last = spans[spans.length - 1];
    if (last && last.scene === s.scene) last.end = s.end; else spans.push({ scene: s.scene, start: s.start, end: s.end });
  }
  spans[0].start = 0; spans[spans.length - 1].end = T.duration;
  for (let i = 0; i < spans.length - 1; i++) spans[i].end = spans[i + 1].start;
  return spans;
}
let SPANS = [];
window.init = (timings) => { T = timings; buildGroups(); SPANS = sceneSpans(); };
window.render = (t) => {
  const sp = SPANS.find(s => t >= s.start && t < s.end) || SPANS[SPANS.length - 1];
  const lt = t - sp.start, d = sp.end - sp.start;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  ctx.save();
  // caméra : zoom "punch" à l'entrée + léger Ken Burns
  const punch = 1 + .08 * (1 - ease(lt / .35));
  const kb = 1 + .05 * (lt / d);
  const z = punch * kb;
  ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  window.SCENES[sp.scene](lt, d, t);
  ctx.restore();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  // flash blanc de transition
  if (lt < .12 && sp.start > 0) { ctx.globalAlpha = 1 - lt / .12; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); ctx.globalAlpha = 1; }
  subtitles(t);
  // filigrane
  ctx.globalAlpha = .55; txt(window.HANDLE || '@histoires.debiles', 540, 1830, 40, '#fff', 'Mont', 'center', 6, '#000'); ctx.globalAlpha = 1;
};
window.frame = (t, q = .9) => { render(t); return cv.toDataURL('image/jpeg', q); };

window.wordTime = (re, n = 0, scene = null) => {
  let k = 0;
  for (const s of T.segments) { if (scene && s.scene !== scene) continue;
    for (const w of s.words) if (re.test(w.w)) { if (k === n) return w.s; k++; } }
  return 1e9;
};
window.sceneStart = (name) => (SPANS.find(s => s.scene === name) || { start: 0 }).start;
