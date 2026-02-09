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

# --- CIRCUIT SECTION ---
circuit_col1, circuit_col2 = st.columns(2, vertical_alignment="center")

with circuit_col1:
    st.markdown("""
## 🧱 The Vault Blueprint
*We are using our **Magic 5** coordinates and the **- Rail** to keep our spy gear organized!*

##### 🔑 :green[Key Card 1] (Switch)
*   **Center Pin:** row 5 column e
*   **Side Pin:** row 4 column e

##### 🔑 :green[Key Card 2] (Switch)
*   **Center Pin:** row 15 column e
*   **Side Pin:** row 14 column e

##### 💡 :red[Vault Status Light] (LED)
*   **Long leg:** row 25 column e
*   **Short leg:** row 22 column e

##### ⚡ Resistor (220 Ohm - Red, Red, Brown): 
*   **Leg 1:** row 22 column c
*   **Leg 2:** **- rail** (Ground Rail)

---

## 🧶 Wiring the Console

1.  **Pin GND** ➡️ **- rail / Ground Rail** (The Main Drain) 🚰
2.  **Pin 5V** ➡️  **+ rail / Power Rail** 5v Power
    **+ rail** ➡️  **row 4 column a** (Power for Key 1)
3.  **+ rail** ➡️ **row 14 column a** (Power for Key 2)
4.  **Pin 2** ➡️ **row 5 column a** (Signal for Key 1)
5.  **Pin 3** ➡️ **row 15 column a** (Signal for Key 2)
6.  **Pin 13** ➡️ **row 25 column a** (Power for Vault Light)
                """)

with circuit_col2:
    st.info("""
🧠 **Spy Logic Secret:**
We are using **Variables** to store a "Status." 
- `boltA = 0` means the first lock is stuck.
- `boltA = 1` means the first lock is open! 🔓

The computer checks these "Status Pockets" to see if it's safe to open the door.
""")
    hover_zoom_at_cursor(spy_vault_layout, width=300, height=300, zoom_factor=2.0, key="vault_zoom")

# --- CODE SECTION ---
code_col1, code_col2 = st.columns([2.75,1.25])

with code_col1:
    st.markdown("## 📜 The Security Script")
    st.code("""
// 🔐 Our Security Lock Variables
int LockA = 0; 
int LockB = 0;

void setup() {
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.println("--- VAULT SYSTEM ARMED ---");
}

void loop() {
  // 1. Read the Key Cards and update our Variables!
  LockA = digitalRead(2);
  LockB = digitalRead(3);

  // 2. The Logic: Check if BOTH bolts are Unlocked (1)
  if (LockA == 1 && LockB == 1) {
    digitalWrite(13, HIGH);
    Serial.println("🔓 ACCESS GRANTED: Vault Open!");
  } 
  else {
    digitalWrite(13, LOW);
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
