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

PAGE_TITLE       = "Project Fourteen Part 1: Code Cracker"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/code_cracker.png"            # top banner         # used in both tabs
ARDUINO_PRESET   = "cb_step1"                         # matches arduino_block_coder preset key

# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🕵️ Project: Code Cracker

Welcome to the Agent Training Program.

During spy training, recruits must prove they can solve problems, think logically, and understand secret communication systems.

Your first test is called The Code Breaker Challenge.

A computer system has locked a message behind a five-letter password.
Your job is to build a program that can help crack the code.

Each time someone enters a guess, the computer will compare it to the real password and report how many letters match.

When all five letters match…

the system will unlock the hidden message.

🔐 What Happens Next?

Inside the system is a message left by the training engineers.

But no one knows what it says yet.

The only way to read it is to build the code-cracking machine and discover the password.

Once the system unlocks, the message will appear in the mission terminal.

Your training instructions will be revealed.

</div>
"""


# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)
from components.code_breaker import serial_monitor
serial_monitor(
    answer = 'SPARE',
    cipher_lines= [
    'STSTARERT',
    'PLSHAREMN',
    'BNSHARKOP',
    'QWSPARETY',
    'ZXSPARKCV',
    'MKSNAREPL',
    'HGSHAKEUI',
    'LKDJSFPOIE',
    'MNBVCXZAQS',
    'POIUYTREWQ'],
    message = [
"CODE CRACKED",
"",
"GOOD WORK AGENT.",
"",
"YOU HAVE SUCCESSFULLY COMPLETED",
"THE FIRST TRAINING EXERCISE.",
"",
"THIS SYSTEM WAS BUILT TO TEST",
"YOUR ABILITY TO ANALYZE",
"AND BREAK SECRET CODES.",
"",
"BUT EVERY TRAINING PROGRAM",
"NEEDS NEW CHALLENGES.",
"",
"YOUR NEXT MISSION:",
"BUILD A NEW CODE BREAKING TRAINING SYSTEM",
"FOR THE NEXT GROUP OF TRAINEES.",
"",
"TRAINING COMMAND OUT."
]) # type: ignore



pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1, 3])
with buttoncol1:
    if st.button("Next Step", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to continue the mission!")
