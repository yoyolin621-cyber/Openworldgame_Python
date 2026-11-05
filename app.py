
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="World Explorer 3D",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
header, footer, #MainMenu {
    visibility: hidden;
}
.stApp {
    background: #08111b;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #07121c;
}

canvas {
    display: block;
}

#hud {
    position: absolute;
    top: 20px;
    left: 20px;
    color: white;
    z-index: 10;
    pointer-events: none;
}

.panel {
    background: rgba(5, 15, 25, 0.75);
    backdrop-filter: blur(12px);
    padding: 15px 22px;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    margin-bottom: 10px;
}

#hud h2 {
    color: #7cecff;
    font-size: 20px;
    letter-spacing: 2px;
}

#hud p {
    font-size: 13px;
    margin-top: 8px;
    color: #c8d9e8;
}

#counter {
    font-size: 19px;
    color: #ffd66b;
    font-weight: bold;
}

#center {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(3, 10, 20, 0.72);
    z-index: 20;
    color: white;
    text-align: center;
    pointer-events: auto;
}

#startbox {
    padding: 35px;
    max-width: 450px;
    background: rgba(12, 29, 45, 0.92);
    border: 1px solid #3a849e;
    border-radius: 20px;
    box-shadow: 0 0 50px rgba(0, 200, 255, 0.15);
    position: relative;
    z-index: 30;
}

#startbox h1 {
    color: #71eaff;
    font-size: 36px;
    margin-bottom: 15px;
}

#startbox p {
    line-height: 1.8;
    color: #c4d8e7;
    margin-bottom: 22px;
}

button {
    padding: 14px 30px;
    border: none;
    border-radius: 30px;
    background: linear-gradient(120deg, #05b9db, #547bff);
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
}

button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 20px #05b9db;
}

#start {
    position: relative;
    z-index: 31;
    pointer-events: auto;
}

#crosshair {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 8px;
    height: 8px;
    border: 2px solid white;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    opacity: 0.8;
}

#message {
    position: absolute;
    bottom: 75px;
    left: 50%;
    transform: translateX(-50%);
    color: #fff;
    background: rgba(0,0,0,0.7);
    padding: 12px 22px;
    border-radius: 10px;
    display: none;
    pointer-events: none;
}

#help {
    position: absolute;
    bottom: 15px;
    left: 20px;
    color: white;
    background: rgba(5,15,25,0.75);
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 12px;
    line-height: 1.8;
    pointer-events: none;
}

#weather {
    position: absolute;
    top: 20px;
    right: 20px;
    color: #fff;
    background: rgba(5,15,25,0.75);
    padding: 15px 20px;
    border-radius: 12px;
    font-size: 13px;
    pointer-events: none;
}
</style>
</head>

<body>

<div id="hud">
    <div class="panel">
        <h2>🌍 WORLD EXPLORER</h2>
        <p>Discover the unknown world</p>
    </div>

    <div class="panel">
        <p>✨ CRYSTALS COLLECTED</p>
        <div id="counter">0 / 15</div>
    </div>
</div>

<div id="weather">
    ☀️ SUNNY DAY<br>
    🌲 FOREST REGION
</div>

<div id="crosshair"></div>

<div id="help">
    <b>CONTROLS</b><br>
    W A S D - Move<br>
    MOUSE DRAG - Look around<br>
    SHIFT - Run<br>
    E - Collect crystals<br>
    ESC - Pause
</div>

<div id="message"></div>

<div id="center">
    <div id="startbox">
        <h1>WORLD EXPLORER</h1>
        <p>
            Welcome to a mysterious 3D world.<br>
            Explore forests, discover hidden crystals,
            and uncover the secrets of the landscape.
        </p>
        <p>
            WASD to move · Mouse to look<br>
            SHIFT to run · E to collect
        </p>
        <button id="start">START EXPLORING</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>

// --------------------------------
// SCENE SETUP
// --------------------------------

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x8bc9e8);
scene.fog = new THREE.Fog(0x8bc9e8, 40, 180);

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    500
);

camera.position.set(0, 4, 0);

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

document.body.appendChild(renderer.domElement);

// --------------------------------
// LIGHTING
// --------------------------------

const ambient = new THREE.HemisphereLight(
    0xc5e8ff,
    0x304a25,
    1.5
);

scene.add(ambient);

const sun = new THREE.DirectionalLight(0xfff0ce, 2);

