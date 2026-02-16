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

hover_zoom_at_cursor(castle_layout, height=300, zoom_factor=2.0, key="castle_zoom")


st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):

    st.markdown("""
## 🧱 Breadboard Layout

##### 💎 :orange[Dragon's Crystal] (The Sensor)
*   **Leg 1:** row 15 column e
*   **Leg 2:** row 20 column e

##### 💡 :red[Warning Fire] (Red LED)
*   **Long leg:** row 10 column e
*   **Short leg:** row 7 column e

##### 🔊 :blue[The Dragon's Roar] (Buzzer)
*   **Long leg (+):** row 5 column f (Right side!)
*   **Short leg (-):** row 10 column f (Right side!)

##### ⚡ Resistor (220 Ohm): 
*   **Leg 1:** row 7 column c
*   **Leg 2:** **- rail** (Ground Rail)

##### ⚡ Resistor (10K Ohm): 
*   **Leg 1:** row 20 column c
*   **Leg 2:** row 25 column c


##### 🧶 Wiring the Defenses

1.  **Pin 13** ➡️ **row 10 column a** (Power for the Fire)
2.  **Pin 5V** ➡️ **row 15 column a** (Power for the Crystal)
3.  **Pin A0** ➡️ **row 25 column a** (Crystal Signal)
4.  **Pin 8** ➡️ **row 5 column j** (Power for the Roar)
5.  **Pin GND** ➡️ **- rail / Ground Rail** (The Main Drain)
6.  **- rail** ➡️ **row 20 column a** (Crystal Ground)
7.  **- rail** ➡️ **row 10 column j** (Roar Ground)
                """)


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
- Every part of our castle sends its "used" energy back to the **Blue Rail**. It's the most important connection on your board! 🚰💨

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
🧪 **Challenge 1:** Can you make the Dragon sound **SAD** by changing `800` to a low `150`? 😢🐲

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
