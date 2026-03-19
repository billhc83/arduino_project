import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.block_builder_launcher import block_builder_launcher
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY  — edit these 4 lines for every new project
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project Fourteen Part 2: Code Cracker"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/code_cracker.png"            # top banner         # used in both tabs
ARDUINO_PRESET   = "codebreaker"      
# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

<h2>🕵️ Spy Training: Code Breaker System</h2>

<p>
Welcome, Agent.
</p>

<p>
You are building a <b>Code Breaker</b> for future trainees.
</p>

<p>
Your system will challenge them to find a hidden 5-letter word.
</p>

<p>
Every step you complete adds a new ability to your machine.
</p>

<hr>

<h3>🧠 How the System Works</h3>

<p>
Every Code Breaker follows the same process:
</p>

<p>⌨️ <b>INPUT</b> → The trainee types a guess</p>
<p>📓 <b>STORE</b> → The program remembers the guess</p>
<p>🔍 <b>CHECK</b> → The program compares it to the answer</p>
<p>💻 <b>OUTPUT</b> → The result is shown on the screen</p>
<p>🏁 <b>RESULT</b> → The system checks if the code is cracked</p>

<hr>

<h3>🔁 The Flow of Your Program</h3>

<p>
Your program will always follow this loop:
</p>

<p>
⏳ WAIT → 📡 READ → 📓 STORE → 🔍 CHECK → 💬 RESPOND
</p>

<p>
Right now, your system is incomplete…
but each step you build brings it closer to life.
</p>

<hr>

<h3>🧩 The Pieces You Will Build</h3>

<p>📦 <b>Variables</b> → store important information</p>
<p>📡 <b>Input</b> → read what the user types</p>
<p>🧠 <b>Logic</b> → compare and make decisions</p>
<p>💬 <b>Output</b> → send messages to the screen</p>
<p>🚪 <b>Conditions</b> → control what happens next</p>

<hr>

<h3>🎯 Your Mission</h3>

<p>
Build a complete system that can:
</p>

<p>✔ read a guess</p>
<p>✔ check how close it is</p>
<p>✔ display the result</p>
<p>✔ detect when the code is cracked</p>

<p>
Stay sharp, Agent… 🕶️
</p>
"""

# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)


from components.block_builder_launcher import block_builder_launcher

block_builder_launcher(
    preset=ARDUINO_PRESET,
    username=st.session_state.get('username'),
    page='lesson_3'
)

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1, 3])
with buttoncol1:
    if st.button("Next Step", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to continue to the next step!")
