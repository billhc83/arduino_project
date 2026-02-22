import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---

# --- ASSETS ---
nightlight_layout = Image.open("graphics/project_seven_circuit.png")

# --- HEADER ---
st.title("💡 Project 7 - The Automagic Night Light!")

st.markdown("""
Put on your **Engineer Hat**! 👷‍♂️👷‍♀️

Have you ever wondered how streetlights know exactly when to turn on at night? They use a "Magic Eye" just like yours! 

Today, you will engineer a **Smart Night Light**. It will stay OFF during the day to save energy, but it will **automagically** glow when the sun goes down! 🌅➡️🌃
""")
st.markdown("""
### 🛠️ The Engineer’s Automatic Night Light Blueprint

**What you need:**

**1× Photoresistor** (The Light Detective) 👁️  
Always on the lookout! This part checks how bright the room is and knows when the lights go out.

**1× LED** (The Night Light) 💡  
The friendly glow that turns on when it gets dark, helping guide the way.

**1× 220-ohm Resistor** (The LED Bodyguard) ⚡  
Keeps the LED safe by stopping too much electricity from rushing in.

**1× 10k-ohm Resistor** (The Sensor Sidekick) ⚡  
Works together with the light detective to decide exactly when it’s dark enough to turn the light on.
""")

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Activate the launch button!!",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 6, column E. <br>Place the LED short leg in row 5, column E",
        "tip": "The long leg is positive — it's called the anode!",
        "highlights": [
             {"pos": (651, 232, 841, 382), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 5, column D. <br>Place the second leg of the resistor in row 1, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (629, 356, 766, 435), "shape": "rect"},
             {"pos": (507, 449), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },  
    {
        "instruction": "Place one leg of the photoresistor in row 15, column F. <br>Place the second leg of the photoresistor in row 18, column F",
        "tip": "This is the photoresistor, it is a light sensor",
        "highlights": [
             {"pos": (962, 309), "shape": "circle", "radius": 45},
             {"pos": (773, 577, 1006, 662), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one end of the 10k Ohm resistor in row 11 column H. <br>Place the other end of the 10k resistor in row  15 column H",
        "tip": "resistors come in many different sizes",
        "highlights": [
             {"pos": (745, 77), "shape": "circle", "radius": 55},
             {"pos": (831, 260, 960, 303), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "Ground wires help complete our circuit loop",
        "highlights": [
             {"pos": (590, 496, 691, 526), "shape": "rect"},
             {"pos": (590, 285, 624, 526), "shape": "rect"},
             {"pos": (388, 285, 624, 311), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin A0. <br>Place the other end in row 15 column J",
        "tip": "this wire is listening signal from the light sensor",
        "highlights": [
             {"pos": (906, 210, 952, 265), "shape": "rect"},
             {"pos": (215, 208, 946, 246), "shape": "rect"},
             {"pos": (52, 208, 227, 513), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 5V. <br>Place the other end in row 18 column J",
        "tip": "This wire powers our night lights sensor",
        "highlights": [
             {"pos": (962, 172, 1010, 260), "shape": "rect"},
             {"pos": (600, 172, 1006, 214), "shape": "rect"},
             {"pos": (600, 6, 645, 214), "shape": "rect"},
             {"pos": (8, 0, 645, 50), "shape": "rect"},
             {"pos": (0, 12, 84, 408), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 13. <br>Place the other end in row 6 column A",
        "tip": "This wire powers our night light",
        "highlights": [
             {"pos": (740, 435, 831, 571), "shape": "rect"},
             {"pos": (529, 547, 770, 571), "shape": "rect"},
             {"pos": (529, 307, 578, 560), "shape": "rect"},
             {"pos": (402, 307, 578, 331), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 1 column A. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the light",
        "highlights": [
             {"pos": (641, 433, 768, 530), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 11 column F. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the light sensor",
        "highlights": [
             {"pos": (827, 309, 1041, 532), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(nightlight_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_seven_circuit.png", steps, "Project 7: The Automatic Night Light")

st.info("🧠 **Engineer Tip:** We are combining an **INPUT** (the eye) with an **OUTPUT** (the light) to make a smart machine!")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

with code_col1:
    st.markdown("## 💻 The Smart Logic")
    st.code("""
int lightSensor = A0;
int nightLight = 13;

void setup() {
  pinMode(nightLight, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int brightness = analogRead(lightSensor);
  Serial.println(brightness);

  // If it's dark (number is low)...
  if (brightness < 300) {
    digitalWrite(nightLight, HIGH); // Light ON!
    Serial.println("It's dark! Light ON 🌙");
  } 
  // If it's bright...
  else {
    digitalWrite(nightLight, LOW);  // Light OFF!
    Serial.println("Sun is up! Light OFF ☀️");
  }

  delay(100); 
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 Engineering Secrets

**Input vs. Output**
- The **Sensor** is an input (information coming in). The **LED** is an output (action going out). 📥➡️📤

**The "Else" Statement**
- This is the Arduino's way of saying **"Otherwise."** 
- *IF* it is dark, do this. *ELSE* (otherwise), do that! It’s like a fork in the road. 🍴

**Testing the Threshold**
- We used the number **300**. If your room is very bright, you might need a different number! 🔢
""")

# --- INFO BOXES ---
st.info("""
### 🕵️‍♂️ Lab Testing
1. Open your **Serial Monitor**.
2. Cup your hands over the sensor. Does the LED turn on? 👐
3. Let go. Does it turn off? 💡
4. If it doesn't work, check your **brightness number** in the monitor!
""")

st.info("""
### 🏆 Promotion Challenges
🧪 **Challenge 1:** Can you make the LED turn on only when it is **Pitch Black** (try a very low number like 100)? 🌑

🧪 **Challenge 2:** Engineering Upgrade! Can you make a **Buzzer** beep once whenever the light turns on? 🔊
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Ready for your next Engineering Project?")
