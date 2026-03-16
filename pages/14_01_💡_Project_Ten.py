import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
spy_vault_layout = Image.open("graphics/project_ten_circuit.png")

# --- HEADER ---
st.title("🕵️‍♂️ Project 10 - The Spy Vault Security Console")

st.markdown("""
Welcome back, **Agent Engineer**! 🕶️💼

The Agency needs your help! You are building the high-security lock for the **Top Secret Spy Vault**. To open the heavy steel doors, you need to slide two **Secret Key Cards** (Switches) at the exact same time. 

We are going to use **Variables** as **Security Locks**. In your code, a variable will track if each bolt is "Locked" (0) or "Unlocked" (1). Only when both bolts are pulled back will the **Vault Light** turn on! 🚨🔓

Ready to secure the base? Let's get to work! ⚔️🛡️
""")

st.markdown("""
## 🛡️ Build the Top Secret Spy Vault Security Lock

###### What parts do I need?

🟦 **Arduino UNO** (The Mission Control Brain!)  
The secret agent computer that checks the key card switches and controls the vault alert light.

🔘 **2 Switches** (The Key Card Readers!)  
Both must be activated at the same time to unlock the vault — only the real agents know the code.

✨ **LED** (The Vault Indicator!)  
Lights up when the secret lock is successfully activated — mission accomplished!

⚡ **Resistor** (The Electricity Guard!)  
Keeps the LED safe by controlling the current so nothing gets fried.
""")