sun.position.set(40, 70, 30);
sun.castShadow = true;

scene.add(sun);

// --------------------------------
// TERRAIN
// --------------------------------

function terrainHeight(x, z) {
    return (
        Math.sin(x * 0.045) * 3 +
        Math.cos(z * 0.055) * 3 +
        Math.sin((x + z) * 0.025) * 5 +
        Math.cos(x * 0.11) * Math.sin(z * 0.1) * 1.5
    );
}

const groundGeometry = new THREE.PlaneGeometry(
    240, 240, 120, 120
);

groundGeometry.rotateX(-Math.PI / 2);

const positions = groundGeometry.attributes.position;

for (let i = 0; i < positions.count; i++) {
    const x = positions.getX(i);
    const z = positions.getZ(i);

    positions.setY(i, terrainHeight(x, z));
}

groundGeometry.computeVertexNormals();

const ground = new THREE.Mesh(
    groundGeometry,
    new THREE.MeshStandardMaterial({
        color: 0x527b45,
        roughness: 1
    })
);

ground.receiveShadow = true;
scene.add(ground);

// --------------------------------
// TREES
// --------------------------------

const treeGroup = new THREE.Group();
scene.add(treeGroup);

function createTree(x, z) {

    const y = terrainHeight(x, z);

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.25, 0.4, 3, 8),
        new THREE.MeshStandardMaterial({
            color: 0x68432b
        })
    );

    trunk.position.set(x, y + 1.5, z);
    trunk.castShadow = true;

    treeGroup.add(trunk);

    const leaves = new THREE.Mesh(
        new THREE.ConeGeometry(2.1, 5, 8),
        new THREE.MeshStandardMaterial({
            color: Math.random() > 0.5
                ? 0x216b42
                : 0x34844c
        })
    );

    leaves.position.set(x, y + 4.6, z);
    leaves.castShadow = true;

    treeGroup.add(leaves);
}

for (let i = 0; i < 180; i++) {

    let x = (Math.random() - 0.5) * 210;
    let z = (Math.random() - 0.5) * 210;

    if (Math.sqrt(x*x + z*z) < 12) continue;

    createTree(x, z);
}

// --------------------------------
// ROCKS
// --------------------------------

for (let i = 0; i < 80; i++) {

    const x = (Math.random() - 0.5) * 200;
    const z = (Math.random() - 0.5) * 200;

    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            0.5 + Math.random() * 1.2
        ),
        new THREE.MeshStandardMaterial({
            color: 0x777f83,
            roughness: 1
        })
    );

    rock.position.set(
        x,
        terrainHeight(x,z) + 0.5,
        z
    );

    rock.rotation.set(
        Math.random(),
        Math.random(),
        Math.random()
    );

    rock.castShadow = true;
    scene.add(rock);
}

// --------------------------------
// CRYSTALS
// --------------------------------

const crystals = [];

const crystalGeometry = new THREE.OctahedronGeometry(0.8);

const crystalMaterial = new THREE.MeshStandardMaterial({
    color: 0x00eaff,
    emissive: 0x0088ff,
    emissiveIntensity: 2,
    metalness: 0.3,
    roughness: 0.2
});

for (let i = 0; i < 15; i++) {

    const crystal = new THREE.Mesh(
        crystalGeometry,
        crystalMaterial.clone()
    );

    const x = (Math.random() - 0.5) * 175;
    const z = (Math.random() - 0.5) * 175;

    crystal.position.set(
        x,
        terrainHeight(x,z) + 2,
        z
    );

    crystal.userData.collected = false;

    crystal.castShadow = true;
    scene.add(crystal);

    const glow = new THREE.PointLight(
        0x00cfff,
        2,
        9
    );

    crystal.add(glow);

    crystals.push(crystal);
}

// --------------------------------
// CONTROLS
// --------------------------------

const startButton = document.getElementById("start");
const center = document.getElementById("center");

let gameStarted = false;
let yaw = 0;
let pitch = 0;
let dragging = false;
let lastMouseX = 0;
let lastMouseY = 0;

// Start without requiring pointer lock.

startButton.addEventListener("click", () => {
    gameStarted = true;
    center.style.display = "none";
    startButton.innerText = "RESUME EXPLORING";
});

// Mouse drag to look around.

document.addEventListener("mousedown", (e) => {
    if (!gameStarted) return;

    dragging = true;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
});

