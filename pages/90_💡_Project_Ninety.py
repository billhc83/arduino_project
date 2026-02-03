import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
# Ensure you have an image representing the Jedi Circuit in your graphics folder
# jedi_circuit = Image.open("graphics/jedi_reaction.png")

# --- HEADER ---
st.title("⚔️ Project 6 - Jedi Reflex Training! 🧘‍♂️")

st.markdown("""
Welcome, young Padawan! To become a **Jedi Master**, you must have lightning-fast reflexes. ⚡

Today, you will build a **Jedi Reflex Tester**. You'll wait for the "Saber Light" (LED) to flash, then hit the "Force Button" as fast as you can! 

Can you move faster than a speeding starship? Let's find out! 🚀✨
""")

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
### 🛠️ Building Your Lightsaber

**Your Jedi Tools:**
- **1x LED** (The Saber Crystal) 🚨
- **1x Push Button** (The Force Trigger) 🔘
- **2x Resistors** (The Power Dampeners) ⚡
- **Jumper Wires** (The Energy Beams) 🧶

**Instructions:**
1. Connect the **LED** to **Pin 13**.
2. Connect the **Button** to **Pin 2**.
3. Use your resistors to keep the energy stable so you don't blow up the Jedi Temple! 🏛️💥
                """)

with circuit_col2:
    st.info("📸 **Hologram Projection:** Look closely at the wiring below!")
    # hover_zoom_at_cursor(jedi_circuit, width=300, height=300, zoom_factor=2.0, key="jedi_zoom_key")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns(2)

with code_col1:
    st.markdown("## 📜 The Sacred Jedi Script")
    st.code("""
int ledPin = 13;
int buttonPin = 2;
unsigned long startTime;
unsigned long reactionTime;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
  Serial.println("--- JEDI TRAINING BEGINS ---");
}

void loop() {
  Serial.println("Clear your mind... wait for the light...");
  digitalWrite(ledPin, LOW);
  
  // Wait 5 seconds + a random force delay!
  delay(5000 + random(1, 5000)); 
  
  digitalWrite(ledPin, HIGH); // SABER ON!
  startTime = millis();
  
  while (digitalRead(buttonPin) == LOW) {
    // Waiting for your lightning move...
  }
  
  reactionTime = millis() - startTime;
  Serial.print("FORCE SPEED: ");
  Serial.print(reactionTime);
  Serial.println(" milliseconds! ⚡");
  
  delay(3000); // Rest before next round
}
""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How the Force Works

**random(1, 5000)**
- This creates a **surprise delay**! You never know exactly when the light will turn on. A Jedi must always be ready! 🎲

**millis()**
- This is the Arduino’s **Super Stopwatch**. It counts time in tiny milliseconds to see how fast you are! ⏱️

**while()**
- This makes the code **freeze** and wait until you finally bash that button! 🧊
""")

# --- INFO BOXES ---
st.info("""
### 🔍 Reading the Holocron
Open your **Serial Monitor** (the magnifying glass 🔎). This is where the Master will tell you your **Force Speed** score! 
- **500ms:** Youngling 👶
- **250ms:** Jedi Knight ⚔️
- **Under 200ms:** Grand Master Yoda!  Yoda 🟢
""")

st.info("""
### 🏆 Master Challenges!
🧪 **Challenge 1:** Can you make the LED **blink** 3 times fast before the game starts? 
🧪 **Challenge 2:** Change the code so that if the score is under 200, it says **"THE FORCE IS STRONG!"** 💪
""")

# --- NAVIGATION ---
pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to complete your Jedi Trials!")
