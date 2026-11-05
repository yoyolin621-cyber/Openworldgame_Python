
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="World Explorer 3D",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #07120d;
}

#game {
    position: relative;
    width: 100%;
    height: 780px;
    overflow: hidden;
    outline: none;
    background: #172b20;
}

canvas {
    display: block;
}

#overlay, #win-screen {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    background: rgba(2, 12, 7, 0.92);
    padding: 20px;
}

#win-screen {
    display: none;
    background: rgba(0, 15, 5, 0.94);
}

#overlay h1 {
    color: #a6ffb8;
    font-size: clamp(30px, 6vw, 65px);
    text-shadow: 0 0 25px #20ff66;
    margin-bottom: 8px;
}

#win-screen h1 {
    color: #ffe45c;
    font-size: clamp(45px, 8vw, 85px);
    text-shadow: 0 0 30px gold;
}

#overlay p, #win-screen p {
    line-height: 1.7;
    font-size: 17px;
}

.game-button {
    padding: 16px 35px;
    border: 0;
    border-radius: 12px;
    background: #38dc70;
    color: #08230e;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 12px;
}

.game-button:hover {
    background: #9cffae;
}

#hud {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 5;
    color: white;
    font-size: 18px;
    text-shadow: 1px 2px 6px black;
    pointer-events: none;
}

#message {
    position: absolute;
    top: 55px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    color: white;
    text-shadow: 1px 2px 6px black;
    pointer-events: none;
    text-align: center;
    width: 90%;
}

#crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 24px;
    z-index: 4;
    pointer-events: none;
}

#help {
    position: absolute;
    left: 12px;
    bottom: 12px;
    z-index: 5;
    color: white;
    font-size: 12px;
    text-shadow: 1px 1px 5px black;
    pointer-events: none;
}

#pad {
    position: absolute;
    right: 18px;
    bottom: 18px;
    z-index: 10;
    display: grid;
    grid-template-columns: 55px 55px 55px;
    grid-template-rows: 55px 55px;
    gap: 6px;
    touch-action: none;
}

.move {
    width: 55px;
    height: 55px;
    border: 2px solid rgba(255,255,255,.8);
    border-radius: 13px;
    background: rgba(8, 30, 20, .88);
    color: white;
    font-size: 22px;
    font-weight: bold;
    touch-action: none;
    user-select: none;
    -webkit-user-select: none;
}

.move.active {
    background: #38dc70;
    color: #06200c;
}

#up { grid-column: 2; grid-row: 1; }
#left { grid-column: 1; grid-row: 2; }
#down { grid-column: 2; grid-row: 2; }
#right { grid-column: 3; grid-row: 2; }

#jump-button {
    position: absolute;
    right: 28px;
    bottom: 155px;
    z-index: 10;
    width: 75px;
    height: 75px;
    border-radius: 50%;
    border: 3px solid white;
    background: rgba(30, 90, 180, .9);
    color: white;
    font-size: 15px;
    font-weight: bold;
    touch-action: none;
    user-select: none;
}

#jump-button:active {
    background: #54aaff;
}

@media (max-width: 600px) {
    #game {
        height: 720px;
    }

    #help {
        max-width: 48%;
        line-height: 1.5;
    }

    #pad {
        right: 10px;
        bottom: 12px;
    }

    #jump-button {
        right: 15px;
        bottom: 145px;
    }
}
</style>
</head>

<body>

<div id="game" tabindex="0">

    <div id="hud">
        💎 Crystals: <span id="count">0</span> / 15
    </div>

    <div id="message">
        Find the crystals. The wolf is hunting you!
    </div>

    <div id="crosshair">+</div>

    <div id="help">
        WASD: Move<br>
        SPACE: Jump<br>
        SHIFT: Sprint<br>
        E: Collect<br>
        Drag mouse: Look
    </div>

    <div id="pad">
        <button class="move" data-key="KeyW" id="up">W</button>
        <button class="move" data-key="KeyA" id="left">A</button>
        <button class="move" data-key="KeyS" id="down">S</button>
        <button class="move" data-key="KeyD" id="right">D</button>
    </div>

    <button id="jump-button">JUMP</button>

    <div id="overlay">
        <h1>WORLD EXPLORER 3D</h1>
        <p>Explore a mysterious forest.</p>
        <p>Collect all 15 glowing crystals.</p>
        <p>Beware! A fast wolf is hunting you!</p>
        <p>Walk, sprint, jump, and survive.</p>
        <button class="game-button" id="start">
            START EXPLORING
        </button>
    </div>

    <div id="win-screen">
        <h1>🏆 YOU WIN!</h1>
        <p>You collected all 15 crystals!</p>
        <p>You conquered the forest!</p>
        <button class="game-button" id="play-again">
            PLAY AGAIN
        </button>
    </div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
