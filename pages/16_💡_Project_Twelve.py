import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
st.set_page_config(layout= "wide")

patrol_alarm = Image.open("graphics/project_thirteen_circuit.png")

st.markdown("""
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
""", unsafe_allow_html=True)

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Lets Light This Car UP!!!",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the long leg of the LED in row 18, column E. <br>Place the short leg of the LED in row 17, column E",
        "tip": "Make sure your lights are in the right order",
        "highlights": [
             {"pos": (876, 175, 971, 344), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        "labels": [  
        {
            "text": "Long Leg",
            "offset_x": 100,
            "offset_y": 90,
            "font_size": 16
        },
        {
            "text": "Short Leg",
            "offset_x": -100,
            "offset_y": 90,
            "font_size": 16
        }
        ]
    },
    {
        "instruction": "Place the long leg of the LED in row 24, column E. <br>Place the short leg of the LED in row 23, column E.",
        "tip": "Make sure your lights are in the right order",
        "highlights": [
             {"pos": (994, 181, 1083, 347), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        "labels": [  
        {
            "text": "Long Leg",
            "offset_x": 100,
            "offset_y": 90,
            "font_size": 16
        },
        {
            "text": "Short Leg",
            "offset_x": -100,
            "offset_y": 90,
            "font_size": 16
        }
        ]
    },
    {
        "instruction": "Place the long leg of the LED in row 30, column E. <br>Place the short leg of the LED in row 29, column E",
        "tip": "Make sure your lights are in the right order",
        "highlights": [
             {"pos": (1093, 168, 1203, 343), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        "labels": [  
        {
            "text": "Long \n"
            " Leg",
            "offset_x": 60,
            "offset_y": 180,
            "font_size": 16
        },
        {
            "text": "Short Leg",
            "offset_x": -75,
            "offset_y": 90,
            "font_size": 16
        }
        ]
    },
    {
        "instruction": "Place one leg of the 220 ohm resistor in row 17, column D. <br>Place the other end in row 13, column D",
        "tip": "You need small resistors to make LED's work",
        "highlights": [
             {"pos": (805, 318, 940, 376), "shape": "rect"},
             ],
        "label":"220 Ohm Resistor",    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 23, column D. <br>Place the second leg of the resistor in row 19, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (929, 305, 1056, 376), "shape": "rect"}
             ],
        "label":"220 Ohm Resistor",      # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the 220 ohm resistor in row 29 column D. <br>Place the other end in row 25 column D.",
        "tip": "Resistors come many different sizes",
        "highlights": [
             {"pos": (1047, 300, 1171, 370), "shape": "rect"},
             ],
        "labels": [  
        {
            "text": "220 Ohm Resistor",
            "offset_x": -20,
            "offset_y": 100,
            "font_size": 16
        }],      # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the button onto the breadboard <br>Place the first leg into row 10 column E.<br>Place the second leg into row 8 column E.<br>Place the third leg into row 10 column F.<br>Place the last leg into row 8 column F.",
        "tip": "This is the way we are going to control the patrol lights",
        "highlights": [
             {"pos": (719, 244, 812, 347), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },   
    {
        "instruction": "Place one end of the wire into Arduino Pin 8.<br>Place the other end of the wire into row 18 column C",
        "tip": "This wire powers the red LED",
        "highlights": [
             {"pos": [(366, 358), (933, 364)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    
    {
        "instruction": "Place one end of the wire in the Arduino Pin 6. <br>Place the other end in row 24 column A",
        "tip": "This wire powers the blue LED",
        "highlights": [
             {"pos": [(1048, 401), (876, 413), (364, 411)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 4. <br>Place the other end in row 30 column A",
        "tip": "This wire powers our clear LED",
        "highlights": [
             {"pos": [(1165, 399), (1069, 443), (370, 449)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 12. <br>Place the other end in row 8 column D",
        "tip": "This wire gets the signal from our button",
        "highlights": [
             {"pos": [(749, 347), (566, 343), (383, 281), (366, 284)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire into Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "This wire complete our circuit",
        "highlights": [
             {"pos": [(621, 113), (444, 115), (442, 248), (356, 249)], "shape": "polyline", "width": 20}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 10 column G. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our button circuit",
        "highlights": [
             {"pos": [(788, 263), (766, 106)], "shape": "polyline", "width": 20}
             
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 13 column E. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our red LED circuit",
        "highlights": [
             {"pos": [(844, 337), (806, 106)], "shape": "polyline", "width": 20}

             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 19 column E. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our blue LED circuit",
        "highlights": [
             {"pos": [(956, 333), (962, 111)], "shape": "polyline", "width": 20}
             
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 25 column E. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our clear LED circuit",
        "highlights": [
             {"pos": [(1075, 336), (1078, 103)], "shape": "polyline", "width": 20}
             
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]

tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(patrol_alarm, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_thirteen_circuit.png", steps, "Project 12: Night Patrol Alarm")



with st.container(border=True):
    st.markdown("""
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
""")
    
from components.arduino_blocks import arduino_block_coder
arduino_block_coder(
    preset='patrol_alarm',
    pin_refs="patrol_alarm",
    drawer_content=DRAWER_CONTENT.get("patrol_alarm"),
    username=st.session_state.get("user_id"),
    height=620 
)

with st.container(border=True):
    st.markdown("""
### ⭐ Night Patrol Academy Challenges

You have built the basic patrol light system.

But the Academy has extra training missions for students who want to go further.

Try one… or try them all!

---

### ⭐ Level 1 Challenge — Double Flash

Right now each light flashes **one time**.

Upgrade the pattern so each light flashes **two times** before moving to the next light.

Example idea:

Red ON  
delay(150)  
Red OFF  
delay(150)

Red ON  
delay(150)  
Red OFF  

Then move to the **Blue Light**.

---

### ⭐⭐ Level 2 Challenge — Faster Strobe

Emergency vehicles sometimes use **faster flashing lights**.

Try changing the delay value to make the lights flash faster.

Example:

delay(100)

or

delay(80)

Watch how the pattern changes when the delay becomes shorter.

---

### ⭐⭐⭐ Level 3 Challenge — Advanced Light Pattern

Create a more exciting light pattern.

Try this order:

Red flash  
Blue flash  
Clear flash  
Blue flash  

Then repeat the pattern.

This will create a **back-and-forth light effect** like a real emergency light bar.

---

🚓 These challenges are optional.

But if you complete them, you are thinking like a real systems engineer.
""")