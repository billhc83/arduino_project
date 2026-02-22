import streamlit as st
from utils.utils import hover_zoom_at_cursor
from PIL import Image
from utils.utils import  get_automated_pages
from utils.steps import complete_step_and_continue

circuit_layout = Image.open("graphics/project_three_circuit.png")


st.title("🧪 Project 3 – Mad Scientist Button Machine")

from utils.utils import intro_player
intro_player("https://github.com/billhc83/arduino_project/releases/download/v1.0.2/project_three_intro_vid.mp4.mp4")

st.markdown("""
Welcome to the Mad Scientist Laboratory! 🧠⚡
            
Strange machines are buzzing… wires are glowing… and something amazing is about to happen!

In this experiment, YOU are the mad scientist 😈
Your job is to control a powerful energy crystal using a button.

👉 Press the button
The crystal wakes up and the light turns ON 💡

✋ Let go of the button
The crystal goes back to sleep and the light turns OFF 😴

This experiment teaches the machine to listen to you.
Press means ON.
Release means OFF.

Mwahahaha!
You are in control of the experiment! 🧪⚡
""")

st.markdown("""
## 🔌 Build the Circuit

###### What parts do I need?

🟦 **Arduino UNO** (The Mad Scientist’s Super Brain!)  
The powerful brain of the lab that controls the experiment and watches for button presses.

⚡ **Resistor** (The Electricity Tamer!)  
Slows the wild electricity down so it doesn’t escape or fry the experiment!

✨ **LED (Any Color)** (The Energy Crystal!)  
This crystal glows with mysterious power when the experiment is activated.

〰️ **Jumper Wires** (The Lab Cables!)  
Carry energy between parts as the experiment comes to life.

🔘 **Push Button** (The Experiment Trigger!)  
Press and hold to activate the energy crystal — release it and the power shuts down!
""")

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Let light the energy crystal",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 12, column E. <br>Place the LED short leg in row 11, column E",
        "tip": "The long leg is positive — it's called the anode!",
        "highlights": [
             {"pos": (733, 194, 903, 319), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 ohm resistor in row 11, column D. <br>Place the second leg of the resistor in row 7, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (691, 307, 834, 368), "shape": "rect"},
             {"pos": (500, 161), "shape": "circle", "radius": 50}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the button onto the breadboard. <br>There are 4 legs on the button, each one goes to its own spot on the breadboard. <br>Button leg → row 18 e <br>Button leg → row 18 f <br>Button leg → row 20 e <br>Button leg → row 20 f",
        "tip": "The button will let us control the energy crystal",
        "highlights": [
             {"pos": (905, 224, 1010, 360), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (328, 82, 639, 271), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 8. <br>Place the other end in row 12 column A",
        "tip": "This wire sends the power to the energy crystal (light)",
        "highlights": [
             {"pos": (357, 350, 838, 448), "shape": "rect"}  
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 2. <br>Place the other end in row 18 column A",
        "tip": "this wire is listening for the button to be pressed",
        "highlights": [
             {"pos": (929, 398, 952, 500), "shape": "rect"},
             {"pos": (382, 486, 952, 540), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 7 column E. <br>Place the other end in the negative / - rail",
        "tip": "Wires are like roads for electicity.  A circuit is like a race track for electricity! We must make a loop. This wire connects our circuit back to the Arduino",
        "highlights": [
             {"pos": (660, 101, 760, 340), "shape": "rect"}
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

  assembly_guide("graphics/project_three_circuit.png", steps, "Project 3: Mad Scientist Button Machine")

code1, code2 = st.columns(2)

with code1:
    st.markdown("## 💻 Secret Lab Code")
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
    st.info("""
            
### 🧪 Mad Scientist Pro Tips

💡 **Tip 1: Follow the electricity path!**  
Pretend electricity is a little bug 🐜 traveling from the pin, through the LED, and back to the ground rail. Can you see its path?  

💡 **Tip 2: One lead per hole!**  
Just like a tiny puzzle, each wire or part gets its own hole. Two things in the same hole can cause a “traffic jam”! 🚦  

💡 **Tip 3: Press slowly and watch!**  
Press the button and see the LED wake up. Let go and see it sleep. Your experiment is alive! ⚡😴
""")
    st.info("""

 **Challenge: Mystery Colors**  
If you have LEDs of different colors, swap the green or yellow LED in place of the first one. What happens when the button is pressed? Can you predict the color?  

 🧪 **Challenge: Faster or Slower**  
Add a tiny delay in the code to make the LED blink faster or slower. Watch how the energy crystal behaves! ⚡💡           
            """)

with code2:
    st.markdown("""
## 🧬 Code Translation (Scientist Edition)

**These lines:**

pinMode(8, OUTPUT);
pinMode(2, INPUT_PULLUP);

                
Means:

> “Door 8 sends electricity to the crystal 💡”  
> “Door 2 listens for the button 🔘”

---

 **This spell:**

digitalRead(2)
                

Means:

> “Is the button being pressed?”

LOW = pressed 😄  
HIGH = not pressed 😴  

---

**This spell:**
                
digitalWrite(8, HIGH);
                

Means:

> “Turn the crystal ON!” 💥

And:

digitalWrite(8, LOW);
                

Means:

> “Turn the crystal OFF.” 🌑

---

**The loop**

Runs forever like a bubbling experiment 🧪♻️

Check → Decide → Glow → Repeat!

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