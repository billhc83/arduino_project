import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
st.set_page_config(layout= "wide")
# --- ASSETS ---
banner = Image.open("graphics/jet_engine_start.png")
engine_start = Image.open("graphics/project_twelve_circuit.png")
st.image(banner)


st.markdown("""
<div style="max-width: 850px; margin: auto;">

## 🛫 Welcome to the Flight Simulator

Today is a big day.

You are sitting in the pilot seat of the simulator. 🧑‍✈️  
I’m still here with you — but your hands are on the controls.

Up until now, you’ve learned how switches work.  
You’ve learned how buttons work.  
You’ve turned lights on.  
You’ve made sounds happen.

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
""", unsafe_allow_html=True)

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Lets Light This Car UP!!!",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the center pin of the switch in row 4, column H. <br>Place the side pin of the switch in row 5, column H",
        "tip": "This is the Engine Armed swtich. Nothing happens unless we arm the engines.",
        "highlights": [
             {"pos": (601, 216, 719, 310), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place the first leg in row 8, column F. <br>Place the second leg in row 10, column F.<br>Place the third leg in row 8 column E.<br>Place the last leg in row 10 column E",
        "tip": "This button starts the engine.",
        "highlights": [
             {"pos": (719, 239, 811, 350), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place the long leg of the buzzer in row 14, column E. <br>Place the short leg of the buzzer in row 14, column F",
        "tip": "This is our engine press the start button to hear it come to life",
        "highlights": [
             {"pos": (799, 222, 909, 344), "shape": "rect"},
             {"pos": (922, 37), "shape": "circle", "radius": 60},
             {"pos": [(917, 56), (861, 248)], "shape": "polyline", "width": 20},
             {"pos": (1034, 563), "shape": "circle", "radius": 60},
             {"pos": [(1043, 550), (850, 314)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the long leg of the LED in row 22, column E. <br>Place the short leg of the LED in row 21, column E",
        "tip": "This is the light that tells us the engines are armed and ready to start",
        "highlights": [
             {"pos": (935, 175, 1069, 347), "shape": "rect"},
             {"pos": [(919, 57), (995, 317)], "shape": "polyline", "width": 20},
             {"pos": [(1040, 542), (1011, 330)], "shape": "polyline", "width": 20},
             {"pos": (922, 44), "shape": "circle", "radius": 60},
             {"pos": (1043, 561), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 21, column D. <br>Place the second leg of the resistor in row 17, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (871, 307, 1034, 384), "shape": "rect"},
             {"pos": (1047, 52), "shape": "circle", "radius": 60},
             {"pos": [(1038, 75), (952, 340)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire into Arduino Pin 9. <br>Place the other end in row 5 column I.",
        "tip": "This is wire lets the Arduino see the position of the switch",
        "highlights": [
             {"pos": [(370, 340), (723, 341), (722, 209), (680, 208)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire into Arduino Pin 7.<br>Place the other end into row 8 column B",
        "tip": "This wire lets the Arduino see if the button is pressed.",
        "highlights": [
             {"pos": [(372, 393), (752, 378)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },   
    {
        "instruction": "Place one end of the wire into Arduino Pin 5.<br>Place the other end of the wire into row 14 column D <br>The side pin goes in row 24 column E",
        "tip": "This wire powers our engine",
        "highlights": [
             {"pos": [(370, 427), (858, 430), (855, 337)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    
    {
        "instruction": "Place one end of the wire in the Arduino Pin 2. <br>Place the other end in row 22 column A",
        "tip": "This wire powers our Engines armed light",
        "highlights": [
             {"pos": [(364, 486), (537, 487), (536, 529), (1012, 532), (1007, 393)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "This wire helps complete our circuit",
        "highlights": [
             {"pos": [(369, 244), (446, 251), (444, 113), (622, 118)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 4 column J. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our switch circuit",
        "highlights": [
             {"pos": [(667, 199), (652, 110)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 10 column J. <br>Place the other end in the negative / - rail",
        "tip": "this wire complete our button circut",
        "highlights": [
             {"pos": [(783, 202), (768, 110)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 14 column J. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our buzzer circuit",
        "highlights": [
             {"pos": [(860, 204), (843, 103)], "shape": "polyline", "width": 20}
             
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 17 column E. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our light circuit",
        "highlights": [
             {"pos": [(915, 331), (922, 106)], "shape": "polyline", "width": 20}

             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(engine_start, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_twelve_circuit.png", steps, "Project 12: Engine Start Sequence (Part 1)")


st.markdown("""
## 🔎 How to Read the Wiring Diagram

Now that you know your mission, let’s look at the wiring diagram. 🕵️‍♂️  
Don’t worry, it looks busy — we just need to notice a few things.

Follow these steps to extract the information you need:

---

### 1️⃣ Find the Parts
Look at the diagram. Can you spot:

- 🔘 The **Switch**
- 🔴 The **Button**
- 💡 The **Engine Light**
- 🔊 The **Buzzer**
- 🖥️ The **Arduino**

That’s all we need to identify right now.

---

### 2️⃣ Follow the Wires
Trace each wire with your eyes:

- Where does this wire start?  
- Where does it end?  
---

### 3️⃣ Match Each Part to a Pin
Now let’s see which pins matter:

- Which pin is the switch connected to?  
- Which pin is the button connected to?  
- Which pin controls the light?  
- Which pin controls the buzzer?  

This is the key step — this tells you **what to control in your code**.

---

### 4️⃣ Ask: Who Controls Who?
Look carefully:

- Does the switch connect directly to the buzzer?  
- Or does it connect to the Arduino?  

Notice: **everything talks to the Arduino**.  
The Arduino decides what happens — that’s where your logic lives.

---

### ✅ Remember
Don’t rush.  
Your job is not to build yet — your job is to **notice and understand**.  

When you know where everything connects, you know exactly what your code must control. 🚀
""")

arduino_block_coder(
    preset = 'engine_start',
    pin_refs= "engine_start",
    drawer_content= DRAWER_CONTENT.get("engine_start") 
)
