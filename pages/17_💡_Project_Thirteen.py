import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line, label

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY  — edit these 4 lines for every new project
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project Thirteen: Your Title Here"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/your_banner.png"            # top banner
CIRCUIT_IMAGE    = "graphics/your_circuit.png"           # used in both tabs
ARDUINO_PRESET   = "your_preset"                         # matches arduino_block_coder preset key
ARDUINO_PIN_REFS = "your_preset"                         # usually same as preset

# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🚀 Welcome to [Your Project Name]

Write your intro narrative here.

---

## 🎯 Your Mission

Describe the parts and the rules here.

</div>
"""

# ════════════════════════════════════════════════════════════
#  ASSEMBLY STEPS  — one build_step() call per physical step
#
#  Shapes:
#    rect(x1, y1, x2, y2)          — rectangle highlight
#    circle(cx, cy, radius=60)     — circle highlight
#    line((x,y), (x,y), ...)       — polyline / wire trace
#
#  Labels (optional keyword arg):
#    labels=[label("Long Leg", offset_x=100), label("Short Leg", offset_x=-100)]
#
#  Full example:
#    build_step(
#        "Place the long leg of the LED in row 18, column E.<br>"
#        "Place the short leg in row 17, column E.",
#        "Make sure your lights are in the right order.",
#        rect(876, 175, 971, 344),
#        labels=[label("Long Leg", offset_x=100), label("Short Leg", offset_x=-100)]
#    )
# ════════════════════════════════════════════════════════════

STEPS = [
    intro_step(
        "Your Intro Title Here!",
        "Press the next button for a step-by-step guide",
    ),

    # ── Step 1 ───────────────────────────────────────────────
    build_step(
        "Place [component] in row X, column Y.",
        "Tip about what this component does.",
        rect(0, 0, 100, 100),          # replace with real coords
    ),

    # ── Step 2 ───────────────────────────────────────────────
    build_step(
        "Place [component] in row X, column Y.",
        "Tip about this step.",
        rect(0, 0, 100, 100),
        line((0, 0), (100, 100)),      # add as many shapes as needed
    ),

    # ── Wire Steps ───────────────────────────────────────────
    build_step(
        "Place one end of the wire into Arduino Pin X.<br>"
        "Place the other end in row Y column Z.",
        "Tip about what this wire does.",
        line((0, 0), (100, 0), (100, 100)),
    ),

    # Add more steps by copying any build_step() block above.
]

# ════════════════════════════════════════════════════════════
#  OPTIONAL: extra markdown sections between the diagram
#  and the code editor (delete if not needed)
# ════════════════════════════════════════════════════════════

WIRING_NOTES_MD = """
### 🔎 How to Read the Wiring Diagram

Add any reading-the-diagram guidance here, or delete this section entirely.
"""

# ════════════════════════════════════════════════════════════
#  OPTIONAL: challenge section below the code editor
#  (delete the with-block at the bottom if not needed)
# ════════════════════════════════════════════════════════════

CHALLENGES_MD = """
### ⭐ Bonus Challenges

Add challenge content here, or delete this section.
"""

# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)
circuit = Image.open(CIRCUIT_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])

with tab1:
    hover_zoom_at_cursor(circuit, zoom_factor=2.0, key="circuit1")

with tab2:
    assembly_guide(CIRCUIT_IMAGE, STEPS, PAGE_TITLE)

if WIRING_NOTES_MD:
    st.markdown(WIRING_NOTES_MD)

arduino_block_coder(
    preset=ARDUINO_PRESET,
    pin_refs=ARDUINO_PIN_REFS,
    drawer_content=DRAWER_CONTENT.get(ARDUINO_PRESET),
    username=st.session_state.get("user_id"),
    page=page,
    height=620,
)

if CHALLENGES_MD:
    with st.container(border=True):
        st.markdown(CHALLENGES_MD)

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1, 3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to secure the next mission!")
