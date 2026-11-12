1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
 
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
      Explore a detailed forest and collect all 15 glowing crystals.
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
