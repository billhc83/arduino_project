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

hover_zoom_at_cursor(circuit_layout, height=300, zoom_factor=2.0, key="circuit1")

st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):

    st.markdown("""
### 🔌 Power Setup

- Arduino **GND** → breadboard **negative (–) rail**  
  (All return wires go here — the spaceship’s ground system)

### 🔊 Rocket Buzzer

**Parts**

- Buzzer positive (+) → row 12, column **e**  
- Buzzer negative (–) → row 12, column **f**

**Wires**

- Arduino **pin 8** → row 12 **a**  
- Wire from row 12 **j** → negative (–) rail

### 🔘 Launch Button

**Parts**

- Button leg → row 18 **e**  
- Button leg → row 18 **f**
- Button leg → row 20 **e**  
- Button leg → row 20 **f**

**Wires**

- Arduino **pin 2** → row 18 **a**  
- Wire from row 20 **j** → negative (–) rail
                """)


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