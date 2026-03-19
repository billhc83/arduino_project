import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.block_builder_launcher import block_builder_launcher
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY  — edit these 4 lines for every new project
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project Thirteen: The Reaction Timer"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/project_fourteen_banner.png"            # top banner
CIRCUIT_IMAGE    = "graphics/reaction_timer_circuit.png"           # used in both tabs
ARDUINO_PRESET   = "reaction_timer"                         # matches arduino_block_coder preset key
ARDUINO_PIN_REFS = "reaction_timer"                         # usually same as preset

# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## ⏱️ Project 13: The Reaction Timer

🧪 Welcome to the **Arduino Reaction Lab!**

Today you are going to build a **reaction timer**.

Scientists use timers like this to measure **how fast people react**.

But first… you need to build the machine!

---

## 🧠 The Story

Imagine you are running a **super secret training program for astronauts**. 🚀

Astronauts need **fast reactions** to fly spacecraft safely.

Your job is to build a **reaction testing device**.

When the astronaut presses the button…

⏱️ the timer starts.

When they press the button again…

⏱️ the timer stops!

The computer will then tell us **how long it took**.

---

## 🎯 Your Mission

Build a timer that:

👉 Starts when the button is pressed  
👉 Stops when the button is pressed again  
👉 Prints the reaction time to the **Serial Monitor**

Can you build a machine that measures **human reaction speed?**

Let's find out! 🚀

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
    "Place the button onto the breadboard.<br>Place the first leg into row 10, column E.<br>Place the second leg into row 8, column E.<br>Place the third leg into row 10, column F.<br>Place the fourth leg into row 8, column F.",
    "Touch the button to start the timer.  Press it again to stop it. Try to stop it at exactly 5 seconds (remember 5 seconds is 5000 milliseconds",
    rect(708, 249, 818, 340),
    ),

    # ── Step 2 ───────────────────────────────────────────────
    build_step(
    "Place one end of the wire in Arduino Pin 2.<br>Place the other end in row 8, column D.",
    "This is the signal for our timer button",
    line((361, 493), (384, 487), (568, 342), (748, 345), width=20),
    ),

    # ── Wire Steps ───────────────────────────────────────────
    build_step(
    "Place one end of the wire in row 10, column G.<br>Place the other end in the negative / - rail.",
    "This completes our button loop",
    line((787, 253), (768, 98), width=20),
    ),

    # ── Wire Steps ───────────────────────────────────────────
    build_step(
    "Place one end of the wire in Arduino Pin GND.<br>Place the other end in the negative / - rail.",
    "This helps complete our circuit loop",
    )

    # Add more steps by copying any build_step() block above.
]

# ════════════════════════════════════════════════════════════
#  OPTIONAL: extra markdown sections between the diagram
#  and the code editor (delete if not needed)
# ════════════════════════════════════════════════════════════

WIRING_NOTES_MD = """
### 🧠 What Are We Learning?

In this project we are learning how a program can **measure time**.

Computers are very good at keeping track of time.

Your Arduino has a special function called:

`millis()`

This function tells us **how many milliseconds have passed since the Arduino started running**.

A **millisecond** is very tiny!


1000 milliseconds = 1 second


---

### ⏱️ How Our Timer Works

Our program does something very clever.

When the button is pressed the **first time**, the Arduino remembers the time.


startTime = millis()


Now the Arduino knows **when the timer started**.

---

When the button is pressed **again**, the program checks the time again.


time = millis() - startTime


Now the Arduino knows **how much time passed**.

It prints the result to the **Serial Monitor**.

---

### 🔎 Reading the Wiring Diagram

Look carefully at the circuit diagram.

You should notice:

🔌 The button is connected to **Pin 2**  
⚡ One side of the button goes to **ground**

This allows the Arduino to detect **when the button is pressed**.

Programs and circuits **work together**.

The wires send signals…  
and the code decides **what to do with them!**

"""

# ════════════════════════════════════════════════════════════
#  OPTIONAL: challenge section below the code editor
#  (delete the with-block at the bottom if not needed)
# ════════════════════════════════════════════════════════════

CHALLENGES_MD = """
### 🧩 Bonus Challenges

Ready to upgrade your timer? Try these!

---

### 🟢 Challenge 1 — Show Seconds

Right now the timer prints **milliseconds**.

Example:


3842


That means **3.842 seconds**.

Can you change the program so it prints **seconds instead**?

Hint: divide the time by **1000**.

---

### 🟡 Challenge 2 — Add a Timer Light

Add an **LED** to your circuit.

Make the LED behave like this:

💡 LED ON → timer running  
💡 LED OFF → timer stopped

This way we can **see when the timer is active**.

---

### 🔴 Challenge 3 — The 5 Second Challenge

Turn your timer into a **game! 🎮**

Press the button to start the timer.

Now try to press the button again when you think **exactly 5 seconds** have passed.

The Arduino will tell you **how close you were**.

Example:


5032
You were 32 milliseconds late!


Can you get **within 50 milliseconds**?

That's some serious timing skill! ⏱️
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