from utils.assembly_guide import assembly_guide, coordinate_picker
steps = [
    {
        "instruction": "Protect the Spy Vault",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 12, column E. <br>Place the LED short leg in row 11, column E",
        "tip": "The long leg is positive — it's called the anode!",
        "highlights": [
             {"pos": (766, 231, 934, 390), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 11, column D. <br>Place the second leg of the resistor in row 7, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (733, 361, 879, 423), "shape": "rect"},
             {"pos": (540, 208), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },  
    {
        "instruction": "Place Switch 1 on the breadboard.<br>The centre pin goes in row 24 column E <br>The side pin goes in row 25 column E",
        "tip": "The switch acts like a key card",
        "highlights": [
             {"pos": (1034, 280, 1150, 398), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place Switch 2 on the breadboard.<br>The centre pin goes in row 17 column E <br>The side pin goes in row 18 column E",
        "tip": "The security locks turn on and off with the switches",
        "highlights": [
             {"pos": (902, 290, 1013, 396), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin GND. <br>Place the other end in row 7 column E",
        "tip": "Ground wires help complete our circuit loop",
        "highlights": [
             {"pos": (382, 282, 790, 385), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "Ground wires help complete our circuit loop",
        "highlights": [
             {"pos": (8, 0, 645, 50), "shape": "rect"},
             {"pos": (0, 12, 84, 415), "shape": "rect"},
             {"pos": (424, 0, 668, 184), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 8. <br>Place the other end in row 12 column A",
        "tip": "This wire powers our LED <br> Light On = Access Granted",
        "highlights": [
             {"pos": (390, 392, 534, 431), "shape": "rect"},
             {"pos": (494, 392, 534, 502), "shape": "rect"},
             {"pos": (494, 433, 881, 502), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 3. <br>Place the other end in row 17 column A",
        "tip": "This is the signal wire for Switch 2",
        "highlights": [
             {"pos": (924, 437, 979, 564), "shape": "rect"},
             {"pos": (534, 525, 975, 566), "shape": "rect"},
              {"pos": (559, 547), "shape": "circle", "radius": 25},
              {"pos": (550, 544), "shape": "circle", "radius": 25},
              {"pos": (540, 541), "shape": "circle", "radius": 25},
              {"pos": (530, 538), "shape": "circle", "radius": 25},
              {"pos": (520, 535), "shape": "circle", "radius": 25},
              {"pos": (510, 532), "shape": "circle", "radius": 25},
              {"pos": (500, 529), "shape": "circle", "radius": 25},
              {"pos": (490, 526), "shape": "circle", "radius": 25},
              {"pos": (480, 523), "shape": "circle", "radius": 25},
              {"pos": (470, 520), "shape": "circle", "radius": 25},
              {"pos": (460, 519), "shape": "circle", "radius": 25},
              {"pos": (450, 519), "shape": "circle", "radius": 25},
              {"pos": (440, 519), "shape": "circle", "radius": 25},
              {"pos": (430, 519), "shape": "circle", "radius": 25},
              {"pos": (420, 519), "shape": "circle", "radius": 25},
              {"pos": (410, 519), "shape": "circle", "radius": 25}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 3. <br>Place the other end in row 24 column A",
        "tip": "This is the signal wire for Switch 1",
        "highlights": [
             {"pos": (1062, 429, 1115, 590), "shape": "rect"},
             {"pos": (540, 562, 1115, 600), "shape": "rect"},
             {"pos": (559, 587), "shape": "circle", "radius": 15},
             {"pos": (550, 584), "shape": "circle", "radius": 15},
             {"pos": (540, 581), "shape": "circle", "radius": 15},
             {"pos": (530, 578), "shape": "circle", "radius": 15},
             {"pos": (520, 575), "shape": "circle", "radius": 15},
             {"pos": (510, 572), "shape": "circle", "radius": 15},
             {"pos": (500, 569), "shape": "circle", "radius": 15},
             {"pos": (490, 566), "shape": "circle", "radius": 15},
             {"pos": (480, 563), "shape": "circle", "radius": 15},
             {"pos": (470, 560), "shape": "circle", "radius": 15},
             {"pos": (460, 557), "shape": "circle", "radius": 15},
             {"pos": (450, 554), "shape": "circle", "radius": 15},
             {"pos": (440, 551), "shape": "circle", "radius": 15},
             {"pos": (430, 548), "shape": "circle", "radius": 15},
             {"pos": (420, 545), "shape": "circle", "radius": 15},
             {"pos": (410, 542), "shape": "circle", "radius": 15}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 18 column D. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the switch",
        "highlights": [
             {"pos": (953, 135, 1046, 411), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 25 column D. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the swtich",
        "highlights": [
             {"pos": (1095, 141, 1174, 406), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(spy_vault_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_ten_circuit.png", steps, "Project 10: The Spy Vault Security Console")

st.info("""
🧠 **Spy Logic Secret:**
We are using **Variables** to store a "Status." 
- `boltA = 0` means the first lock is stuck.
- `boltA = 1` means the first lock is open! 🔓

The computer checks these "Status Pockets" to see if it's safe to open the door.
""")
    

# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.75,1.25])

with code_col1:
    st.markdown("## 📜 The Security Script")
    st.code("""
// 🔐 Our Security Lock Variables
int LockA = 0; 
int LockB = 0;

void setup() {
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
  Serial.println("--- VAULT SYSTEM ARMED ---");
}

void loop() {
  // 1. Read the Key Cards and update our Variables!
  LockA = digitalRead(2);
  LockB = digitalRead(3);

  // 2. The Logic: Check if BOTH bolts are Unlocked (1)
  if (LockA == 1 && LockB == 1) {
    digitalWrite(8, HIGH);
    Serial.println("🔓 ACCESS GRANTED: Vault Open!");
  } 
  else {
    digitalWrite(8, LOW);
    Serial.println("🔒 ACCESS DENIED: Locks Engaged.");
  }
  
  delay(500); 
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How the Spy Logic Works

**The "&&" Code** 
- This symbol means **"AND."** It’s like a secret handshake. The computer asks: "Is Lock A open **AND** is Lock B open?" If the answer is YES to both, the light turns on! 🤝🚨

**Variables as Memory**
- The `LockA` variable "remembers" what you did to the first switch even while the computer is busy checking the second switch. 🧩🧠

**Decision Making**
- Engineers use variables to help the computer make decisions. Without the variable, the computer wouldn't know if both switches were flipped!
""")

# --- INFO BOXES ---
st.info("""
### 🔎 Vault Monitor
Open your [Arduino Serial Monitor](https://docs.arduino.cc) 🔎. 
1. Flip one switch. Does the vault open? (Nope!) 🔒
2. Flip the second switch. Watch the screen change to **"ACCESS GRANTED"**! 🔓✨
""")

st.info("""
### 🏆 Special Agent Challenges
🧪 **Challenge 1: The Fast Lock.** Can you change the `delay` to `100` so the vault reacts at super-speed? ⚡
🧪 **Challenge 2: Hidden Message.** Can you change the "Access Denied" message to say **"INTRUDER ALERT!"**? 🕵️‍♂️🚫
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to secure the next mission!")
