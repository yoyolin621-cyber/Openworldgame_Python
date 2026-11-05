
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
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    height: 740px;
    overflow: hidden;
    background: #315b32;
    outline: none;
}

canvas {
    display: block;
}

#overlay, #win-screen {
    position: absolute;
    inset: 0;
    z-index: 10;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    background: rgba(3, 15, 8, 0.9);
    padding: 20px;
}

#win-screen {
    display: none;
    z-index: 15;
    background: rgba(0, 15, 5, 0.94);
}

#overlay h1 {
    color: #9cffae;
    font-size: clamp(30px, 6vw, 58px);
    text-shadow: 0 0 20px #20ff66;
}

#win-screen h1 {
    color: #ffe45c;
    font-size: clamp(45px, 8vw, 80px);
    text-shadow: 0 0 25px gold;
}

#overlay p, #win-screen p {
    line-height: 1.7;
    font-size: 18px;
}

#start, #play-again {
    padding: 16px 35px;
    border: 0;
    border-radius: 12px;
    background: #38dc70;
    color: #08230e;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
}

#hud {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 3;
    color: white;
    font-size: 18px;
    text-shadow: 1px 2px 5px black;
    pointer-events: none;
}

#message {
    position: absolute;
    top: 55px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 3;
    color: white;
    text-shadow: 1px 2px 5px black;
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
    font-size: 25px;
    z-index: 2;
    pointer-events: none;
}

#help {
    position: absolute;
    left: 12px;
    bottom: 12px;
    z-index: 3;
    color: white;
    font-size: 12px;
    text-shadow: 1px 1px 4px black;
    pointer-events: none;
}

#pad {
    position: absolute;
    right: 18px;
    bottom: 18px;
    z-index: 8;
    display: grid;
    grid-template-columns: 58px 58px 58px;
    grid-template-rows: 58px 58px;
    gap: 7px;
    touch-action: none;
}

.move {
    width: 58px;
    height: 58px;
    border: 2px solid white;
    border-radius: 12px;
    background: rgba(10, 35, 25, 0.9);
    color: white;
    font-size: 23px;
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
</style>
</head>

<body>
<div id="game" tabindex="0">

    <div id="hud">
        💎 Crystals: <span id="count">0</span> / 15
    </div>

    <div id="message">
        Explore the forest and find the crystals!
    </div>

    <div id="crosshair">+</div>

    <div id="help">
        WASD: Move | Drag mouse: Look | E: Collect | SHIFT: Sprint
    </div>

    <div id="pad">
        <button class="move" id="up" data-key="KeyW">W</button>
        <button class="move" id="left" data-key="KeyA">A</button>
        <button class="move" id="down" data-key="KeyS">S</button>
        <button class="move" id="right" data-key="KeyD">D</button>
    </div>

    <div id="overlay">
        <h1>WORLD EXPLORER 3D</h1>
        <p>Explore a mysterious forest.</p>
        <p>Collect all 15 glowing crystals!</p>
        <p>But watch out... a wolf is hunting you!</p>
        <button id="start">START EXPLORING</button>
    </div>

    <div id="win-screen">
        <h1>🏆 YOU WIN!</h1>
        <p>You collected all 15 crystals!</p>
        <p>You escaped the wolf and conquered the forest!</p>
        <button id="play-again">PLAY AGAIN</button>
    </div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
const game = document.getElementById("game");
const overlay = document.getElementById("overlay");
const startButton = document.getElementById("start");
const winScreen = document.getElementById("win-screen");
const playAgainButton = document.getElementById("play-again");
const countText = document.getElementById("count");
const message = document.getElementById("message");

// SCENE
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x91b8c5);
scene.fog = new THREE.Fog(0x91b8c5, 35, 120);

// CAMERA
const camera = new THREE.PerspectiveCamera(
    75,
    game.clientWidth / game.clientHeight,
    0.1,
    300
);

camera.position.set(0, 2, 8);

