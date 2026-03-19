import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.block_builder_launcher import block_builder_launcher
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line, lbl

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project 11: Engine System Start"
BANNER_IMAGE     = "graphics/jet_engine_start.png"
CIRCUIT_IMAGE    = "graphics/project_twelve_circuit.png"
ARDUINO_PRESET   = "engine_start"
ARDUINO_PIN_REFS = "engine_start"

# ════════════════════════════════════════════════════════════
#  INTRO
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🛫 Welcome to the Flight Simulator

Today is a big day.

You are sitting in the pilot seat of the simulator. 🧑‍✈️  
I'm still here with you — but your hands are on the controls.

Up until now, you've learned how switches work.  
You've learned how buttons work.  
You've turned lights on.  
You've made sounds happen.

Today…

You decide when the engine starts. 🔥

---

## 🎯 Your Mission

This aircraft has:

- 🔘 An **Arm Switch**
- 🔴 An **Engage Button**
- 💡 An **Engine Light**
- 🔊 An **Engine Sound**

The aircraft follows very clear rules:

- If the Arm Switch is OFF → everything is OFF.
- If the Arm Switch is ON → the aircraft is ready.
- If the system is ready and you press the Engage Button → the engine starts.
- The engine keeps running until you turn the Arm Switch OFF.

Your job is to build the code that makes this happen.

</div>
"""

# ════════════════════════════════════════════════════════════
#  ASSEMBLY STEPS
# ════════════════════════════════════════════════════════════

STEPS = [
    intro_step(
        "Engage Engines!!!!",
        "Press the next button for a step by step guide",
    ),
    build_step(
        "Place the center pin of the switch in row 4, column H.<br>"
        "Place the side pin of the switch in row 5, column H",
        "This is the Engine Armed switch. Nothing happens unless we arm the engines.",
        rect(601, 216, 719, 310),
    ),
    build_step(
        "Place the first leg in row 24, column E.<br>"
        "Place the second leg in row 23, column E.<br>"
        "Place the third leg in row 8 column E.<br>"
        "Place the last leg in row 10 column E",
        "This button starts the engine.",
        rect(719, 239, 811, 350),
    ),
    build_step(
        "Place the long leg of the buzzer in row 14, column E.<br>"
        "Place the short leg of the buzzer in row 14, column F",
        "This is our engine — press the start button to hear it come to life.",
        rect(799, 222, 909, 344),
        circle(922, 37),
        line((917, 56), (861, 248)),
        circle(1034, 563),
        line((1043, 550), (850, 314)),
    ),
    build_step(
        "Place the long leg of the LED in row 22, column E.<br>"
        "Place the short leg of the LED in row 21, column E",
        "This is the light that tells us the engines are armed and ready to start.",
        rect(935, 175, 1069, 347),
        line((919, 57), (995, 317)),
        line((1040, 542), (1011, 330)),
        circle(922, 44),
        circle(1043, 561),
    ),
    build_step(
        "Place one leg of the 220 Ohm resistor in row 21, column D.<br>"
        "Place the second leg of the resistor in row 17, column D",
        "The resistor slows down the electricity.",
        rect(871, 307, 1034, 384),
        circle(1047, 52),
        line((1038, 75), (952, 340)),
    ),
    build_step(
        "Place one end of the wire into Arduino Pin 9.<br>"
        "Place the other end in row 5 column I.",
        "This wire lets the Arduino see the position of the switch.",
        line((370, 340), (723, 341), (722, 209), (680, 208)),
    ),
    build_step(
        "Place one end of the wire into Arduino Pin 7.<br>"
        "Place the other end into row 8 column B",
        "This wire lets the Arduino see if the button is pressed.",
        line((372, 393), (752, 378)),
    ),
    build_step(
        "Place one end of the wire into Arduino Pin 5.<br>"
        "Place the other end of the wire into row 14 column D.<br>"
        "The side pin goes in row 24 column E",
        "This wire powers our engine.",
        line((370, 427), (858, 430), (855, 337)),
    ),
    build_step(
        "Place one end of the wire in the Arduino Pin 2.<br>"
        "Place the other end in row 22 column A",
        "This wire powers our Engines armed light.",
        line((364, 486), (537, 487), (536, 529), (1012, 532), (1007, 393)),
    ),
    build_step(
        "Place one end of the wire in Arduino Pin GND.<br>"
        "Place the other end in the negative / - rail",
        "This wire helps complete our circuit.",
        line((369, 244), (446, 251), (444, 113), (622, 118)),
    ),
    build_step(
        "Place one end of the wire in row 4 column J.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our switch circuit.",
        line((667, 199), (652, 110)),
    ),
    build_step(
        "Place one end of the wire in row 10 column J.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our button circuit.",
        line((783, 202), (768, 110)),
    ),
    build_step(
        "Place one end of the wire in row 14 column J.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our buzzer circuit.",
        line((860, 204), (843, 103)),
    ),
    build_step(
        "Place one end of the wire in row 17 column E.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our light circuit.",
        line((915, 331), (922, 106)),
    ),
]

# ════════════════════════════════════════════════════════════
#  OPTIONAL SECTIONS
# ════════════════════════════════════════════════════════════

WIRING_NOTES_MD = """
## 🔎 How to Read the Wiring Diagram

Now that you know your mission, let's look at the wiring diagram. 🕵️‍♂️  
Don't worry, it looks busy — we just need to notice a few things.

Follow these steps to extract the information you need:

---

### 1️⃣ Find the Parts
Look at the diagram. Can you spot:

- 🔘 The **Switch**
- 🔴 The **Button**
- 💡 The **Engine Light**
- 🔊 The **Buzzer**
- 🖥️ The **Arduino**

---

### 2️⃣ Follow the Wires
Trace each wire with your eyes:

- Where does this wire start?  
- Where does it end?  

---

### 3️⃣ Match Each Part to a Pin
Now let's see which pins matter:

- Which pin is the switch connected to?  
- Which pin is the button connected to?  
- Which pin controls the light?  
- Which pin controls the buzzer?  

This is the key step — this tells you **what to control in your code**.

---

### 4️⃣ Ask: Who Controls Who?

Notice: **everything talks to the Arduino**.  
The Arduino decides what happens — that's where your logic lives.

---

### ✅ Remember
Don't rush. When you know where everything connects, you know exactly what your code must control. 🚀
"""

CHALLENGES_MD = None   # No challenges section for this project

# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line changes per project
# ════════════════════════════════════════════════════════════

page    = os.path.basename(__file__).replace(".py", "")
banner  = Image.open(BANNER_IMAGE)
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

block_builder_launcher(
    preset=ARDUINO_PRESET,
    drawer_content=DRAWER_CONTENT.get(ARDUINO_PRESET),
    username=st.session_state.get("user_id"),
    page=page,
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