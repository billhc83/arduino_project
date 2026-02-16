import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---

# --- ASSETS ---
circuit_layout = Image.open("graphics/project_six_circuit.png")

# --- HEADER ---
st.title("🤿 Project 6 - The Deep Sea Explorer! 🐙")

st.markdown("""
🚢 Submarine Light Sensor Mission

Welcome aboard the S.S. Arduino! 🚢⚓
Today, you are part of a brave submarine crew going deep into the ocean.

We are diving into the Midnight Zone, a dark place far below the surface. 🌊🌑
Down here, sunlight cannot reach, and it gets darker and darker as we go.

Our submarine has a special tool called a Submarine Sensor 👁️‍🗨️
This sensor can “see” how bright or dark it is around us.

If it is bright, we know we are near the surface and safe.
If it is dark, we know we are deep in the ocean… maybe even near the spooky home of the Giant Squid! 🦑✨

Your mission is to:

Watch the light sensor

Read the data on the screen

Discover how deep the submarine has traveled

Lights on, crew!
Let’s dive! 🌊⚓
""")
st.markdown("""
## 🔌 Build the Circuit

###### What parts do I need?

🟦 **Arduino UNO** (The Submarine’s Brain!)  
This is the captain of the submarine! It thinks, makes decisions, and reports light levels back to mission control using the serial monitor.

〰️ **Jumper Wires** (The Submarine’s Nerve Cables!)  
These carry messages and power around the submarine so all the parts can talk to each other.

👁️‍🗨️ **Photoresistor (LDR)** (The Submarine’s Periscope Eye!)  
This eye looks around underwater and tells the submarine how bright it is outside.

⚡ **Resistor** (The Current Controller!)  
Slows the electricity down so the periscope eye gives smooth, accurate readings instead of going wild!
""")

hover_zoom_at_cursor(circuit_layout, height=300, zoom_factor=2.0, key="sub_zoom")
st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):
    st.markdown("""
### 🛠️ Setting up the Sub-Sensor

**Ship Supplies:**
- **1x Photoresistor** (The Depth Eye) 👁️🌊
- **1x 10k Resistor** (The Water-Proof Link) ⚡
- **Jumper Wires** (The Submarine Cables) 🧶

### 🧱 Breadboard layout
                
👁️ :orange[Photoresistor] (LDR)

  Leg 1: row 15 column f
  Leg 2: row 19 column f

⚡ Resistor (10k Ohm):

  Leg 1: row 15 column h (same row as LDR!)
  Leg 2: row 11 column h

🧶 3 Wires:

  Arduino Pin 5V to row 18 column j (Power to the 👁️ )
                
  Arduino Pin A0 to row 15 column j (Signal between LDR and Resistor)
                
  Arduino Pin GND to row 11 column j (Ground for the Resistor)
                """)

st.info("🐋 **Captain's Log:** This sensor acts like a submarine window. It sees how much 'Ocean Light' is coming through!")
    

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
    Serial.println(""
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
