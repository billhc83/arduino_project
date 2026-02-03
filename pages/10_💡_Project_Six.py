import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---

# --- ASSETS ---
circuit_layout = Image.open("graphics/project_six_circuit.png")

# --- HEADER ---
st.title("🤿 Project 6 - The Deep Sea Explorer! 🐙")

st.markdown("""
Welcome aboard the **S.S. Arduino**! 🚢⚓ 

We are diving into the mysterious **Midnight Zone** of the ocean. Down here, the sun's rays can't reach! 🌊🌑

We will use our **Submarine Sensor** (the Photoresistor) to tell us if we are safe at the surface or if we have reached the dark, spooky home of the **Giant Squid**! 🦑✨
""")

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
### 🛠️ Setting up the Sub-Sensor

**Ship Supplies:**
- **1x Photoresistor** (The Depth Eye) 👁️🌊
- **1x 10k Resistor** (The Water-Proof Link) ⚡
- **Jumper Wires** (The Submarine Cables) 🧶

### 🧱 Breadboard layout
                
👁️ :orange[Photoresistor] (LDR)

  Leg 1: row 15 column e
  Leg 2: row 20 column e

⚡ Resistor (10k Ohm):

  Leg 1: row 20 column c (same row as LDR!)
  Leg 2: row 25 column c

🧶 3 Wires:

  Pin 5V to row 15 column a (Power to the 👁️ )
  Pin A0 to row 25 column a (Signal between LDR and Resistor)
  Pin GND to row 20 column a (Ground for the Resistor)
                """)

with circuit_col2:
    st.info("🐋 **Captain's Log:** This sensor acts like a submarine window. It sees how much 'Ocean Light' is coming through!")
    hover_zoom_at_cursor(circuit_layout, width=300, height=300, zoom_factor=2.0, key="sub_zoom")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.5,1.5])

with code_col1:
    st.markdown("## 📜 The Navigation Script")
    st.code("""
void setup() {
  // Start the sonar screen
  Serial.begin(9600);
  Serial.println("--- SUBMARINE POWER ON ---");
}

void loop() {
  // Measure the light under the sea
  int oceanLight = analogRead(A0);

  Serial.print("Light Level: ");
  Serial.println(oceanLight);

  if (oceanLight > 400) {
    Serial.println("" +
          "☀️ SURFACE: I see dolphins! 🐬");
  } 
  else {
    Serial.println(""
          "🐙 MIDNIGHT ZONE: Watch for tentacles! ✨");
  }

  delay(600); // Take a breath!
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How the Sonar Works

**analogRead(A0)**
- This reads the **Ocean Light**. It’s a number between **0 (Pitch Black)** and **1023 (Super Bright)**. 🔢🌊

**The "if" Dive-Line**
- We set the depth limit to **400**. If the light drops below this, our submarine computer knows we are in the deep, dark water! 🔦

**Serial.println()**
- This sends messages from the bottom of the ocean back to your **Computer Screen**! 🖥️📡
""")

# --- INFO BOXES ---
st.info("""
### 🔎 The Sonar Screen
Open your **Serial Monitor** 🔎. It's time to dive!
- **Mission:** Cover the sensor with your hand to "Dive" into the **Midnight Zone**. 🦑
- **Mission:** Let the light back in to "Surface" and see the **Dolphins**! 🐬
""")

st.info("""
### 🏆 Master Diver Challenges
🧪 **Challenge 1:** Can you change the code so it says **"🏴‍☠️ TREASURE FOUND!"** when it gets dark? 

🧪 **Challenge 2:** Change the delay from `600` to `100`. Now your submarine scans **Super Fast**! ⚡🚤
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to set sail for the next mission!")
