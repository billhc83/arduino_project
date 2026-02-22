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
Welcome back to the Garage, Master Mechanic! 🛠️
The tools are lined up. The engine is quiet. The dashboard is waiting for you.

Before we turn this into a Smart Car, we have to build it the old-school way — manual control.

That means no computers making decisions yet.
No automatic lights.
No automatic braking.

Right now, you are the driver and the engineer.

In this project, you will build:

💡 A Headlight Switch – Flip it on and the road lights up.
🛑 A Brake Pedal – Press it and the brake light shines bright.
📢 A Horn Button – Push it and let everyone hear that engine roar!

Every button you press sends a signal.
Every signal controls a part of the car.

The super car does exactly what your fingers tell it to do — nothing more, nothing less.

This is how real engineers start:

One control

One action

One clear result

Hands on the controls, Mechanic.
Let’s build the dash. 🏁✨
""")

from utils.assembly_guide import assembly_guide, coordinate_picker

steps = [
    {
        "instruction": "Lets Light This Car UP!!!",
        "tip": "Press the next button for a step by step guide",  
    },
    {
        "instruction": "Place the LED long leg in row 1, column E. <br>Place the LED short leg in row 2, column E",
        "tip": "This is the brake light",
        "highlights": [
             {"pos": (541, 219, 671, 372), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place the LED long leg in row 30, column E. <br>Place the LED short leg in row 29, column E",
        "tip": "This is the head light",
        "highlights": [
             {"pos": (1100, 202, 1234, 364), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 11, column D. <br>Place the second leg of the resistor in row 7, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (608, 337, 726, 403), "shape": "rect"},
             {"pos": (734, 49), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 2, column D. <br>Place the second leg of the resistor in row 6, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (608, 337, 726, 403), "shape": "rect"},
             {"pos": (734, 49), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one leg of the 220 Ohm resistor in row 29, column D. <br>Place the second leg of the resistor in row 25, column D",
        "tip": "The resistor slows down the electricity",
        "highlights": [
             {"pos": (1053, 350, 1167, 397), "shape": "rect"},
             {"pos": (1035, 41), "shape": "circle", "radius": 60}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the button onto the breadboard. <br>There are 4 legs on the button, each one goes to its own spot on the breadboard. <br>Button leg → row 10 column E <br>Button leg → row 8 column E <br>Button leg → row 10 column F <br>Button leg → row 8 column F",
        "tip": "The button will let us control the brake light",
        "highlights": [
             {"pos": (707, 280, 813, 366), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the button onto the breadboard. <br>There are 4 legs on the button, each one goes to its own spot on the breadboard. <br>Button leg → row 14 column E <br>Button leg → row 12 column E <br>Button leg → row 14 column F <br>Button leg → row 12 column F",
        "tip": "The button will let us control the horn",
        "highlights": [
             {"pos": (809, 282, 886, 372), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },   
    {
        "instruction": "Place the headlight switch on the breadboard.<br>The centre pin goes in row 23 column E <br>The side pin goes in row 24 column E",
        "tip": "The switch turns on the headlight",
        "highlights": [
             {"pos": (982, 266, 1087, 374), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place the buzzer long leg in row 18, column E. <br>Place the buzzer short leg in row 18, column F",
        "tip": "This is the horn",
        "highlights": [
             {"pos": (939, 327), "shape": "circle", "radius": 60}
             ],
          "labels": [
        {
            "text": "Long Leg",
            "offset_x": -65,
            "offset_y": 70,
            "font_size": 24,
        },
        {
            "text": "Short Leg",
            "offset_x": -65,
            "offset_y": -90,
            "font_size": 24,
        }
    ],
        "greyout": True,   # dims everything outside the highlights
        #"label": "LED +",
    },
    {
        "instruction": "Place one end of the wire in the Arduino Pin GND. <br>Place the other end in the negative / - rail",
        "tip": "Ground wires help complete our circuit loop",
        "highlights": [
             {"pos": (333, 114, 557, 296), "shape": "rect"},
             {"pos": (524, 114, 652, 170), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 13. <br>Place the other end in row 30 column A",
        "tip": "This wire sends power to our headlight",
        "highlights": [
             {"pos": (337, 84, 569, 311), "shape": "rect"},
             {"pos": (337, 51, 1244, 119), "shape": "rect"},
             {"pos": (1211, 67, 1244, 454), "shape": "rect"},
             {"pos": (1146, 413, 1240, 454), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 12. <br>Place the other end in row 1 column D",
        "tip": "This wire powers our brake light",
        "highlights": [
             {"pos": (344, 297, 636, 387), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 8. <br>Place the other end in row 18 column C",
        "tip": "This wire send power to our horn",
        "highlights": [
             {"pos": (354, 372, 965, 413), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 4. <br>Place the other end in row 12 column B",
        "tip": "This is the signal for our horn button",
        "highlights": [
             {"pos": (563, 407, 841, 423), "shape": "rect"},
             {"pos": (352, 407, 606, 491), "shape": "rect"}
             
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 3. <br>Place the other end in row 8 column A",
        "tip": "This is the signal for our brake light button",
        "highlights": [
             {"pos": (730, 419, 770, 540), "shape": "rect"},
             {"pos": (518, 520, 764, 540), "shape": "rect"},
             {"pos": (520, 530), "shape": "circle", "radius": 10},
              {"pos": (510, 528), "shape": "circle", "radius": 10},
              {"pos": (500, 526), "shape": "circle", "radius": 10},
              {"pos": (490, 524), "shape": "circle", "radius": 10},
              {"pos": (480, 522), "shape": "circle", "radius": 10},
              {"pos": (470, 520), "shape": "circle", "radius": 10},
              {"pos": (460, 518), "shape": "circle", "radius": 10},
              {"pos": (450, 516), "shape": "circle", "radius": 10},
              {"pos": (440, 514), "shape": "circle", "radius": 10},
              {"pos": (430, 512), "shape": "circle", "radius": 10},
              {"pos": (420, 510), "shape": "circle", "radius": 10},
              {"pos": (410, 508), "shape": "circle", "radius": 10},
              {"pos": (400, 506), "shape": "circle", "radius": 10},
              {"pos": (390, 504), "shape": "circle", "radius": 10},
              {"pos": (380, 505), "shape": "circle", "radius": 10},
              {"pos": (370, 502), "shape": "circle", "radius": 10}

             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in Arduino Pin 2. <br>Place the other end in row 23 column A",
        "tip": "This is the signal for our headlight switch",
        "highlights": [
             {"pos": (1006, 413, 1047, 559), "shape": "rect"},
             {"pos": (500, 542, 1047, 559), "shape": "rect"},
             {"pos": (520, 550), "shape": "circle", "radius": 10},
              {"pos": (510, 548), "shape": "circle", "radius": 10},
              {"pos": (500, 546), "shape": "circle", "radius": 10},
              {"pos": (490, 544), "shape": "circle", "radius": 10},
              {"pos": (480, 542), "shape": "circle", "radius": 10},
              {"pos": (470, 540), "shape": "circle", "radius": 10},
              {"pos": (460, 538), "shape": "circle", "radius": 10},
              {"pos": (450, 536), "shape": "circle", "radius": 10},
              {"pos": (440, 534), "shape": "circle", "radius": 10},
              {"pos": (430, 532), "shape": "circle", "radius": 10},
              {"pos": (420, 530), "shape": "circle", "radius": 10},
              {"pos": (410, 528), "shape": "circle", "radius": 10},
              {"pos": (400, 526), "shape": "circle", "radius": 10},
              {"pos": (390, 524), "shape": "circle", "radius": 10},
              {"pos": (380, 525), "shape": "circle", "radius": 10},
              {"pos": (370, 522), "shape": "circle", "radius": 10}

             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in the Arduino GND Pin <br>Place the other end in the negative / - rail",
        "tip": "This wire completes our loop for the swtich",
        "highlights": [
             {"pos": (1136, 474, 1181, 603), "shape": "rect"},
             {"pos": (390, 562, 1179, 603), "shape": "rect"},
             {"pos": (8, 350, 468, 603), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 6 column A <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (671, 411, 730, 505), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 10 column J <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (752, 123, 819, 243), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 14 column J <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (839, 119, 894, 254), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 18 column J <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (900, 127, 976, 241), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 24 column A <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (1030, 415, 1108, 507), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    },
    {
        "instruction": "Place one end of the wire in row 25 column C <br>Place the other end in negative/ - rail",
        "tip": "The wires are like roads for electricity",
        "highlights": [
             {"pos": (1073, 389, 1136, 503), "shape": "rect"}
             ],    # pixel coords on your image
        "greyout": True,   # dims everything outside the highlights
    }]
tab1, tab2 = st.tabs(["**📋 Quick Overview**", "**🔧 Step-by-Step**"])  

with tab1:
  
  hover_zoom_at_cursor(manual_car_layout, zoom_factor=2.0, key="circuit1")

with tab2:

  assembly_guide("graphics/project_eleven_circuit.png", steps, "Project 11: The Manual Super Car (Part 1)")

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
