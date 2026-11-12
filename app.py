 
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="World Explorer 3D", page_icon="🌲", layout="wide")
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background:#06120d;}
.block-container {padding:0 !important; max-width:100% !important;}
iframe {border:0;}
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>World Explorer 3D</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07130e;font-family:Arial,Helvetica,sans-serif}
#game{position:fixed;inset:0}
canvas{display:block;width:100%;height:100%}
#hud{position:fixed;top:16px;left:16px;z-index:5;color:white;text-shadow:0 2px 8px #000;font-weight:700;pointer-events:none}
#crystalCount{font-size:20px;background:rgba(3,20,13,.72);border:1px solid rgba(255,255,255,.2);padding:10px 14px;border-radius:12px;backdrop-filter:blur(8px)}
#warning{margin-top:9px;color:#ffcf65;font-size:14px;max-width:270px}
#hint{position:fixed;top:16px;right:16px;z-index:5;color:#fff;background:rgba(3,20,13,.65);padding:10px 13px;border-radius:10px;font-size:12px;line-height:1.7;text-align:right;pointer-events:none}
#overlay{position:fixed;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(2,15,9,.88),rgba(3,30,17,.72));color:#fff;text-align:center;padding:22px}
.panel{width:min(560px,94vw);padding:34px 28px;border:1px solid rgba(255,255,255,.22);border-radius:24px;background:rgba(7,25,15,.82);box-shadow:0 20px 80px #0009;backdrop-filter:blur(14px)}
.panel h1{font-size:clamp(32px,7vw,58px);margin:0 0 12px;letter-spacing:1px;color:#a8ffcb;text-shadow:0 0 24px #20ff8b66}
.panel p{font-size:16px;line-height:1.6;color:#e0f2e7;margin:8px 0 22px}
button{border:0;border-radius:999px;padding:14px 28px;background:linear-gradient(135deg,#5cff9b,#00c978);color:#042012;font-weight:900;font-size:16px;cursor:pointer;box-shadow:0 8px 26px #00d87855}
#touch{position:fixed;bottom:20px;left:20px;z-index:6;display:none;gap:8px;align-items:flex-end;user-select:none;touch-action:none}
.pad{display:grid;grid-template-columns:repeat(3,48px);grid-template-rows:repeat(2,48px);gap:5px}
.touchbtn{width:48px;height:48px;border-radius:13px;background:#123b2bd9;border:1px solid #b8ffcf88;color:white;font-size:19px;font-weight:bold;display:flex;align-items:center;justify-content:center;touch-action:none;box-shadow:none;padding:0}
#actions{position:fixed;bottom:25px;right:20px;z-index:6;display:none;gap:9px;flex-direction:column}
#actions .touchbtn{width:76px;height:58px;font-size:12px}
@media (pointer:coarse){#touch,#actions{display:flex}#hint{display:none}}
</style>
</head>
<body>
<div id="game"></div>
<div id="hud">
  <div id="crystalCount">💎 Crystals: 0 / 15</div>
  <div id="warning"></div>
</div>
<div id="hint">
  W A S D — Move<br>
  SHIFT — Sprint<br>
  SPACE — Jump<br>
  Mouse drag — Look around<br>
  E — Collect nearby crystal
</div>

<div id="touch">
  <div class="pad">
    <button class="touchbtn" data-key="w" style="grid-column:2;grid-row:1">▲</button>
    <button class="touchbtn" data-key="a" style="grid-column:1;grid-row:2">◀</button>
    <button class="touchbtn" data-key="s" style="grid-column:2;grid-row:2">▼</button>
    <button class="touchbtn" data-key="d" style="grid-column:3;grid-row:2">▶</button>
  </div>
</div>

<div id="actions">
  <button class="touchbtn" id="jumpBtn">JUMP</button>
  <button class="touchbtn" id="sprintBtn">SPRINT</button>
  <button class="touchbtn" id="collectBtn">COLLECT</button>
</div>

<div id="overlay">
  <div class="panel">
    <h1 id="panelTitle">WORLD EXPLORER</h1>
    <p id="panelText">
      Explore the forest and collect all 15 glowing crystals.
      Watch out — a fast wolf is hunting you!
      <br><br>
      Use WASD to move, SHIFT to sprint, and SPACE to jump.
    </p>
    <button id="startBtn">ENTER THE FOREST</button>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(() => {
'use strict';

const mount = document.getElementById('game');
const overlay = document.getElementById('overlay');
const title = document.getElementById('panelTitle');
const panelText = document.getElementById('panelText');
const startBtn = document.getElementById('startBtn');
const countEl = document.getElementById('crystalCount');
const warningEl = document.getElementById('warning');

if (!window.THREE) {
  panelText.textContent = 'Three.js could not load. Check your internet connection and refresh.';
  return;
}

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x8cc9e8);
scene.fog = new THREE.FogExp2(0x9bcbb5, 0.0065);

const camera = new THREE.PerspectiveCamera(
  70, innerWidth / innerHeight, 0.1, 650
);
camera.position.set(0, 2.4, 8);

const renderer = new THREE.WebGLRenderer({
  antialias: true,
  powerPreference: 'high-performance',
  alpha: false
});

renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.22;
mount.appendChild(renderer.domElement);

// Lighting
scene.add(new THREE.HemisphereLight(0xdaf4ff, 0x35502a, 1.45));

const sun = new THREE.DirectionalLight(0xfff1d1, 2.25);
sun.position.set(-65, 100, 45);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -90;
sun.shadow.camera.right = 90;
sun.shadow.camera.top = 90;
sun.shadow.camera.bottom = -90;
sun.shadow.bias = -0.00025;
sun.shadow.normalBias = 0.025;
scene.add(sun);

const fillLight = new THREE.DirectionalLight(0x8acbff, 0.55);
fillLight.position.set(45, 35, -55);
scene.add(fillLight);

// High-resolution procedural texture helper
function canvasTexture(draw, w=1024, h=1024, repeatX=1, repeatY=1) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;

  const ctx = c.getContext('2d');
  draw(ctx, w, h);

  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(repeatX, repeatY);
  t.anisotropy = renderer.capabilities.getMaxAnisotropy();
  t.encoding = THREE.sRGBEncoding;

  return t;
}

// 4K ground texture
const groundTex = canvasTexture((ctx, w, h) => {
  ctx.fillStyle = '#496b36';
  ctx.fillRect(0, 0, w, h);

  for (let i = 0; i < 26000; i++) {
    const x = Math.random() * w;
    const y = Math.random() * h;
    const r = 1 + Math.random() * 8;

    const colors = [
      '#284b27', '#638b3c', '#91a84a',
      '#35552b', '#b0a45b', '#73533a', '#3d7140'
    ];

    ctx.globalAlpha = 0.12 + Math.random() * 0.32;
    ctx.fillStyle = colors[(Math.random() * colors.length) | 0];

    ctx.beginPath();
    ctx.ellipse(
      x, y, r, r * (0.35 + Math.random()),
      Math.random() * 3, 0, Math.PI * 2
    );
    ctx.fill();
  }

  ctx.globalAlpha = 1;
}, 4096, 4096, 18, 18);

const groundBump = canvasTexture((ctx, w, h) => {
  ctx.fillStyle = '#777';
  ctx.fillRect(0, 0, w, h);

  for (let i = 0; i < 18000; i++) {
    const v = 70 + Math.random() * 120;
    ctx.fillStyle = `rgb(${v},${v},${v})`;
    ctx.beginPath();
    ctx.arc(
      Math.random() * w,
      Math.random() * h,
      1 + Math.random() * 5,
      0, Math.PI * 2
    );
    ctx.fill();
  }
}, 1024, 1024, 18, 18);

const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(420, 420, 1, 1),
  new THREE.MeshStandardMaterial({
    map: groundTex,
    bumpMap: groundBump,
    bumpScale: 0.18,
    roughness: 1
  })
);

ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.08;
ground.receiveShadow = true;
scene.add(ground);

// Detailed bark texture
const barkTex = canvasTexture((ctx, w, h) => {
  ctx.fillStyle = '#65402a';
  ctx.fillRect(0, 0, w, h);

  for (let i = 0; i < 950; i++) {
    ctx.strokeStyle = Math.random() > 0.5 ? '#986744' : '#34251d';
    ctx.globalAlpha = 0.18 + Math.random() * 0.35;
    ctx.lineWidth = 1 + Math.random() * 5;

    const x = Math.random() * w;

    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.bezierCurveTo(
      x - 20, h * 0.3,
      x + 20, h * 0.7,
      x + (Math.random() - 0.5) * 20, h
    );
    ctx.stroke();
  }

  ctx.globalAlpha = 1;
}, 1024, 1024, 1, 2);

const barkMat = new THREE.MeshStandardMaterial({
  map: barkTex,
  color: 0xffffff,
  roughness: 0.94,
  bumpMap: barkTex,
  bumpScale: 0.12
});

const leafMats = [
  0x176b35, 0x238b3d, 0x3a9d45,
  0x4eaa49, 0x286f31
].map(c => new THREE.MeshStandardMaterial({
  color: c,
  roughness: 0.88
}));

const leafGeo = new THREE.IcosahedronGeometry(1, 2);
const trunkGeo = new THREE.CylinderGeometry(0.34, 0.62, 7.4, 12, 5);
const branchGeo = new THREE.CylinderGeometry(0.09, 0.2, 2.5, 8, 2);

// Realistic layered trees
function makeTree(x, z, scale=1) {
  const tree = new THREE.Group();
  tree.position.set(x, 0, z);
  tree.scale.setScalar(scale);

  const trunk = new THREE.Mesh(trunkGeo, barkMat);
  trunk.position.y = 3.65;
  trunk.castShadow = true;
  trunk.receiveShadow = true;
  tree.add(trunk);

  for (let b = 0; b < 5; b++) {
    const a = b * Math.PI * 2 / 5 + 0.3;
    const branch = new THREE.Mesh(branchGeo, barkMat);

    branch.position.set(
      Math.cos(a) * 0.62,
      3.4 + b * 0.48,
      Math.sin(a) * 0.62
    );

    branch.rotation.z = -Math.cos(a) * 0.65;
    branch.rotation.x = Math.sin(a) * 0.65;
    branch.castShadow = true;
    tree.add(branch);
  }

  // Dense irregular canopy clusters
  for (let i = 0; i < 26; i++) {
    const y = 5.4 + Math.random() * 4.2;
    const a = Math.random() * Math.PI * 2;
    const radius = (1.0 + Math.random() * 2.2) *
      (1 - (y - 5.4) / 9);

    const s = 0.85 + Math.random() * 1.0;

    const leaf = new THREE.Mesh(
      leafGeo,
      leafMats[(Math.random() * leafMats.length) | 0]
    );

    leaf.position.set(
      Math.cos(a) * radius,
      y,
      Math.sin(a) * radius
    );

    leaf.scale.set(s * 1.2, s, s * 1.1);
    leaf.rotation.set(
      Math.random() * 2,
      Math.random() * 3,
      Math.random() * 2
    );

    leaf.castShadow = true;
    leaf.receiveShadow = true;
    tree.add(leaf);
  }

  for (let i = 0; i < 5; i++) {
    const twig = new THREE.Mesh(branchGeo, barkMat);

    twig.position.set(
      (Math.random() - 0.5) * 1.8,
      5 + Math.random() * 2,
      (Math.random() - 0.5) * 1.8
    );

    twig.scale.set(0.35, 0.7, 0.35);
    twig.rotation.z = (Math.random() - 0.5) * 1.2;
    tree.add(twig);
  }

  scene.add(tree);
  return tree;
}

// Main forest, leaving an open central area
for (let i = 0; i < 115; i++) {
  let x = (Math.random() - 0.5) * 190;
  let z = (Math.random() - 0.5) * 190;

  if (Math.abs(x) < 17 && Math.abs(z) < 17) {
    i--;
    continue;
  }

  makeTree(x, z, 0.78 + Math.random() * 0.62);
}

// Distant forest horizon
for (let i = 0; i < 85; i++) {
  const a = Math.random() * Math.PI * 2;
  const r = 105 + Math.random() * 65;

  makeTree(
    Math.cos(a) * r,
    Math.sin(a) * r,
    0.9 + Math.random() * 0.65
  );
}

// Natural rocks
const rockGeo = new THREE.DodecahedronGeometry(1, 1);

const rockMats = [
  0x727d75, 0x8b887a, 0x586b64, 0x9a927f
].map(c => new THREE.MeshStandardMaterial({
  color: c,
  roughness: 1
}));

for (let i = 0; i < 95; i++) {
  const x = (Math.random() - 0.5) * 180;
  const z = (Math.random() - 0.5) * 180;

  if (Math.abs(x) < 13 && Math.abs(z) < 13) continue;

  const rock = new THREE.Mesh(
    rockGeo,
    rockMats[(Math.random() * rockMats.length) | 0]
  );

  const s = 0.25 + Math.random() * 1.15;

  rock.position.set(x, s * 0.45, z);
  rock.scale.set(s * 1.3, s * 0.75, s);
  rock.rotation.set(Math.random(), Math.random() * 3, Math.random());
  rock.castShadow = true;
  rock.receiveShadow = true;
  scene.add(rock);
}

// Grass clumps
const grassMat = new THREE.MeshStandardMaterial({
  color: 0x5f9d42,
  side: THREE.DoubleSide,
  roughness: 1
});

const grassGeo = new THREE.BufferGeometry();
const verts = [];

for (let i = 0; i < 3; i++) {
  const a = i * Math.PI / 3;
  const x = Math.cos(a) * 0.16;
  const z = Math.sin(a) * 0.16;

  verts.push(-x, 0, -z, x, 0, z, 0, 0.65, 0);
}

grassGeo.setAttribute(
  'position',
  new THREE.Float32BufferAttribute(verts, 3)
);
grassGeo.computeVertexNormals();

for (let i = 0; i < 240; i++) {
  const x = (Math.random() - 0.5) * 160;
  const z = (Math.random() - 0.5) * 160;

  if (Math.abs(x) < 12 && Math.abs(z) < 12) continue;

  const g = new THREE.Mesh(grassGeo, grassMat);
  g.position.set(x, 0, z);
  g.scale.setScalar(0.45 + Math.random() * 0.8);
  g.rotation.y = Math.random() * Math.PI;
  scene.add(g);
}

// 15 collectible crystals
const crystals = [];
const crystalGeo = new THREE.OctahedronGeometry(0.72, 1);

const crystalMat = new THREE.MeshPhysicalMaterial({
  color: 0x39eaff,
  emissive: 0x087bff,
  emissiveIntensity: 1.5,
  metalness: 0.28,
  roughness: 0.12,
  clearcoat: 1,
  clearcoatRoughness: 0.08
});

for (let i = 0; i < 15; i++) {
  let x, z;

  do {
    x = (Math.random() - 0.5) * 130;
    z = (Math.random() - 0.5) * 130;
  } while (Math.abs(x) < 12 && Math.abs(z) < 12);

  const group = new THREE.Group();
  group.position.set(x, 1.25, z);

  const gem = new THREE.Mesh(crystalGeo, crystalMat);
  gem.scale.set(0.75, 1.35, 0.75);
  gem.rotation.y = Math.random() * 2;
  gem.castShadow = true;
  group.add(gem);

  const glow = new THREE.PointLight(0x20cfff, 2.2, 9);
  glow.position.y = 0.2;
  group.add(glow);

  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(0.9, 0.035, 8, 32),
    new THREE.MeshBasicMaterial({
      color: 0x80f5ff,
      transparent: true,
      opacity: 0.8
    })
  );

  ring.rotation.x = Math.PI / 2;
  ring.position.y = -0.8;
  group.add(ring);

  scene.add(group);
  crystals.push({
    group,
    active: true,
    phase: Math.random() * 6
  });
}

// Player model
const player = {
  x: 0,
  z: 0,
  y: 0,
  vy: 0,
  onGround: true
};

const playerGroup = new THREE.Group();

const playerMaterial = new THREE.MeshStandardMaterial({
  color: 0x2f83ff,
  roughness: 0.55
});

const body = new THREE.Mesh(
  new THREE.CylinderGeometry(0.42, 0.42, 0.95, 16, 1),
  playerMaterial
);

body.position.y = 1.0;
body.castShadow = true;
playerGroup.add(body);

const bodyTop = new THREE.Mesh(
  new THREE.SphereGeometry(0.42, 16, 12),
  playerMaterial
);

bodyTop.position.y = 1.47;
playerGroup.add(bodyTop);

const bodyBottom = new THREE.Mesh(
  new THREE.SphereGeometry(0.42, 16, 12),
  playerMaterial
);

bodyBottom.position.y = 0.53;
playerGroup.add(bodyBottom);

const head = new THREE.Mesh(
  new THREE.SphereGeometry(0.32, 16, 12),
  new THREE.MeshStandardMaterial({
    color: 0xffc99c,
    roughness: 0.75
  })
);

head.position.y = 1.85;
head.castShadow = true;
playerGroup.add(head);
scene.add(playerGroup);

// Wolf model
const wolf = new THREE.Group();

const wolfMat = new THREE.MeshStandardMaterial({
  color: 0x555b60,
  roughness: 0.9
});

const darkMat = new THREE.MeshStandardMaterial({
  color: 0x252a30,
  roughness: 0.8
});

const muzzleMat = new THREE.MeshStandardMaterial({
  color: 0x9a9b98,
  roughness: 0.8
});

function wolfPart(geo, mat, pos, scale) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(...pos);

  if (scale) {
    m.scale.set(...scale);
  }

  m.castShadow = true;
  m.receiveShadow = true;
  wolf.add(m);

  return m;
}

wolfPart(
  new THREE.SphereGeometry(1, 20, 16),
  wolfMat,
  [0, 1.05, 0],
  [0.72, 0.72, 1.25]
);

wolfPart(
  new THREE.SphereGeometry(0.58, 18, 14),
  wolfMat,
  [0, 1.62, 0.72],
  [0.72, 0.78, 0.72]
);

wolfPart(
  new THREE.SphereGeometry(0.4, 16, 12),
  muzzleMat,
  [0, 1.43, 1.35],
  [0.75, 0.52, 0.8]
);

wolfPart(
  new THREE.SphereGeometry(0.22, 12, 10),
  darkMat,
  [0, 1.5, 1.68],
  [0.8, 0.55, 0.45]
);

const legs = [];

for (const side of [-1, 1]) {
  const ear = wolfPart(
    new THREE.ConeGeometry(0.22, 0.65, 8),
    darkMat,
    [side * 0.42, 2.22, 0.63],
    [1, 1, 1]
  );

  ear.rotation.z = side * -0.22;

  wolfPart(
    new THREE.SphereGeometry(0.09, 12, 8),
    new THREE.MeshStandardMaterial({
      color: 0xff342a,
      emissive: 0xff1200,
      emissiveIntensity: 2
    }),
    [side * 0.43, 1.79, 1.23],
    [1, 1, 1]
  );
}

for (const x of [-0.43, 0.43]) {
  for (const z of [-0.78, 0.78]) {
    const leg = wolfPart(
      new THREE.CylinderGeometry(0.13, 0.16, 0.85, 10),
      darkMat,
      [x, 0.53, z],
      [1, 1, 1]
    );

    legs.push(leg);
  }
}

const tail = wolfPart(
  new THREE.ConeGeometry(0.22, 0.9, 10),
  wolfMat,
  [0, 1.35, -1.38],
  [1, 1, 1]
);

tail.rotation.x = -1.0;

const wolfGlow = new THREE.PointLight(0xff342a, 0.45, 5);
wolfGlow.position.set(0, 1.7, 1.1);
wolf.add(wolfGlow);
scene.add(wolf);

// Game state
const keys = {};

let started = false;
let ended = false;
let collected = 0;
let lastTime = performance.now();
let yaw = 0;
let pitch = -0.12;
let dragging = false;
let lastX = 0;
let lastY = 0;

// Movement settings
const WALK_SPEED = 5.2;
const SPRINT_SPEED = 10.7;
const WOLF_SPEED = 8.65;
const GRAVITY = 20;
const JUMP_POWER = 8.8;

function updateCount() {
  countEl.textContent = `💎 Crystals: ${collected} / 15`;
}

// Positive ending when the wolf catches the player
function finishGame() {
  if (ended) return;

  ended = true;
  started = false;
  overlay.style.display = 'flex';

  title.textContent = 'YOU ARE A LOSER!';
  title.style.color = '#ffe58a';

  panelText.innerHTML =
    'The wolf caught up with you — but that does not make you a loser. ' +
    'You are still a FOREST LEGEND!' +
    '<br><br>Adventure complete. Your courage was brighter than every crystal.';

  startBtn.textContent = 'PLAY AGAIN';
}

// Crystal collection ending
function winGame() {
  if (ended) return;

  ended = true;
  started = false;
  overlay.style.display = 'flex';

  title.textContent = 'FOREST CHAMPION!';
  title.style.color = '#a8ffcb';

  panelText.textContent =
    'You collected all 15 crystals and outsmarted the forest challenge. Incredible exploring!';

  startBtn.textContent = 'PLAY AGAIN';
}

function startGame() {
  if (ended) {
    location.reload();
    return;
  }

  started = true;
  overlay.style.display = 'none';
  lastTime = performance.now();
}

startBtn.addEventListener('click', startGame);

function jump() {
  if (started && !ended && player.onGround) {
    player.vy = JUMP_POWER;
    player.onGround = false;
  }
}

// Keyboard controls
window.addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  keys[k] = true;

  if (k === ' ') {
    e.preventDefault();
    jump();
  }

  if (k === 'e') {
    collectNearby();
  }
});

window.addEventListener('keyup', e => {
  keys[e.key.toLowerCase()] = false;
});

// Touch controls
function bindHold(el, key) {
  el.addEventListener('pointerdown', e => {
    e.preventDefault();
    keys[key] = true;
    el.setPointerCapture(e.pointerId);
  });

  const release = () => {
    keys[key] = false;
  };

  el.addEventListener('pointerup', release);
  el.addEventListener('pointercancel', release);
  el.addEventListener('lostpointercapture', release);
}

document.querySelectorAll('[data-key]').forEach(el => {
  bindHold(el, el.dataset.key);
});

bindHold(document.getElementById('sprintBtn'), 'shift');

document.getElementById('jumpBtn').addEventListener('pointerdown', e => {
  e.preventDefault();
  jump();
});

document.getElementById('collectBtn').addEventListener('pointerdown', e => {
  e.preventDefault();
  collectNearby();
});

// Mouse camera controls
renderer.domElement.addEventListener('pointerdown', e => {
  if (e.pointerType === 'mouse') {
    dragging = true;
    lastX = e.clientX;
    lastY = e.clientY;
  }
});

window.addEventListener('pointerup', () => {
  dragging = false;
});

window.addEventListener('pointermove', e => {
  if (dragging) {
    yaw -= (e.clientX - lastX) * 0.004;

    pitch = Math.max(
      -0.75,
      Math.min(0.35, pitch - (e.clientY - lastY) * 0.003)
    );

    lastX = e.clientX;
    lastY = e.clientY;
  }
});

// Mobile camera controls
let touchLookX = null;

renderer.domElement.addEventListener('touchstart', e => {
  if (e.touches.length === 1) {
    touchLookX = e.touches[0].clientX;
  }
}, { passive: true });

renderer.domElement.addEventListener('touchmove', e => {
  if (e.touches.length === 1 && touchLookX !== null) {
    const nx = e.touches[0].clientX;
    yaw -= (nx - touchLookX) * 0.003;
    touchLookX = nx;
  }
}, { passive: true });

renderer.domElement.addEventListener('touchend', () => {
  touchLookX = null;
});

// Crystal collection
function collectNearby() {
  if (!started || ended) return;

  for (const c of crystals) {
    if (
      c.active &&
      Math.hypot(
        c.group.position.x - player.x,
        c.group.position.z - player.z
      ) < 3.6
    ) {
      c.active = false;
      scene.remove(c.group);

      collected++;
      updateCount();

      if (collected >= 15) {
        winGame();
      }

      break;
    }
  }
}

// Main game loop
function animate(now) {
  requestAnimationFrame(animate);

  const dt = Math.min((now - lastTime) / 1000, 0.045);
  lastTime = now;

  const time = now * 0.001;

  if (started && !ended) {
    const forward =
      (keys['w'] || keys['arrowup'] ? 1 : 0) -
      (keys['s'] || keys['arrowdown'] ? 1 : 0);

    const strafe =
      (keys['d'] || keys['arrowright'] ? 1 : 0) -
      (keys['a'] || keys['arrowleft'] ? 1 : 0);

    const moving = Math.hypot(forward, strafe) > 0;
    const speed = keys['shift'] ? SPRINT_SPEED : WALK_SPEED;

    const fx = -Math.sin(yaw);
    const fz = -Math.cos(yaw);
    const rx = Math.cos(yaw);
    const rz = -Math.sin(yaw);

    let dx = fx * forward + rx * strafe;
    let dz = fz * forward + rz * strafe;

    const len = Math.hypot(dx, dz) || 1;
    dx /= len;
    dz /= len;

    player.x += dx * speed * dt;
    player.z += dz * speed * dt;

    player.x = Math.max(-195, Math.min(195, player.x));
    player.z = Math.max(-195, Math.min(195, player.z));

    if (moving) {
      playerGroup.rotation.y = Math.atan2(dx, dz);
    }

    // Jump physics work while walking or sprinting
    player.vy -= GRAVITY * dt;
    player.y += player.vy * dt;

    if (player.y <= 0) {
      player.y = 0;
      player.vy = 0;
      player.onGround = true;
    }

    playerGroup.position.set(player.x, player.y, player.z);

    // Wolf chases the player
    const wx = player.x - wolf.position.x;
    const wz = player.z - wolf.position.z;
    const dist = Math.hypot(wx, wz);

    if (dist > 0.001) {
      wolf.position.x += (wx / dist) * WOLF_SPEED * dt;
      wolf.position.z += (wz / dist) * WOLF_SPEED * dt;
      wolf.rotation.y = Math.atan2(wx, wz);
    }

    wolf.position.y = Math.abs(Math.sin(time * 8)) * 0.08;

    // Wolf running animation
    for (let i = 0; i < legs.length; i++) {
      legs[i].rotation.x =
        Math.sin(time * 13 + (i % 2) * Math.PI) * 0.32;
    }

    tail.rotation.z = Math.sin(time * 5) * 0.22;

    // Touch detection: the game ends when the wolf reaches the player
    if (dist < 1.75) {
      finishGame();
    }

    if (dist < 9) {
      warningEl.textContent = '⚠ THE WOLF IS RIGHT BEHIND YOU!';
    } else if (dist < 17) {
      warningEl.textContent = 'The wolf is getting closer...';
    } else {
      warningEl.textContent = '';
    }

    // Crystal animation
    for (const c of crystals) {
      if (c.active) {
        c.group.rotation.y += dt * 0.9;
        c.group.position.y =
          1.25 + Math.sin(time * 2 + c.phase) * 0.18;
      }
    }

    if (collected === 15) {
      winGame();
    }
  }

  // Third-person camera
  const target = new THREE.Vector3(
    player.x,
    1.55 + player.y,
    player.z
  );

  const camDist = 8.5;

  const desired = new THREE.Vector3(
    player.x + Math.sin(yaw) * camDist,
    player.y + 3.0 + Math.sin(-pitch) * 2,
    player.z + Math.cos(yaw) * camDist
  );

  camera.position.lerp(desired, 0.12);
  camera.lookAt(target);

  renderer.render(scene, camera);
}

updateCount();
wolf.position.set(-24, 0, -24);

requestAnimationFrame(animate);

// Responsive screen resizing
window.addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
});

})();
</script>
</body>
</html>
"""

components.html(game_html, height=900, scrolling=False)