// RENDERER
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(game.clientWidth, game.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
game.insertBefore(renderer.domElement, game.firstChild);

// LIGHTING
scene.add(
    new THREE.HemisphereLight(0xc8eaff, 0x263d20, 1.5)
);

const sunlight = new THREE.DirectionalLight(0xffedc4, 1.5);
sunlight.position.set(25, 45, 15);
sunlight.castShadow = true;
scene.add(sunlight);

// GROUND
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(240, 240),
    new THREE.MeshStandardMaterial({ color: 0x315b32 })
);

ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

// GRASS
const grassMaterial = new THREE.MeshStandardMaterial({
    color: 0x477a39
});

for (let i = 0; i < 350; i++) {
    const patch = new THREE.Mesh(
        new THREE.CircleGeometry(0.25 + Math.random() * 0.5, 6),
        grassMaterial
    );

    patch.rotation.x = -Math.PI / 2;
    patch.position.set(
        (Math.random() - 0.5) * 180,
        0.02,
        (Math.random() - 0.5) * 180
    );

    scene.add(patch);
}

// TREES
const trunkMaterial = new THREE.MeshStandardMaterial({
    color: 0x60402a
});

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

// ROCKS
const rockMaterial = new THREE.MeshStandardMaterial({
    color: 0x777d75
});

for (let i = 0; i < 45; i++) {
    const rock = new THREE.Mesh(
        new THREE.DodecahedronGeometry(
            0.4 + Math.random() * 0.8,
            0
        ),
        rockMaterial
    );

    rock.position.set(
        (Math.random() - 0.5) * 130,
        0.35,
        (Math.random() - 0.5) * 130
    );

    rock.rotation.set(
        Math.random(),
        Math.random(),
        Math.random()
    );

    rock.castShadow = true;
    scene.add(rock);
}

// WOLF MODEL
const wolf = new THREE.Group();

const wolfFur = new THREE.MeshStandardMaterial({
    color: 0x55545a,
    roughness: 0.9
});

const wolfDark = new THREE.MeshStandardMaterial({
    color: 0x29282d
});

const wolfEyes = new THREE.MeshStandardMaterial({
    color: 0xff2222,
    emissive: 0xff0000,
    emissiveIntensity: 1.5
});

// Wolf body
const wolfBody = new THREE.Mesh(
    new THREE.BoxGeometry(1.1, 0.8, 1.7),
    wolfFur
);
wolfBody.position.y = 1;
wolf.add(wolfBody);

// Wolf head
const wolfHead = new THREE.Mesh(
    new THREE.BoxGeometry(0.85, 0.8, 0.8),
    wolfFur
);
wolfHead.position.set(0, 1.35, 1);
wolf.add(wolfHead);

// Wolf snout
const wolfSnout = new THREE.Mesh(
    new THREE.BoxGeometry(0.48, 0.35, 0.65),
    wolfDark
);
wolfSnout.position.set(0, 1.15, 1.55);
wolf.add(wolfSnout);

// Wolf ears
for (const x of [-0.3, 0.3]) {
    const ear = new THREE.Mesh(
        new THREE.ConeGeometry(0.22, 0.65, 5),
        wolfFur
    );

    ear.position.set(x, 1.95, 0.9);
    wolf.add(ear);
}

// Wolf eyes
for (const x of [-0.22, 0.22]) {
    const eye = new THREE.Mesh(
        new THREE.SphereGeometry(0.09, 8, 8),
        wolfEyes
    );

    eye.position.set(x, 1.43, 1.38);
    wolf.add(eye);
}

// Wolf legs
const wolfLegs = [];

for (const x of [-0.35, 0.35]) {
    for (const z of [-0.55, 0.55]) {
        const leg = new THREE.Mesh(
            new THREE.BoxGeometry(0.22, 0.85, 0.25),
            wolfDark
        );

        leg.position.set(x, 0.48, z);
        wolf.add(leg);
        wolfLegs.push(leg);
    }
}