"use strict";

// ========================================
// BASIC GAME SETUP
// ========================================

const game = document.getElementById("game");
const overlay = document.getElementById("overlay");
const winScreen = document.getElementById("win-screen");
const startButton = document.getElementById("start");
const playAgainButton = document.getElementById("play-again");
const countText = document.getElementById("count");
const message = document.getElementById("message");

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x8caeb5);
scene.fog = new THREE.FogExp2(0x8caeb5, 0.006);

// Camera
const camera = new THREE.PerspectiveCamera(
    75,
    game.clientWidth / game.clientHeight,
    0.1,
    350
);

camera.position.set(0, 2, 8);

// Renderer
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
});

renderer.setSize(game.clientWidth, game.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;

game.insertBefore(renderer.domElement, game.firstChild);

// ========================================
// LIGHTING
// ========================================

const hemisphere = new THREE.HemisphereLight(
    0xc9eaff,
    0x26351b,
    1.4
);

scene.add(hemisphere);

const sunlight = new THREE.DirectionalLight(
    0xffe5b0,
    2.0
);

sunlight.position.set(35, 55, 25);
sunlight.castShadow = true;
sunlight.shadow.mapSize.set(2048, 2048);
sunlight.shadow.camera.left = -65;
sunlight.shadow.camera.right = 65;
sunlight.shadow.camera.top = 65;
sunlight.shadow.camera.bottom = -65;
sunlight.shadow.bias = -0.0003;

scene.add(sunlight);

// Soft atmospheric light
const fillLight = new THREE.PointLight(
    0x4b91ad,
    0.8,
    100
);

fillLight.position.set(-15, 12, -15);
scene.add(fillLight);

// ========================================
// GROUND
// ========================================

const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x355b32,
    roughness: 1
});

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(260, 260),
    groundMaterial
);

ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// Grass patches
const grassMaterials = [
    new THREE.MeshStandardMaterial({ color: 0x426d32 }),
    new THREE.MeshStandardMaterial({ color: 0x527a3a }),
    new THREE.MeshStandardMaterial({ color: 0x294f2a })
];

for (let i = 0; i < 650; i++) {
    const material = grassMaterials[
        Math.floor(Math.random() * grassMaterials.length)
    ];

    const patch = new THREE.Mesh(
        new THREE.CircleGeometry(
            0.25 + Math.random() * 0.7,
            7
        ),
        material
    );

    patch.rotation.x = -Math.PI / 2;
    patch.position.set(
        (Math.random() - 0.5) * 220,
        0.025,
        (Math.random() - 0.5) * 220
    );

    scene.add(patch);
}

// ========================================
// FOREST TREES
// ========================================

const trunkMaterial = new THREE.MeshStandardMaterial({
    color: 0x60402d,
    roughness: 1
});

const leafMaterials = [
    new THREE.MeshStandardMaterial({
        color: 0x174927,
        roughness: 1
    }),
    new THREE.MeshStandardMaterial({
        color: 0x245e31,
        roughness: 1
    }),
    new THREE.MeshStandardMaterial({
        color: 0x34723b,
        roughness: 1
    }),
    new THREE.MeshStandardMaterial({
        color: 0x123c25,
        roughness: 1
    })
];

for (let i = 0; i < 125; i++) {
    const x = (Math.random() - 0.5) * 190;
    const z = (Math.random() - 0.5) * 190;

    if (Math.abs(x) < 9 && Math.abs(z) < 9) continue;

    const height = 4 + Math.random() * 5;
    const width = 0.3 + Math.random() * 0.25;

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(
            width * 0.8,
            width * 1.4,
            height,
            9
        ),
        trunkMaterial
    );

    trunk.position.set(x, height / 2, z);
    trunk.castShadow = true;
    trunk.receiveShadow = true;
    scene.add(trunk);

    // Multiple layers of foliage
    for (let layer = 0; layer < 3; layer++) {
        const leaves = new THREE.Mesh(
            new THREE.ConeGeometry(
                2.0 + Math.random() * 0.8,
                3.2,
                8
            ),
            leafMaterials[
                Math.floor(Math.random() * leafMaterials.length)
            ]
        );

        leaves.position.set(
            x,
            height - 0.5 + layer * 1.25,
            z
        );

        leaves.castShadow = true;
        scene.add(leaves);
    }
}

