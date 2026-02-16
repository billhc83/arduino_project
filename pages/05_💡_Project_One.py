import streamlit as st
import pandas
from data_base import save_and_unlock, save_only
from PIL import Image
from utils.utils import hover_zoom_at_cursor
from utils.utils import complete_step_and_continue, get_automated_pages

circuit_layout = Image.open("graphics/project_one_circuit.png")

st.title("Project One - Lights On! 💡 💡 💡")
st.divider()
st.markdown("""

## Goal

🚨Make a tiny light turn on using the Arduino.🚨

### New ideas  💭

---
#### Pins
            
Imagine your Arduino is a tiny robot brain, and the pins are its arms, ears, and mouth! 🤖
            
Without pins, the brain would just sit there thinking. The pins allow it to reach out and touch the world. Here is how they work:

#### 👂 The "Ear" Pins (Inputs)
Some pins are for listening. When you plug a button or a sensor into these, the Arduino can "hear" what’s happening:

❓ "Is someone pressing my button?"

❓ "Is it dark in this room?"

❓ "Is there a cat nearby?"

#### 🗣️ The "Mouth" Pins (Outputs)
Other pins are for talking to your toys. When the Arduino wants to do something, it sends a tiny zap of electricity through these pins:

💡 "Turn on the light!" (Makes a light glow)

⚙️ "Spin the wheel!" (Makes a motor turn)

🎵 "Beep-beep!" (Makes a buzzer make noise)

---
### OUTPUT
            
#### What can an Output do?
✨ Light up: It can turn on a tiny light to show a bright color.
            
⚙️ Move: It can make a motor spin a wheel or wave a robot arm.
            
🎵 Make Noise: It can make a buzzer go "Beep!" or play a happy tune.
            

#### Two ways to "talk":
1️⃣ On or Off: Like a light switch. The Arduino says "YES, turn on!" or "NO, stay off!" 💡
            
2️⃣ A Little Bit: Like a volume knob. The Arduino can make a light look dim or make a motor spin slowly instead of fast. 🔉

---
#### First code 🖥️

Imagine your Arduino code is the Rule Book for your tiny robot brain! 📖🤖
            
Without code, the brain wouldn't know what to do with its ears or its mouth. The code tells the Arduino exactly how to behave. Here is how it works:

📝 The "Instructions" (The Sketch)
Arduino code is called a "Sketch." It is like a recipe or a list of chores that the robot brain follows in a specific order:

📋 First, I gather my tools. (Setting up the pins)

📋 Next, I do my work. (Turning on lights or moving motors)

📋 Then, I do it all over again! (Repeating the rules)
            
            """)
st.title("""
         
  🔌 Build the circuit

    ###### What parts do I need?
                
    🟦 Arduino UNO (It’s the computer brain!)
                
    ⚡ Resistor (It’s the electricity speed-bump!)

    ✨ Any color LED (It’s the tiny glowing light!)

    〰️ Wires (They are the robot's veins and nerves!)
   """)
hover_zoom_at_cursor(circuit_layout, zoom_factor=2.0, key="circuit1")
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
    }
            """)
    
with code2:
     
    st.markdown("""
    ### 🧩 What this code means

    setup() → runs once when Arduino wakes up 🌅

    pinMode(8, OUTPUT) → pin 8 sends power out 🗲

    loop() → runs forever 🔁

    digitalWrite(8, HIGH) → turns the LED on 💡
            """)
st.info("""
## How to Move Your Code🔌
            
#### Copy it: 📋 

Find the code box and click the Copy button. Now the computer is holding the words for you!

#### Open Arduino: ♾️ 

Open the Arduino app on your computer. It is the blue circle icon.

#### Clean the page: 🧹 

Click on the white page. Hold the Ctrl key and tap A, then hit Backspace. Now the page is empty!

#### Paste it: 📥
Click the empty white page. Hold the Ctrl key and tap V. Your code will pop up!

#### Send it: 🚀 
 
Plug your board into the computer with the cable. Click the Arrow button (➔) at the top. When it says "Done," your code is ready!
""")

st.write("""
The Magic Blue Brain: 🟦 "If your light isn't turning on, check the green light on the Arduino board itself. If that's not on, your 'Brain' isn't getting power! Check your USB cable."

Color Matching: 🌈 "Wires come in different colors, but inside, they are all the same! You can use a yellow wire for a red light, and it will still work. It's like wearing a blue shirt or a red shirt—you're still you!
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