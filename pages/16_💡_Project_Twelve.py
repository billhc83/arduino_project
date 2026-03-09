import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line, lbl

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project 12: Night Patrol Alarm"
BANNER_IMAGE     = "graphics/patrol_alarm.png"          # update to your actual banner filename
CIRCUIT_IMAGE    = "graphics/project_thirteen_circuit.png"
ARDUINO_PRESET   = "patrol_alarm"
ARDUINO_PIN_REFS = "patrol_alarm"

# ════════════════════════════════════════════════════════════
#  INTRO
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🚓 Welcome to Night Patrol Academy

The sun has gone down.

The streets are darker now.  
Street lights glow.  
Cars move through the city.

At night, emergency vehicles must be easy to see.

That is why they use **light bars**.

Red lights.  
Blue lights.  
Bright white strobes.

These lights flash in a pattern so drivers can notice them from far away.

Tonight, you are training in the **Emergency Systems Lab** at Night Patrol Academy.

Before a patrol vehicle goes on duty, the light bar must pass inspection.

That is your job today.

You will build the system.  
You will control the lights.  
You will program the flashing pattern.

---

## 🎯 Your Mission

This patrol vehicle has four parts:

- 🔘 A **Master Power Button**
- 🔴 A **Red Light**
- 🔵 A **Blue Light**
- ⚪ A **Clear Strobe Light**

The system follows simple rules.

- If the Master Button is **not pressed** → all lights must stay **OFF**.
- If the Master Button is **pressed** → the light pattern begins.
- The lights must flash **one at a time**.
- The pattern must **repeat again and again**.

When the button isn't pressed, the system must **stop immediately**.

---

## ⏱️ Flash Timing

Emergency lights do not stay on for long.

They flash quickly.

To make this happen, we use **short delays** in the code.

At the Academy we use a standard timing rule.

Each flash must last:

**150 milliseconds**

After the light turns off, we wait another:

**150 milliseconds**

This short pause helps our eyes see the flashing pattern clearly.

When you build your code, make sure you use:

**delay(150)**

for each flash and each pause.

---

## 🔁 The Light Pattern

When the system is ON, the lights will follow this order:

1. 🔴 Red light flashes  
2. 🔵 Blue light flashes  
3. ⚪ Clear light flashes  

Then the pattern starts again.

Red → Blue → White → Repeat.

This pattern continues until the Master Button is released.

---

## 🚨 Remember

You are not just turning lights on.

You are controlling a **system**.

The lights must:
- Flash clearly
- Follow the correct order
- Use the correct delay timing
- Stop when the system is turned OFF

Press the button.

And see if your system passes inspection. 🚓