// ========================================
// ROCKS
// ========================================

const rockMaterials = [
    new THREE.MeshStandardMaterial({ color: 0x777b76, roughness: 1 }),
    new THREE.MeshStandardMaterial({ color: 0x555d58, roughness: 1 }),
    new THREE.MeshStandardMaterial({ color: 0x898477, roughness: 1 })
];

for (let i = 0; i < 75; i++) {
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            0.35 + Math.random() * 1.0,
            1
        ),
        rockMaterials[Math.floor(Math.random() * rockMaterials.length)]
    );

    rock.position.set(
        (Math.random() - 0.5) * 170,
        0.35,
        (Math.random() - 0.5) * 170
    );

    rock.rotation.set(
        Math.random(),
        Math.random(),
        Math.random()
    );

    rock.scale.y = 0.5 + Math.random();
    rock.castShadow = true;
    rock.receiveShadow = true;
    scene.add(rock);
}

// ========================================
// GLOWING CRYSTALS
// ========================================

const crystals = [];

const crystalMaterial = new THREE.MeshStandardMaterial({
    color: 0x5beaff,
    emissive: 0x087cbb,
    emissiveIntensity: 2.2,
    metalness: 0.25,
    roughness: 0.12
});

for (let i = 0; i < 15; i++) {
    const crystalGroup = new THREE.Group();

    const crystal = new THREE.Mesh(
        new THREE.OctahedronGeometry(0.7, 0),
        crystalMaterial.clone()
    );

    crystal.castShadow = true;
    crystalGroup.add(crystal);

    // Small glow light
    const glow = new THREE.PointLight(
        0x35dfff,
        1.8,
        7
    );

    glow.position.y = 0.3;
    crystalGroup.add(glow);

    crystalGroup.position.set(
        (Math.random() - 0.5) * 90,
        1.2,
        (Math.random() - 0.5) * 90
    );

    crystalGroup.userData.baseY = 1.2;
    crystalGroup.userData.collected = false;

    scene.add(crystalGroup);
    crystals.push(crystalGroup);
}

// ========================================
// WOLF MODEL
// ========================================

const wolf = new THREE.Group();

const wolfFur = new THREE.MeshStandardMaterial({
    color: 0x4b4b52,
    roughness: 0.85
});

const wolfDark = new THREE.MeshStandardMaterial({
    color: 0x202026,
    roughness: 0.9
});

const wolfEye = new THREE.MeshStandardMaterial({
    color: 0xff1616,
    emissive: 0xff0000,
    emissiveIntensity: 2.5
});

// Body
const wolfBody = new THREE.Mesh(
    new THREE.BoxGeometry(1.2, 0.9, 1.9),
    wolfFur
);

wolfBody.position.y = 1.05;
wolfBody.castShadow = true;
wolf.add(wolfBody);

// Chest
const wolfChest = new THREE.Mesh(
    new THREE.BoxGeometry(0.95, 0.95, 0.65),
    wolfDark
);

wolfChest.position.set(0, 0.95, 0.65);
wolf.add(wolfChest);

// Head
const wolfHead = new THREE.Mesh(
    new THREE.BoxGeometry(0.9, 0.85, 0.85),
    wolfFur
);

wolfHead.position.set(0, 1.55, 1.1);
wolf.add(wolfHead);

// Snout
const wolfSnout = new THREE.Mesh(
    new THREE.BoxGeometry(0.55, 0.35, 0.7),
    wolfDark
);

wolfSnout.position.set(0, 1.32, 1.7);
wolf.add(wolfSnout);

// Ears
for (const x of [-0.32, 0.32]) {
    const ear = new THREE.Mesh(
        new THREE.ConeGeometry(0.23, 0.75, 6),
        wolfDark
    );

    ear.position.set(x, 2.12, 1.05);
    wolf.add(ear);
}

// Eyes
for (const x of [-0.24, 0.24]) {
    const eye = new THREE.Mesh(
        new THREE.SphereGeometry(0.1, 12, 12),
        wolfEye
    );

    eye.position.set(x, 1.62, 1.52);
    wolf.add(eye);
}