// Wolf tail
const wolfTail = new THREE.Mesh(
    new THREE.ConeGeometry(0.2, 0.9, 6),
    wolfFur
);

wolfTail.position.set(0, 1.2, -1.1);
wolfTail.rotation.x = -1.1;
wolf.add(wolfTail);

wolf.position.set(-18, 0, -18);
scene.add(wolf);

// CRYSTALS
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

// GAME STATE
const keys = {};

let started = false;
let won = false;
let yaw = 0;
let pitch = 0;
let dragging = false;
let lastX = 0;
let lastY = 0;
let collected = 0;

// CAMERA DIRECTION
function updateCamera() {
    camera.rotation.order = "YXZ";
    camera.rotation.y = yaw;
    camera.rotation.x = pitch;
}

// START GAME
function startGame() {
    started = true;
    overlay.style.display = "none";
    camera.position.set(0, 2, 8);
    updateCamera();
    game.focus();
    message.textContent = "Find the crystals. Watch out for the wolf!";
}

startButton.addEventListener("click", startGame);

// KEYBOARD
window.addEventListener("keydown", function(event) {
    keys[event.code] = true;

    if (
        ["KeyW", "KeyA", "KeyS", "KeyD",
         "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.code)
    ) {
        event.preventDefault();
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

// ON-SCREEN WASD BUTTONS
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

// MOUSE CAMERA CONTROL
game.addEventListener("pointerdown", function(event) {
    if (!started || won) return;
    if (event.target.closest("#pad")) return;
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

// COLLECT CRYSTALS
function collectCrystal() {
    if (won) return;

    let nearest = null;
    let nearestDistance = 3;

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

    if (nearest) {
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
                "Crystal collected! Keep exploring!";
        }
    } else {
        message.textContent =
            "Move closer to a crystal first!";
    }
}

// PLAY AGAIN
playAgainButton.addEventListener("click", function() {
    location.reload();
});

// GAME LOOP
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), 0.05);
    const time = clock.elapsedTime;

    // Crystal animation
    crystals.forEach(crystal => {
        if (!crystal.userData.collected) {
            crystal.rotation.y += delta * 1.2;

            crystal.position.y =
                crystal.userData.baseY +
                Math.sin(time * 2 + crystal.position.x) * 0.25;
        }
    });

    if (started && !won) {

        // PLAYER MOVEMENT
        const speed =
            (keys["ShiftLeft"] || keys["ShiftRight"]) ? 10 : 5;

        const forward = new THREE.Vector3(
            -Math.sin(yaw), 0, -Math.cos(yaw)
        );

        const right = new THREE.Vector3(
            Math.cos(yaw), 0, -Math.sin(yaw)
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
            movement.multiplyScalar(speed * delta);
            camera.position.add(movement);
        }

        camera.position.y = 2;

        // WOLF CHASE
        const playerPosition = camera.position.clone();
        playerPosition.y = 0;

        const direction = new THREE.Vector3()
            .subVectors(playerPosition, wolf.position);

        const distance = direction.length();

        if (distance > 1.8) {
            direction.normalize();

            // Wolf follows the player
            wolf.position.addScaledVector(
                direction,
                3.2 * delta
            );

            // Wolf faces the player
            wolf.rotation.y = Math.atan2(
                direction.x,
                direction.z
            );

            // Running animation
            wolf.position.y =
                Math.abs(Math.sin(time * 9)) * 0.12;

            wolfLegs.forEach((leg, index) => {
                leg.rotation.x =
                    Math.sin(time * 10 + index * Math.PI) * 0.35;
            });
        }

        if (distance < 7) {
            message.textContent =
                "🐺 WATCH OUT! THE WOLF IS CHASING YOU!";
        }
    }

    renderer.render(scene, camera);
}

animate();

// RESIZE
window.addEventListener("resize", function() {
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
