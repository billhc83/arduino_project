import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
manual_car_layout = Image.open("graphics/project_eleven_circuit.png")

# --- HEADER ---
st.title("🏎️ Project 11 - The Manual Super Car (Part 1)")

st.markdown("""
Welcome back to the Garage, **Master Mechanic**! 🛠️

Before we make our car "Smart," we need to build the **Manual Dash**. In this version, every light and sound has its own physical control. 

You are going to engineer a **Headlight Switch**, a **Brake Pedal**, and a **Horn Button**! You are the pilot, and the car does exactly what your fingers tell it to do. 🕹️✨
""")
hover_zoom_at_cursor(manual_car_layout, height=300, zoom_factor=2.0, key="manual_car_zoom")

st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):
    st.markdown("""
## 🧱 The Manual Dash Blueprint
*We are using the **Magic 5** coordinates and the **- Rail** to keep our workshop tidy!*

##### 💡 :white[Headlights] (LED)
*   **Long leg:** row 30 column e
*   **Short leg:** row 29 column e

##### 💡 :red[Brake Lights] (LED)
*   **Long leg:** row 1 column e
*   **Short leg:** row 2 column e

##### 🔊 :blue[The Horn] (Buzzer)
*   **Long leg (+):** row 18 column e
*   **Short leg (-):** row 18 column f

##### 🔑 :green[Headlight Switch] (Slide Switch)
*   **Center Pin:** row 23 column e
*   **Side Pin:** row 24 column e

##### 🔘 :orange[Brake Pedal] (Button)
*   **Leg 1:** row 10 column e
*   **Leg 2:** row 8 column e
*   **Leg 1:** row 10 column f
*   **Leg 2:** row 8 column f

##### 🔘 :orange[Horn Button] (Button)
*   **Leg 1:** row 14 column e
*   **Leg 2:** row 12 column e
*   **Leg 1:** row 14 column f
*   **Leg 2:** row 12 column f

##### ⚡ Resistors (220 Ohm x 2): 
*   **Resistor 1:** row 2 column d ➡️ row 6 column d
*   **Resistor 2:** row 29 column d ➡️ row 25 column d

##### 🧶 Wiring the Manual Dash
                
**We need both ground rails this time add a wire from a GND pin to each - rail
1.  **Pin GND** ➡️ **- rail / Ground Rail** X 2 (The Two Main Drains) 🚰 
2.  **Pin 13** ➡️ **row 30 column a** (Headlight Power)
3.  **Pin 12** ➡️ **row 1 column d** (Brake Power)
4.  **Pin 8** ➡️ **row 18 column c** (Horn Power)
5.  **Pin 2** ➡️ **row 23 column a** (Switch Signal)
6.  **Pin 3** ➡️ **row 8 column a** (Brake Signal)
7.  **Pin 4** ➡️ **row 12 column b** (Horn Signal)
9.  **row 10 column j ➡️ **- rail** (Brake Drain)
10. **row 14 column j** ➡️ **- rail** (Horn Drain)
11. **row 18 column j** ➡️ **- rail** (Buzzer Drain)
12.  **- rail** ➡️ **row 6 column a** (Brake Light Drain)
13.  **- rail** ➡️ **row 24 column a** (Headlight Switch Drain)
14.  **- rail** ➡️ **row 25 column c** (Brake Signal)
                """)
st.info("""
🧠 **Mechanic's Secret:** 
In this project, the Arduino is acting like a **Messenger**. 
It waits for you to press a button, and then it sends a "Go" signal to the light or buzzer. 
Every action needs **YOU**! 🕹️➡️💡
""")
# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

with code_col1:
    st.markdown("## 📜 The Manual Control Script")
    st.code("""
void setup() {
  pinMode(13, OUTPUT); // Headlights
  pinMode(12, OUTPUT); // Brakes
  pinMode(8, OUTPUT);  // Horn
  
  pinMode(2, INPUT_PULLUP);   // Headlight Switch
  pinMode(3, INPUT_PULLUP);   // Brake Button
  pinMode(4, INPUT_PULLUP);   // Horn Button
  
  Serial.begin(9600);
  Serial.println("--- MANUAL DASH ACTIVE ---");
}

void loop() {
  // 1. Check the Headlight Switch
  if (digitalRead(2) == LOW) {
    digitalWrite(13, HIGH);
    Serial.println("Manual: Headlights ON 🔦");
  } else {
    digitalWrite(13, LOW);
  }

  // 2. Check the Brake Pedal
  if (digitalRead(3) == LOW) {
    digitalWrite(12, HIGH);
    Serial.println("Manual: Braking! 🛑");
  } else {
    digitalWrite(12, LOW);
  }

  // 3. Check the Horn Button
  if (digitalRead(4) == LOW) {
    tone(8, 400);
    Serial.println("Manual: BEEP BEEP! 🔊");
  } else {
    noTone(8);
  }
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How the Dashboard Works

**Three-Way Logic**
- The Arduino is running three separate `if` statements inside the loop. It checks the switch, then the brake, then the horn—over and over again! 🔄🏎️

**The Physical Connection**
- Each part is wired to its own **Digital Pin**. When you flip the switch or push the button, you complete the circuit and send a **HIGH** signal to the Arduino.

**Real World Use**
- This is exactly how older cars worked! No computers, just wires and switches controlling the lights and sounds.
""")

# --- INFO BOXES ---
st.info("""
### 🔎 Dashboard Inspection
Open your [Arduino Serial Monitor](https://docs.arduino.cc) 🔎. 
1. Flip your **Headlight Switch**. Does the screen tell you they are ON? 💡
2. Mash the **Brake Pedal** and **Horn Button** at the same time. Can you make a big noise and a red flash? 🚨💥
""")

st.info("""
### 🏆 Senior Mechanic Challenges
🧪 **Challenge 1: The Mixed-Up Car.** Can you swap the code so the **Horn Button** turns on the **Headlights**? 🔄💡
🧪 **Challenge 2: High Pitched Horn.** Can you change the `tone(8, 400)` to `tone(8, 1200)` to make it sound like a tiny scooter? 🛴🔊
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Ready for Part 2: The Smart Car Upgrade?")
