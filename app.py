
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="World Explorer 3D", layout="wide")

st.markdown("""
<style>
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    header, footer, #MainMenu {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #07130d;
}
#game {
    position: relative;
    width: 100%;
    height: 740px;
    overflow: hidden;
    background: #142b1b;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#overlay {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: white;
    text-align: center;
    background: linear-gradient(#07130dbb, #07130ddd);
}
#overlay h1 {
    font-size: clamp(30px, 6vw, 58px);
    margin: 10px;
    color: #aaffbd;
    text-shadow: 0 0 20px #36ff75;
}
#overlay p {
    font-size: 16px;
    line-height: 1.7;
    padding: 0 15px;
}
#start {
    border: 0;
    border-radius: 12px;
    padding: 17px 38px;
    margin-top: 20px;
    background: #39d66c;
    color: #06210d;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
}
#start:hover { background: #8affaa; }
#hud {
    position: absolute;
    top: 15px;
    left: 15px;
    color: white;
    font-size: 17px;
    text-shadow: 1px 2px 4px black;
    z-index: 2;
    pointer-events: none;
}
#message {
    position: absolute;
    top: 65px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 17px;
    text-shadow: 1px 2px 4px black;
    z-index: 2;
    pointer-events: none;
}
#crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 24px;
    text-shadow: 0 0 5px black;
    pointer-events: none;
}
#pad {
    position: absolute;
    right: 18px;
    bottom: 18px;
    z-index: 4;
    display: grid;
    grid-template-columns: 58px 58px 58px;
    grid-template-rows: 58px 58px;
    gap: 7px;
    touch-action: none;
}
.move {
    border: 2px solid #ffffff99;
    border-radius: 12px;
    background: #10251dcc;
    color: white;
    font-size: 23px;
    font-weight: bold;
    cursor: pointer;
    touch-action: none;
    user-select: none;
}
.move:active { background: #39d66c; color: #07130d; }
#up { grid-column: 2; grid-row: 1; }
#left { grid-column: 1; grid-row: 2; }
#down { grid-column: 2; grid-row: 2; }
#right { grid-column: 3; grid-row: 2; }
#help {
    position: absolute;
    left: 15px;
    bottom: 15px;
    color: white;
    font-size: 12px;
    text-shadow: 1px 1px 3px black;
    z-index: 2;
    pointer-events: none;
}
</style>
</head>
<body>
<div id="game">
    <div id="hud">💎 Crystals: <span id="count">0</span> / 15</div>
    <div id="message">Explore the forest and find the crystals!</div>
    <div id="crosshair">+</div>
    <div id="help">WASD / buttons: Move · Drag mouse: Look · E: Collect</div>

    <div id="pad">
        <button class="move" id="up" data-key="KeyW">W</button>
        <button class="move" id="left" data-key="KeyA">A</button>
        <button class="move" id="down" data-key="KeyS">S</button>
        <button class="move" id="right" data-key="KeyD">D</button>
    </div>

    <div id="overlay">
        <h1>WORLD EXPLORER 3D</h1>
        <p>Explore a mysterious forest.<br>
        Find all 15 glowing crystals!</p>
        <p>WASD to move · Drag to look around · E to collect</p>
        <button id="start">START EXPLORING</button>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const game = document.getElementById("game");
const overlay = document.getElementById("overlay");
const startButton = document.getElementById("start");
const countText = document.getElementById("count");
const message = document.getElementById("message");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91b8c5);
scene.fog = new THREE.Fog(0x91b8c5, 35, 115);

const camera = new THREE.PerspectiveCamera(
    75, game.clientWidth / game.clientHeight, 0.1, 300
);
camera.position.set(0, 2, 8);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(game.clientWidth, game.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
game.insertBefore(renderer.domElement, game.firstChild);

scene.add(new THREE.HemisphereLight(0xc8eaff, 0x263d20, 1.5));

const sunlight = new THREE.DirectionalLight(0xffedc4, 1.4);
sunlight.position.set(25, 45, 15);
sunlight.castShadow = true;
scene.add(sunlight);

// Forest floor
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(240, 240),
    new THREE.MeshStandardMaterial({ color: 0x315b32 })
);
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Small patches of grass
const grassMaterial = new THREE.MeshStandardMaterial({ color: 0x477a39 });
for (let i = 0; i < 350; i++) {
    const patch = new THREE.Mesh(
        new THREE.CircleGeometry(0.25 + Math.random() * 0.5, 6),
        grassMaterial
    );
    patch.rotation.x = -Math.PI / 2;
    patch.position.set(
        (Math.random() - 0.5) * 180,
        0.015,
        (Math.random() - 0.5) * 180
    );
    scene.add(patch);
}

// Trees
const trunkMaterial = new THREE.MeshStandardMaterial({ color: 0x60402a });
const leafMaterials = [
    new THREE.MeshStandardMaterial({ color: 0x174d27 }),
    new THREE.MeshStandardMaterial({ color: 0x236333 }),
    new THREE.MeshStandardMaterial({ color: 0x315f2c })
];

for (let i = 0; i < 95; i++) {
    const x = (Math.random() - 0.5) * 150;
    const z = (Math.random() - 0.5) * 150;

    if (Math.abs(x) < 7 && Math.abs(z) < 7) continue;

    const height = 3 + Math.random() * 3;

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.25, 0.38, height, 7),
        trunkMaterial
    );
    trunk.position.set(x, height / 2, z);
    trunk.castShadow = true;
    scene.add(trunk);

    const leaves = new THREE.Mesh(
        new THREE.ConeGeometry(1.7 + Math.random(), 3.5, 7),
        leafMaterials[Math.floor(Math.random() * leafMaterials.length)]
    );
    leaves.position.set(x, height + 1.1, z);
    leaves.castShadow = true;
    scene.add(leaves);
}

// Rocks
const rockMaterial = new THREE.MeshStandardMaterial({ color: 0x777d75 });
for (let i = 0; i < 45; i++) {
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(0.4 + Math.random() * 0.8, 0),
        rockMaterial
    );
    rock.position.set(
        (Math.random() - 0.5) * 130,
        0.35,
        (Math.random() - 0.5) * 130
    );
    rock.rotation.set(Math.random(), Math.random(), Math.random());
    rock.castShadow = true;
    scene.add(rock);
}

// Collectible crystals
const crystals = [];
const crystalMaterial = new THREE.MeshStandardMaterial({
    color: 0x48eaff,
    emissive: 0x087cbb,
    emissiveIntensity: 1.8,
    metalness: 0.2,
    roughness: 0.15
});

for (let i = 0; i < 15; i++) {
    const crystal = new THREE.Mesh(
        new THREE.OctahedronGeometry(0.65),
        crystalMaterial.clone()
    );

    crystal.position.set(
        (Math.random() - 0.5) * 90,
        1.1,
        (Math.random() - 0.5) * 90
    );
    crystal.userData.baseY = crystal.position.y;
    crystal.userData.collected = false;
    crystal.castShadow = true;
    scene.add(crystal);
    crystals.push(crystal);
}

// Player and controls
const keys = {};
let started = false;
let yaw = 0;
let pitch = 0;
let dragging = false;
let lastX = 0;
let lastY = 0;
let collected = 0;

function updateCameraDirection() {
    camera.rotation.order = "YXZ";
    camera.rotation.y = yaw;
    camera.rotation.x = pitch;
}

function startGame() {
    started = true;
    overlay.style.display = "none";
    camera.position.set(0, 2, 8);
    updateCameraDirection();
    message.textContent = "Find the glowing crystals!";
}

startButton.addEventListener("click", startGame);

// Keyboard movement
window.addEventListener("keydown", (event) => {
    keys[event.code] = true;
    if (event.code === "KeyE" && started) collectCrystal();
});
window.addEventListener("keyup", (event) => {
    keys[event.code] = false;
});
window.addEventListener("blur", () => {
    for (const key in keys) keys[key] = false;
});

// Bottom-right touch and mouse movement buttons
document.querySelectorAll(".move").forEach(button => {
    const key = button.dataset.key;

    button.addEventListener("pointerdown", event => {
        event.preventDefault();
        keys[key] = true;
        button.setPointerCapture(event.pointerId);
    });

    function releaseKey(event) {
        event.preventDefault();
        keys[key] = false;
    }

    button.addEventListener("pointerup", releaseKey);
    button.addEventListener("pointercancel", releaseKey);
    button.addEventListener("lostpointercapture", () => {
        keys[key] = false;
    });
});

// Drag to look around
game.addEventListener("pointerdown", event => {
    if (!started || event.target.closest("#pad") || event.target.closest("#overlay")) return;
    dragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
});

window.addEventListener("pointerup", () => {
    dragging = false;
});

window.addEventListener("pointermove", event => {
    if (!dragging || !started) return;

    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    lastX = event.clientX;
    lastY = event.clientY;

    yaw -= dx * 0.004;
    pitch -= dy * 0.004;
    pitch = Math.max(-1.35, Math.min(1.35, pitch));
    updateCameraDirection();
});

// Collect a nearby crystal
function collectCrystal() {
    let nearest = null;
    let nearestDistance = 3;

    for (const crystal of crystals) {
        if (crystal.userData.collected) continue;

        const distance = camera.position.distanceTo(crystal.position);
        if (distance < nearestDistance) {
            nearest = crystal;
            nearestDistance = distance;
        }
    }

    if (nearest) {
        nearest.userData.collected = true;
        scene.remove(nearest);
        collected++;
        countText.textContent = collected;

        if (collected === 15) {
            message.textContent = "Amazing! You found all 15 crystals!";
        } else {
            message.textContent = "Crystal collected! Keep exploring!";
        }
    } else {
        message.textContent = "Move closer to a crystal first!";
    }
}

// Main game loop
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const time = clock.getElapsedTime();
    const delta = Math.min(clock.getDelta(), 0.05);

    crystals.forEach(crystal => {
        if (!crystal.userData.collected) {
            crystal.rotation.y += delta * 1.2;
            crystal.position.y =
                crystal.userData.baseY + Math.sin(time * 2 + crystal.position.x) * 0.25;
        }
    });

    if (started) {
        const speed = keys["ShiftLeft"] || keys["ShiftRight"] ? 10 : 5;
        const forward = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw));
        const right = new THREE.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));

        const movement = new THREE.Vector3();

        if (keys["KeyW"]) movement.add(forward);
        if (keys["KeyS"]) movement.sub(forward);
        if (keys["KeyD"]) movement.add(right);
        if (keys["KeyA"]) movement.sub(right);

        if (movement.lengthSq() > 0) {
            movement.normalize().multiplyScalar(speed * delta);
            camera.position.add(movement);
        }

        camera.position.y = 2;
    }

    renderer.render(scene, camera);
}

animate();

window.addEventListener("resize", () => {
    const width = game.clientWidth;
    const height = game.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});
</script>
</body>
</html>
"""

components.html(game_html, height=760, scrolling=False)