document.addEventListener("mouseup", () => {
    dragging = false;
});

document.addEventListener("mousemove", (e) => {

    if (!gameStarted || !dragging) return;

    const dx = e.clientX - lastMouseX;
    const dy = e.clientY - lastMouseY;

    lastMouseX = e.clientX;
    lastMouseY = e.clientY;

    yaw -= dx * 0.004;
    pitch -= dy * 0.003;

    pitch = THREE.MathUtils.clamp(
        pitch,
        -1.2,
        1.2
    );

    camera.rotation.order = "YXZ";
    camera.rotation.y = yaw;
    camera.rotation.x = pitch;
});

const keys = {};

document.addEventListener("keydown", e => {

    keys[e.code] = true;

    if (e.code === "Escape" && gameStarted) {

        gameStarted = false;
        center.style.display = "flex";
        startButton.innerText = "RESUME EXPLORING";
        dragging = false;
    }
});

document.addEventListener("keyup", e => {
    keys[e.code] = false;
});

// --------------------------------
// COLLECTION SYSTEM
// --------------------------------

let collected = 0;

const counter = document.getElementById("counter");
const message = document.getElementById("message");

function showMessage(text) {

    message.innerText = text;
    message.style.display = "block";

    setTimeout(() => {
        message.style.display = "none";
    }, 2200);
}

function collectCrystal() {

    let nearest = null;
    let nearestDistance = 5;

    crystals.forEach(crystal => {

        if (crystal.userData.collected) return;

        const distance = camera.position.distanceTo(
            crystal.position
        );

        if (distance < nearestDistance) {
            nearest = crystal;
            nearestDistance = distance;
        }
    });

    if (nearest) {

        nearest.userData.collected = true;
        scene.remove(nearest);

        collected++;

        counter.innerText = collected + " / 15";

        showMessage("✨ Crystal collected!");

        if (collected === 15) {
            showMessage("🏆 AMAZING! YOU FOUND ALL CRYSTALS!");
        }

    } else {
        showMessage("No crystal nearby. Keep exploring!");
    }
}

document.addEventListener("keydown", e => {

    if (e.code === "KeyE" && gameStarted) {
        collectCrystal();
    }
});

// --------------------------------
// MOVEMENT AND ANIMATION
// --------------------------------

const clock = new THREE.Clock();

const WORLD_LIMIT = 112;

function animate() {

    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.05);
    const time = clock.elapsedTime;

    // Crystal animation

    crystals.forEach((crystal, i) => {

        if (!crystal.userData.collected) {

            crystal.rotation.y += delta;

            crystal.position.y +=
                Math.sin(time * 2 + i) * 0.003;
        }
    });

    // Player movement

    if (gameStarted) {

        const speed = keys["ShiftLeft"] ||
                      keys["ShiftRight"] ? 18 : 9;

        let forward = 0;
        let sideways = 0;

        if (keys["KeyW"]) forward += 1;
        if (keys["KeyS"]) forward -= 1;
        if (keys["KeyA"]) sideways -= 1;
        if (keys["KeyD"]) sideways += 1;

        const length = Math.sqrt(
            forward * forward +
            sideways * sideways
        );

        if (length > 0) {
            forward /= length;
            sideways /= length;
        }

        // Move relative to camera direction.

        const moveX =
            Math.sin(yaw) * forward +
            Math.cos(yaw) * sideways;

        const moveZ =
            -Math.cos(yaw) * forward +
            Math.sin(yaw) * sideways;

        camera.position.x += moveX * speed * delta;
        camera.position.z += moveZ * speed * delta;

        // World boundaries.

        camera.position.x = THREE.MathUtils.clamp(
            camera.position.x,
            -WORLD_LIMIT,
            WORLD_LIMIT
        );

        camera.position.z = THREE.MathUtils.clamp(
            camera.position.z,
            -WORLD_LIMIT,
            WORLD_LIMIT
        );

        // Follow terrain elevation.

        const groundY = terrainHeight(
            camera.position.x,
            camera.position.z
        );

        camera.position.y = groundY + 2.2;
    }

    renderer.render(scene, camera);
}

animate();

// --------------------------------
// RESPONSIVE SCREEN
// --------------------------------

window.addEventListener("resize", () => {

    camera.aspect =
        window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
});

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=760,
    scrolling=False
)
