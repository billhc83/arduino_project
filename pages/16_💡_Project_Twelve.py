import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT

st.markdown("""
# ✈️ Project – Engine Start Sequence

## 🛫 Welcome to the Flight Simulator

Today is a big day.

You are sitting in the pilot seat of the simulator. 🧑‍✈️  
I’m still here with you — but your hands are on the controls.

Up until now, you’ve learned how switches work.  
You’ve learned how buttons work.  
You’ve turned lights on.  
You’ve made sounds happen.

Today…

You decide when the engine starts. 🔥

---

## 🎯 Your Mission

This aircraft has:

- 🔘 An **Arm Switch**
- 🔴 An **Engage Button**
- 💡 An **Engine Light**
- 🔊 An **Engine Sound**

The aircraft follows very clear rules:

- If the Arm Switch is OFF → everything is OFF.
- If the Arm Switch is ON → the aircraft is ready.
- If the system is ready and you press the Engage Button → the engine starts.
- The engine keeps running until you turn the Arm Switch OFF.

Your job is to build the code that makes this happen.

---

## 🧠 Think Like a Pilot

Before you start building, look at the circuit diagram.

Ask yourself:

- Which part turns the system ON?
- Which part starts the engine?
- Which parts show that the engine is running?

You are not copying code today.

You are building the rules. ✨

---

## 🛠️ When You Test It

Try this:

1. Leave the switch OFF. Press the button. What happens?
2. Turn the switch ON. Does the light come on?
3. Press the button. Does the engine start?
4. Turn the switch OFF. Does everything shut down?

If it works exactly like that…

You did it. 🛫

---

## 🌟 What Just Happened?

You didn’t just turn something on.

You told the aircraft **when it is allowed to turn on.**

That’s real control.

From this point forward, you are not just following instructions.

You are building systems. 💪
""")

st.markdown("""
## 🔎 How to Read the Wiring Diagram

Now that you know your mission, let’s look at the wiring diagram. 🕵️‍♂️  
Don’t worry, it looks busy — we just need to notice a few things.

Follow these steps to extract the information you need:

---

### 1️⃣ Find the Parts
Look at the diagram. Can you spot:

- 🔘 The **Switch**
- 🔴 The **Button**
- 💡 The **Engine Light**
- 🔊 The **Buzzer**
- 🖥️ The **Arduino**

That’s all we need to identify right now.

---

### 2️⃣ Follow the Wires
Trace each wire with your eyes:

- Where does this wire start?  
- Where does it end?  

No need to think about voltage or current — just **start → end**.

---

### 3️⃣ Match Each Part to a Pin
Now let’s see which pins matter:

- Which pin is the switch connected to?  
- Which pin is the button connected to?  
- Which pin controls the light?  
- Which pin controls the buzzer?  

This is the key step — this tells you **what to control in your code**.

---

### 4️⃣ Ask: Who Controls Who?
Look carefully:

- Does the switch connect directly to the buzzer?  
- Or does it connect to the Arduino?  

Notice: **everything talks to the Arduino**.  
The Arduino decides what happens — that’s where your logic lives.

---

### ✅ Remember
Don’t rush.  
Your job is not to build yet — your job is to **notice and understand**.  

When you know where everything connects, you know exactly what your code must control. 🚀
""")

st.set_page_config(layout= "wide")
st.title("Build Your Sketch")

arduino_block_coder(
    preset = 'engine_start',
    drawer_content= DRAWER_CONTENT.get("engine_start") 
)
