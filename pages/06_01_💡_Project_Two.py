import streamlit as st
import pandas
from data_base import save_and_unlock, save_only
from utils.utils import hover_zoom_at_cursor
from PIL import Image
from utils.utils import get_automated_pages

circuit_layout = Image.open("graphics/project_one_circuit.png")

st.title("Project Two - BLINKING BEACON💡 💡")
st.markdown("""
## Goal

🚨 Make your light blink on and off like a lighthouse! 🚨

### New ideas 💭

---

#### ⏱️ The "Wait" Command (Delay)
Imagine you are playing "Red Light, Green Light." When you hear "Red Light," you freeze! 

The Arduino uses a command called `delay()`. This tells the robot brain to stop and do **nothing** for a little bit of time. 
*   `delay(1000)` = Wait for 1 second.
*   `delay(500)` = Wait for half a second (a quick blink!).

#### 🔄 The "Forever" Loop
In your code, the `void loop()` section is like a hamster wheel. The Arduino reads the rules, gets to the bottom, and then jumps back to the top to do it all over again... forever! 

1. **High:** Turn the light ON 💡
2. **Wait:** Hold your breath! ⏱️
3. **Low:** Turn the light OFF 🌑
4. **Wait:** Hold your breath! ⏱️
5. **Jump back to step 1!**

---

### The Code Secret 🖥️

#### `digitalWrite(8, LOW);`
In Project 1, we used `HIGH` to give the light electricity. Now we use **`LOW`**. 
*   **HIGH** = Electricity flows! (Light ON)
*   **LOW** = Electricity stops! (Light OFF)

Think of it like a water tap. `HIGH` is turning the water on, and `LOW` is turning it off.

---
""")
   
st.markdown("""
## 🔌 Build the Circuit

*(If you still have Project 1 built, you are already ready!)*

###### What parts do I need?

🟦 **Arduino UNO** (The Lighthouse Keeper’s Controller!)  
This is the brain inside the lighthouse that decides when the beacon turns on and starts flashing.

⚡ **Resistor** (The Power Protector!)  
Keeps the electricity flowing safely so the beacon shines smoothly.

✨ **LED (Any Color)** (The Lighthouse Beacon!)  
This is the bright light that flashes to guide ships safely through the night.

〰️ **Jumper Wires** (The Lighthouse Wiring!)  
Carry power and signals through the lighthouse, connecting everything together.
""")

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Lets light the Blinking Beacon",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 12, column E. <br>Place the LED short leg in row 11, column E",
        "tip": "The long leg is positive — it's called the anode!",
        "highlights": [
             {"pos": (708, 175, 899, 331), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 ohm resistor in row 11, column D. <br>Place the second leg of the resistor in row 7, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (693, 324, 825, 363), "shape": "rect"},
             {"pos": (492, 154), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino GND Pin. <br>Place the other end in row 7, column E",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (375, 231, 740, 339), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin 8. <br>Place the other end in row 12, column A",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (346, 350, 844, 453), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]

tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])


with tab1:
  
  hover_zoom_at_cursor(circuit_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_one_circuit.png", steps, "Project 2: Blinking Beacon!")

  
code1, code2 = st.columns([2.5,1.5])

with code1:
        
    st.markdown("""

    ## Code 
                
                """)

    st.code("""
    void setup() {
      pinMode(8, OUTPUT); 
    }

   
    void loop() {
      digitalWrite(8, HIGH); 
      delay(500);  
      
      digitalWrite(8, LOW);  
      delay(500); 
    }
            """)

with code2:
  st.markdown("""### 🌟 Pro-Tips!

  **Delay()**
               
  In Arduino land, 1,000 equals 1 second. If you want the light to stay off for a really long time, what number would you use for 5 seconds?
    
  **The Semicolon** 🧐
    
  Don't forget the **;** at the end of your code lines! It tells the brain to move on to the next thought!!!
            
""")
st.info("""
    Remember use the copy button to grab your code and Ctrl + v to put it down in the Arduino IDE""")
st.info("🚀Try changing the number inside `delay(500)` to `delay(100)`. Does your robot blink faster or slower?")

from utils.steps import complete_step_and_continue
from utils.utils import get_automated_pages

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1,3])
with buttoncol1:
    if st.button("Next Project", type = "primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))

with buttoncol2:
    st.markdown("#### ⬅️ Click here to add the next project to the menu")