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

st.set_page_config(
    page_title="World Explorer 3D",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Streamlit styling
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

# Game HTML, CSS and JavaScript
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