// Legs
const wolfLegs = [];

for (const x of [-0.4, 0.4]) {
    for (const z of [-0.65, 0.65]) {
        const leg = new THREE.Mesh(
            new THREE.BoxGeometry(0.25, 0.9, 0.3),
            wolfDark
        );

        leg.position.set(x, 0.48, z);
        leg.castShadow = true;
        wolf.add(leg);
        wolfLegs.push(leg);
    }
}

// Tail
const wolfTail = new THREE.Mesh(
    new THREE.ConeGeometry(0.23, 1.0, 7),
    wolfFur
);

wolfTail.position.set(0, 1.35, -1.25);
wolfTail.rotation.x = -1.1;
wolf.add(wolfTail);

// Wolf starting position
wolf.position.set(-22, 0, -22);
scene.add(wolf);

// ========================================
// GAME STATE
// ========================================

const keys = {};

let started = false;
let won = false;
let collected = 0;

let yaw = 0;
let pitch = 0;

let dragging = false;
let lastX = 0;
let lastY = 0;

let jumpVelocity = 0;
let jumpHeight = 0;
let onGround = true;

const GRAVITY = 19;
const JUMP_POWER = 8.5;

// ========================================
// CAMERA
// ========================================

function updateCamera() {
    camera.rotation.order = "YXZ";
    camera.rotation.y = yaw;
    camera.rotation.x = pitch;
}

// ========================================
// START GAME
// ========================================

function startGame() {
    started = true;
    overlay.style.display = "none";

    camera.position.set(0, 2, 8);
    yaw = 0;
    pitch = 0;

    updateCamera();

    message.textContent = "Find the crystals! The wolf is coming!";
    game.focus();
}

startButton.addEventListener("click", startGame);

// ========================================
// KEYBOARD INPUT
// ========================================

function jump() {
    if (!started || won || !onGround) return;

    jumpVelocity = JUMP_POWER;
    onGround = false;
}

window.addEventListener("keydown", function(event) {
    keys[event.code] = true;

    if (
        ["KeyW", "KeyA", "KeyS", "KeyD",
         "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
         "Space"].includes(event.code)
    ) {
        event.preventDefault();
    }

    if (event.code === "Space" && !event.repeat) {
        jump();
    }

    if (event.code === "KeyE" && started && !won) {
        collectCrystal();
    }
});

window.addEventListener("keyup", function(event) {
    keys[event.code] = false;
});

window.addEventListener("blur", function() {
    for (const key in keys) {
        keys[key] = false;
    }
});

// ========================================
// TOUCH WASD INPUT
// ========================================

document.querySelectorAll(".move").forEach(button => {
    const key = button.dataset.key;

    button.addEventListener("pointerdown", function(event) {
        event.preventDefault();
        event.stopPropagation();

        keys[key] = true;
        button.classList.add("active");

        try {
            button.setPointerCapture(event.pointerId);
        } catch (error) {}
    });

    function release(event) {
        event.preventDefault();
        keys[key] = false;
        button.classList.remove("active");
    }

    button.addEventListener("pointerup", release);
    button.addEventListener("pointercancel", release);

    button.addEventListener("lostpointercapture", function() {
        keys[key] = false;
        button.classList.remove("active");
    });
});

// Touch jump button
const jumpButton = document.getElementById("jump-button");

jumpButton.addEventListener("pointerdown", function(event) {
    event.preventDefault();
    event.stopPropagation();
    jump();

    try {
        jumpButton.setPointerCapture(event.pointerId);
    } catch (error) {}
});

// ========================================
// MOUSE CAMERA CONTROL
// ========================================

game.addEventListener("pointerdown", function(event) {
    if (!started || won) return;
    if (event.target.closest("#pad")) return;
    if (event.target.closest("#jump-button")) return;
    if (event.target.closest("#overlay")) return;

    dragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
});

window.addEventListener("pointerup", function() {
    dragging = false;
});

window.addEventListener("pointermove", function(event) {
    if (!dragging || !started || won) return;

    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;

    lastX = event.clientX;
    lastY = event.clientY;

    yaw -= dx * 0.004;
    pitch -= dy * 0.004;

    pitch = Math.max(-1.35, Math.min(1.35, pitch));

    updateCamera();
});

// ========================================
// COLLECT CRYSTALS
// ========================================

