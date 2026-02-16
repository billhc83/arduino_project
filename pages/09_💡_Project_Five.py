import streamlit as st
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages

# --- PAGE CONFIG ---
# (Optionally add st.set_page_config here if not in main.py)

# --- ASSETS ---
# Replace with the specific image for the new project
#circuit_layout = Image.open("graphics/YOUR_IMAGE_HERE.png")

# --- HEADER ---
st.title("🚀 Project 5 - Top Secret Mission! 🤫")

st.markdown("""
🕵️‍♂️ Secret Spy Data Beam Mission

Did you know your Arduino can talk to your computer? 🤯
It can send messages using a secret digital signal called a data beam!

Today, you are a Secret Spy 🕶️
Your mission is to build a special device that sends secret messages from your hardware straight to your screen.

Wires connect your spy gadget, and the Arduino sends the information quietly and safely — just like a real spy system.

When everything is working, you will see secret messages appear on the computer.
No talking. No shouting. Just data. 📟⚡

This mission teaches you how:

The Arduino sends information

The computer receives messages

Engineers and spies share secret data

Get ready…
Build the beam.
Watch the screen.
Crack the code! 🔐✨

""")

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
### 🔌 Spy Gear Setup

**What you need:**
- **USB Cable:** This is your "Secret Data Pipe" 🖱️
- **The Brain:** Your Arduino

**Instructions:**
1. Plug the Arduino into your computer.
2. That’s it! The USB cable does all the hard work today. 🔌✨

---
*Tip: Make sure the green light is ON so we know the spy gear has power!* 🔋

                """)

with circuit_col2:
    st.markdown("")
    # Key functional zoom component
    #hover_zoom_at_cursor(circuit_layout, width=300, height=300, zoom_factor=2.0, key="circuit_zoom_unique_key")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns(2)

with code_col1:
    st.markdown("## 💻 Code")
    st.code("""
void setup() {
  // Start the secret chat!
  Serial.begin(9600); 
  Serial.println("--- SPY PHONE ON ---");
}

void loop() {
  // Send a secret message
  Serial.println("I am a hacker! 💻");
  delay(1000); 
  
  Serial.println("Mission: Success! ✅");
  delay(1000);
}

""", language="cpp")

with code_col2:
    st.markdown("""
## 🧬 How it Works

**Serial.begin(9600)**
- This turns on the "Spy Phone" inside the Arduino so it can talk to the computer. 📞

**Serial.println()**
- This is like hitting **"Send"** on a text message. Whatever you put in the ("brackets") shows up on your screen! 💬

""")

# --- INFO BOXES ---
st.info("""
### 🕵️‍♂️ Spy Skills
💡 **Find the Secret Window:** Click the **Magnifying Glass** icon in the corner of your Arduino app. That is the **Serial Monitor**—your secret chat screen! 🔎

""")

st.info("""
### 🏆 Level Up!
🧪 **Challenge 1:** Can you change the code to say your **Name**? 

🧪 **Challenge 2:** Make the messages send **Super Fast** by changing the `delay` number to 100! ⚡

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