import streamlit as st
from utils.utils import hover_zoom_at_cursor
from PIL import Image
from utils.utils import complete_step_and_continue, get_automated_pages

# Show toast **once** after rerun
# User-closable toast notification


circuit_layout = Image.open("graphics/project_four_circuit.png")

st.title("🚀Project 4 – Space Station Launch Button")

st.markdown("""

Welcome to the space station, Astronaut! 👨‍🚀👩‍🚀
Today is a very important day — you are helping launch a rocket into space!

Inside the rocket is a spaceship computer that watches everything and keeps the mission safe.
Wires run all through the rocket, carrying messages just like space roads.

When it is time to launch, YOU press the big launch button 🔘
The computer wakes up and starts the launch sequence.

Suddenly…
🚨 BEEP! BEEP! BEEP! 🚨

The launch alarm sounds to warn everyone that the rocket is about to lift off!

This project teaches the rocket how to:

Listen for a button press

Make a sound when something important happens

Follow your commands, just like a real spacecraft

Get ready…
3… 2… 1… LAUNCH! 🚀✨
""")

st.markdown("""
## 🔌 Build the Circuit

###### What parts do I need?

🟦 **Arduino UNO** (The Spaceship’s Computer!)  
This is mission control onboard the rocket. It listens for the launch command and tells everything else what to do.

〰️ **Jumper Wires** (The Rocket’s Wiring!)  
These connect all the systems together so signals can travel at light speed.

🔘 **Push Button** (The Launch Button!)  
Press this button to start the launch sequence — no going back once it’s pushed!

🔔 **Buzzer** (The Launch Alarm!)  
Sounds the warning alarm so everyone knows the rocket is about to lift off!
""")
from utils.assembly_guide import assembly_guide, coordinate_picker
steps = [
    {
        "instruction": "Activate the launch button!!",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the buzzer long leg in row 12, column E. <br>Place the buzzer short leg in row 12, column F",
        "tip": "This is the launch alarm",
        "highlights": [
             {"pos": (823, 287), "shape": "circle", "radius": 55},
             {"pos": (846, 565), "shape": "circle", "radius": 55},
             {"pos": (882, 55), "shape": "circle", "radius": 55}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place the button onto the breadboard. <br>There are 4 legs on the button, each one goes to its own spot on the breadboard. <br>Button leg → row 18 column e <br>Button leg → row 18 column f <br>Button leg → row 20 column e <br>Button leg → row 20 column f",
        "tip": "The button will control the launch alarm",
        "highlights": [
             {"pos": (905, 224, 1010, 360), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (352, 91, 648, 270), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 8. <br>Place the other end in row 12 column A",
        "tip": "This wire sends the power to our launch alarm",
        "highlights": [
             {"pos": (376, 353, 846, 452), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 2. <br>Place the other end in row 18 column A",
        "tip": "this wire is listening for the button to be pressed",
        "highlights": [
             {"pos": (905, 387, 960, 543), "shape": "rect"},
             {"pos": (369, 469, 924, 542), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 12 column J  . <br>Place the other end in the negative / - rail",
        "tip": "Wires are like roads for electicity.  A circuit is like a race track for electricity! We must make a loop. This wire connects our circuit back to the Arduino",
        "highlights": [
             {"pos": (673, 100, 844, 219), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 20 column J. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop.  it connects our button back to the Arduino",
        "highlights": [
             {"pos": (928, 95, 1013, 224), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(circuit_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_four_circuit.png", steps, "Project 4: Space Station Launch Button")

code1,code2 = st.columns(2)

with code1:
    st.markdown("## 💻 Rocket Control Code")
    st.code("""
void setup() {
  pinMode(8, OUTPUT);
  pinMode(2, INPUT_PULLUP);
}

void loop() {
  if (digitalRead(2) == LOW) {
    digitalWrite(8, HIGH);
  } else {
    digitalWrite(8, LOW);
  }
}
""", language="cpp")

with code2:
    st.markdown("""
## 🧬 Code Translation (Space Edition)

**setup()**

- Pin 8 powers the rocket buzzer 🔊🚀  
- Pin 2 listens for your launch button 👆

**loop()**

- Check the button 👀  
- Pressed → Buzzer ON (engine roaring!) 🛸  
- Not pressed → Buzzer OFF (rocket rests) 😴
""")

# ---------- Optional Info Boxes ----------
st.info("""
### 🌟 Space Explorer Pro Tips

💡 Tip 1: Make sure the buzzer’s + and – are in the correct holes!  
💡 Tip 2: Follow the energy path like a rocket fuel line 🚀  
💡 Tip 3: If you want a louder buzzer remove the resistor !!!!⚡
""")

st.info("""
### 🔬 Space Explorer Challenges

🧪 Challenge 1: Make the buzzer beep faster or slower by adding delays.  
🧪 Challenge 2: Add a second button that activates a warning light in addition to the buzzer.  
""")
from utils.steps import complete_step_and_continue
from utils.utils import get_automated_pages

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type = "primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to add the next project to the menu")