function collectCrystal() {
    if (won) return;

    let nearest = null;
    let nearestDistance = 3.5;

    for (const crystal of crystals) {
        if (crystal.userData.collected) continue;

        const distance = camera.position.distanceTo(
            crystal.position
        );

        if (distance < nearestDistance) {
            nearest = crystal;
            nearestDistance = distance;
        }
    }

    if (!nearest) {
        message.textContent = "Move closer to a crystal!";
        return;
    }

    nearest.userData.collected = true;
    scene.remove(nearest);

    collected++;
    countText.textContent = collected;

    if (collected === 15) {
        won = true;
        started = false;
        winScreen.style.display = "flex";
        message.textContent = "YOU WON!";
    } else {
        message.textContent =
            "Crystal collected! " + (15 - collected) + " left!";
    }
}

// ========================================
// PLAY AGAIN
// ========================================

playAgainButton.addEventListener("click", function() {
    location.reload();
});

// ========================================
// ANIMATION LOOP
// ========================================

const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.05);
    const time = clock.elapsedTime;

    // Crystal animation
    crystals.forEach(crystal => {
        if (!crystal.userData.collected) {
            crystal.rotation.y += delta * 1.4;

            crystal.position.y =
                crystal.userData.baseY +
                Math.sin(time * 2.5 + crystal.position.x) * 0.3;
        }
    });

    if (started && !won) {

        // --------------------------------
        // PLAYER MOVEMENT
        // --------------------------------

        const sprinting =
            keys["ShiftLeft"] || keys["ShiftRight"];

        const playerSpeed = sprinting ? 10.5 : 5;

        const forward = new THREE.Vector3(
            -Math.sin(yaw),
            0,
            -Math.cos(yaw)
        );

        const right = new THREE.Vector3(
            Math.cos(yaw),
            0,
            -Math.sin(yaw)
        );

        const movement = new THREE.Vector3();

        if (keys["KeyW"] || keys["ArrowUp"]) {
            movement.add(forward);
        }

        if (keys["KeyS"] || keys["ArrowDown"]) {
            movement.sub(forward);
        }

        if (keys["KeyD"] || keys["ArrowRight"]) {
            movement.add(right);
        }

        if (keys["KeyA"] || keys["ArrowLeft"]) {
            movement.sub(right);
        }

        if (movement.lengthSq() > 0) {
            movement.normalize();
            movement.multiplyScalar(playerSpeed * delta);
            camera.position.add(movement);
        }

        // --------------------------------
        // JUMP PHYSICS
        // --------------------------------

        if (!onGround) {
            jumpVelocity -= GRAVITY * delta;
            jumpHeight += jumpVelocity * delta;

            if (jumpHeight <= 0) {
                jumpHeight = 0;
                jumpVelocity = 0;
                onGround = true;
            }
        }

        camera.position.y = 2 + jumpHeight;

        // --------------------------------
        // FASTER WOLF CHASE
        // --------------------------------

        const playerPosition = camera.position.clone();
        playerPosition.y = 0;

        const direction = new THREE.Vector3()
            .subVectors(playerPosition, wolf.position);

        const distance = direction.length();

        if (distance > 1.8) {
            direction.normalize();

            // Wolf speed: faster than normal walking
            const wolfSpeed = 7.5;

            wolf.position.addScaledVector(
                direction,
                wolfSpeed * delta
            );

            wolf.rotation.y = Math.atan2(
                direction.x,
                direction.z
            );

            // Running animation
            wolf.position.y =
                Math.abs(Math.sin(time * 12)) * 0.16;

            wolfLegs.forEach((leg, index) => {
                leg.rotation.x =
                    Math.sin(time * 13 + index * Math.PI) * 0.5;
            });

            wolfTail.rotation.z =
                Math.sin(time * 5) * 0.15;
        }

        // Wolf warning
        if (distance < 7) {
            message.textContent =
                "🐺 THE WOLF IS RIGHT BEHIND YOU! RUN!";
        } else if (distance < 15) {
            message.textContent =
                "🐺 The wolf is getting closer!";
        }
    }

    renderer.render(scene, camera);
}

animate();

// ========================================
// RESIZE
// ========================================

window.addEventListener("resize", function() {
    const width = game.clientWidth;
    const height = game.clientHeight;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

</script>
</body>
</html>
"""

components.html(game_html, height=800, scrolling=False)