</div>
"""

# ════════════════════════════════════════════════════════════
#  ASSEMBLY STEPS
# ════════════════════════════════════════════════════════════

STEPS = [
    intro_step(
        "Lets Light This Car UP!!!",
        "Press the next button for a step by step guide",
    ),
    build_step(
        "Place the long leg of the LED in row 18, column E.<br>"
        "Place the short leg of the LED in row 17, column E",
        "Make sure your lights are in the right order.",
        rect(876, 175, 971, 344),
        labels=[lbl("Long Leg", offset_x=100, offset_y=90), lbl("Short Leg", offset_x=-100, offset_y=90)],
    ),
    build_step(
        "Place the long leg of the LED in row 24, column E.<br>"
        "Place the short leg of the LED in row 23, column E.",
        "Make sure your lights are in the right order.",
        rect(994, 181, 1083, 347),
        labels=[lbl("Long Leg", offset_x=100, offset_y=90), lbl("Short Leg", offset_x=-100, offset_y=90)],
    ),
    build_step(
        "Place the long leg of the LED in row 30, column E.<br>"
        "Place the short leg of the LED in row 29, column E",
        "Make sure your lights are in the right order.",
        rect(1093, 168, 1203, 343),
        labels=[lbl("Long\nLeg", offset_x=60, offset_y=180), lbl("Short Leg", offset_x=-75, offset_y=90)],
    ),
    build_step(
        "Place one leg of the 220 ohm resistor in row 17, column D.<br>"
        "Place the other end in row 13, column D",
        "You need small resistors to make LEDs work.",
        rect(805, 318, 940, 376),
    ),
    build_step(
        "Place one leg of the 220 Ohm resistor in row 23, column D.<br>"
        "Place the second leg of the resistor in row 19, column D",
        "The resistor slows down the electricity.",
        rect(929, 305, 1056, 376),
    ),
    build_step(
        "Place one end of the 220 ohm resistor in row 29 column D.<br>"
        "Place the other end in row 25 column D.",
        "Resistors come in many different sizes.",
        rect(1047, 300, 1171, 370),
        labels=[lbl("220 Ohm Resistor", offset_x=-20, offset_y=100)],
    ),
    build_step(
        "Place the button onto the breadboard.<br>"
        "Place the first leg into row 10 column E.<br>"
        "Place the second leg into row 8 column E.<br>"
        "Place the third leg into row 10 column F.<br>"
        "Place the last leg into row 8 column F.",
        "This is how we are going to control the patrol lights.",
        rect(719, 244, 812, 347),
    ),
    build_step(
        "Place one end of the wire into Arduino Pin 8.<br>"
        "Place the other end of the wire into row 18 column C",
        "This wire powers the red LED.",
        line((366, 358), (933, 364)),
    ),
    build_step(
        "Place one end of the wire in the Arduino Pin 6.<br>"
        "Place the other end in row 24 column A",
        "This wire powers the blue LED.",
        line((1048, 401), (876, 413), (364, 411)),
    ),
    build_step(
        "Place one end of the wire in Arduino Pin 4.<br>"
        "Place the other end in row 30 column A",
        "This wire powers our clear LED.",
        line((1165, 399), (1069, 443), (370, 449)),
    ),
    build_step(
        "Place one end of the wire in Arduino Pin 12.<br>"
        "Place the other end in row 8 column D",
        "This wire gets the signal from our button.",
        line((749, 347), (566, 343), (383, 281), (366, 284)),
    ),
    build_step(
        "Place one end of the wire into Arduino Pin GND.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our circuit.",
        line((621, 113), (444, 115), (442, 248), (356, 249)),
    ),
    build_step(
        "Place one end of the wire in row 10 column G.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our button circuit.",
        line((788, 263), (766, 106)),
    ),
    build_step(
        "Place one end of the wire in row 13 column E.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our red LED circuit.",
        line((844, 337), (806, 106)),
    ),
    build_step(
        "Place one end of the wire in row 19 column E.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our blue LED circuit.",
        line((956, 333), (962, 111)),
    ),
    build_step(
        "Place one end of the wire in row 25 column E.<br>"
        "Place the other end in the negative / - rail",
        "This wire completes our clear LED circuit.",
        line((1075, 336), (1078, 103)),
    ),
]

# ════════════════════════════════════════════════════════════
#  OPTIONAL SECTIONS
# ════════════════════════════════════════════════════════════

WIRING_NOTES_MD = """
### 🧰 Create Your Light Variables

Before the lights can flash, the Arduino needs to know **which pins control each light**.

Create a variable for each part of the system in the global section.

Use these variable names:

buttonPin  
redLED  
blueLED  
clearLED  

Each variable should point to the **pin number connected to that part**.

Look at the wiring diagram and choose the correct pin numbers.

Once these variables are created, the rest of the code will use their names to control the lights.

We have filled in some of the blocks to guide you. Can you recognize the pattern, to fill in the rest of the blocks.  Take your time and don't give up.
"""

CHALLENGES_MD = """
### ⭐ Night Patrol Academy Challenges

You have built the basic patrol light system.

But the Academy has extra training missions for students who want to go further.

Try one… or try them all!

---

### ⭐ Level 1 Challenge — Double Flash

Right now each light flashes **one time**.

Upgrade the pattern so each light flashes **two times** before moving to the next light.

Example idea:

Red ON → delay(150) → Red OFF → delay(150)  
Red ON → delay(150) → Red OFF  

Then move to the **Blue Light**.

---

### ⭐⭐ Level 2 Challenge — Faster Strobe

Emergency vehicles sometimes use **faster flashing lights**.

Try changing the delay value to make the lights flash faster.

Example: delay(100) or delay(80)

Watch how the pattern changes when the delay becomes shorter.

---

### ⭐⭐⭐ Level 3 Challenge — Advanced Light Pattern

Create a more exciting light pattern.

Try this order:

Red flash → Blue flash → Clear flash → Blue flash

Then repeat the pattern.

This will create a **back-and-forth light effect** like a real emergency light bar.

---

🚓 These challenges are optional.

But if you complete them, you are thinking like a real systems engineer.
"""

# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line changes per project
# ════════════════════════════════════════════════════════════
st.image(BANNER_IMAGE)
st.markdown(INTRO_MD, unsafe_allow_html=True)

page    = os.path.basename(__file__).replace(".py", "")
circuit = Image.open(CIRCUIT_IMAGE)

tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])

with tab1:
    hover_zoom_at_cursor(circuit, zoom_factor=2.0, key="circuit1")

with tab2:
    assembly_guide(CIRCUIT_IMAGE, STEPS, PAGE_TITLE)

if WIRING_NOTES_MD:
    with st.container(border=True):
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
#with buttoncol1:
 #   if st.button("Next Project", type="primary"):
  #      complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to secure the next mission!")