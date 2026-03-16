import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

castle_layout = Image.open("graphics/project_eight_circuit.png")


# --- HEADER ---    
st.title("🏰 Project 8 - The Dragon's Crystal Alarm!")

st.markdown("""
Greetings, **Grand Dungeon Master**! 👑📜

The Kingdom's greatest treasure—the **Golden Gear**—is in danger! Sneaky shadow-thieves are trying to creep into the dungeon. 

You must build an automated **Perimeter Alarm**. It uses a legendary **Dragon's Crystal** (Photoresistor) to watch the hallways. If it sees a shadow pass by, it will trigger a **Dragon's Roar** (Buzzer) and flash the **Warning Fire** (LED)! 🚨🐉

Grab your tools, Master Engineer! We need to fit all our defenses onto the board before sunset! ⚔️💎
""")
st.markdown("""
### 🗝️🕯️ The Shadow Thief Detection Blueprint

**Arcane Components (a.k.a. normal electronics):**

**1× Photoresistor** (The Shadow Watcher) 👁️
Constantly monitors the dungeon light. When a thief blocks the light, it knows.

**1× LED** (The Alarm Rune) 🔴
Flashes the instant a shadow crosses the warded path.

**1× 220-ohm Resistor (Rune Stabilizer) ⚡**
Protects the alarm rune from overload.

**1× 10k-ohm Resistor (Shadow Reference Sigil) ⚖️**
Sets the light threshold so only real intrusions trigger the trap.

**1× Buzzer (The Silent-Breaker) 🔊**
Emits a sharp warning tone — stealth instantly ruined.
""")
from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Protect the dragon crystal",
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
             {"pos": (500, 499), "shape": "circle", "radius": 60}
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
        "instruction": "Place the buzzer long leg in row 25, column E. <br>Place the buzzer short leg in row 28, column E",
        "tip": "This is the alarm",
        "highlights": [
             {"pos": (1161, 382), "shape": "circle", "radius": 60},
             {"pos": (1113, 95), "shape": "circle", "radius": 60},
             {"pos": (1215, 584), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
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
        "instruction": "Place one end of the wire in Arduino Pin 8. <br>Place the other end in row 25 column A",
        "tip": "This wire powers our alarm",
        "highlights": [
             {"pos": (1107, 445, 1157, 594), "shape": "rect"},
             {"pos": (526, 565, 1147, 594), "shape": "rect"},
             {"pos": (522, 405, 554, 590), "shape": "rect"},
             {"pos": (396, 401, 554, 435), "shape": "rect"}
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
    },
    {
        "instruction": "Place one end of the wire in row 28 column A. <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the alarm",
        "highlights": [
             {"pos": (1153, 433, 1233, 543), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(castle_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_eight_circuit.png", steps, "Project 8: The Dragons Crystal Alarm")


st.info("""
🧠 **Dungeon Master's Trick:** 
Our breadboard has a "valley" in the middle. We put the **Buzzer** on the right side (columns f to j) to make more room! Both sides work exactly the same way. ⛰️🚶‍♂️
""")
    
# --- CODE SECTION ---
code_col1, code_col2 = st.columns(2)

with code_col1:
    st.markdown("## 📜 The Master's Decree")
    st.code("""
int crystalPin = A0;
int firePin = 13;
int roarPin = 8;

void setup() {
  pinMode(firePin, OUTPUT);
  pinMode(roarPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("--- DEFENSES ARMED! ---");
}

void loop() {
  int lightLevel = analogRead(crystalPin);
  
  Serial.print("Crystal Light: ");
  Serial.println(lightLevel);

  if (lightLevel < 350) {
    Serial.println("🚨 INTRUDER DETECTED! 🚨");
    
    digitalWrite(firePin, HIGH); 
    tone(roarPin, 800);         
    delay(150);
    
    digitalWrite(firePin, LOW);  
    noTone(roarPin);             
    delay(150);
  } 
  else {
    digitalWrite(firePin, LOW);
    noTone(roarPin);
    delay(100);
  }
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How the Magic Works

**The Two Sides**
- Electricity can't jump across the middle gap (the valley). We use wires to send power to the right side so the **Buzzer** can roar! ⚡🌉

**The Ground Rail (-)**
- Every part of our castle sends its "used" energy back to the **Blue Rail**. It's the most important connection on your board! 🏰

**Tone Control**
- The Arduino sends a fast "wiggle" of electricity to Pin 8 to make the buzzer vibrate. That's how we get sound! 🔊🎶
""")

# --- INFO BOXES ---
st.info("""
### 🔎 The Magic Map (Serial Monitor)
Open your Arduino Serial Monitor
1. Watch the numbers fly by. This is the **Light Level**.
2. Wave your hand over the **Dragon's Crystal**. 🖐️✨
3. Watch the number drop and listen for the **Dragon's Roar**! 🐲
""")

st.info("""
### 🏆 Grand Master Challenges
🧪 **Challenge 1:** Can you make the Dragon sound **SAD** by changing `800` to a low `500`? 😢🐲

🧪 **Challenge 2:** Change the code so the light flashes **Super Fast** by changing the `delay` to `50`! ⚡
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to defend the next Tower!")
