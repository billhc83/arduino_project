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


hover_zoom_at_cursor(circuit_layout, height=300, zoom_factor=2.0, key="circuit1")

st.info("👇 Need help? Click below for detailed instructions")

with st.expander("📋 Step-by-step wiring guide"):

    st.markdown("""  
                   
    ## 🧱 Breadboard layout (exact wire & part placement)

    ##### :red[Red] LED

      * Long leg: row 12 column e

      * Short leg: row 1 column e

    ##### Resistor 330 or 220 Ohms: 
      
     * row 11 column d, row 7 column d

    ##### 2 Wires:   
        
    1:  Arduino pin 8, row 12 column a

    2:  Arduino pin GND, row 7 column e

    """)
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