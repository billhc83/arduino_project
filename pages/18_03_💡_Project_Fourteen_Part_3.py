import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
from components.contents import DRAWER_CONTENT
from PIL import Image
from utils.utils import hover_zoom_at_cursor, complete_step_and_continue, get_automated_pages
from utils.assembly_guide import assembly_guide
from utils.step_builder import build_step, intro_step, rect, circle, line

st.set_page_config(layout="wide")

# ════════════════════════════════════════════════════════════
#  PAGE IDENTITY  — edit these 4 lines for every new project
# ════════════════════════════════════════════════════════════

PAGE_TITLE       = "Project Fourteen Part 3: Code Cracker"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/code_cracker.png"            # top banner         # used in both tabs
ARDUINO_PRESET   = "cb_step2"      
# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">
## 🕵️ Spy Training – Phase 3

Agent, continue building the new **Code Breaker System**.

The next group of trainees will depend on this machine, so every part must be installed correctly.

As before, the system needs:

💻 a connection to the training terminal
🔐 a cipher system to protect the hidden message

---

## 💻 Connecting the Training Terminal

The Code Breaker communicates through the **training terminal**.

This is where trainees will enter guesses and receive feedback from the system.

To activate this connection, we use:

```id="7k2xq1"
Serial.begin(9600);
```

This allows the computer to send and receive messages.

---

## 🔐 Cipher Values from Another Agent

The cipher system used in this challenge was created by another agent during a previous training cycle.

They left behind a set of cipher values for you to install.

These values are required for the system to decode the hidden message when the correct password is entered.

---

## ⚠️ An Unusual Discovery

While reviewing the cipher data, training command noticed something unexpected.

The previous agent may have left **additional encoded information** inside the system.

No one has been able to fully decode it yet.

Before continuing, you have access to a **cipher test terminal** below.

This tool lets you experiment with the cipher system and observe how the encoded data behaves.

Take a moment to explore.

Do you notice anything unusual?

---"""
MISSION = """
## 🎯 Your Mission

Review the cipher values we put into the system and continue building the Code Breaker.


## 🕵️ Spy Training – System Output Setup

Agent, we have now installed the **display system** for the Code Breaker.

This is what the next trainees will see when they run your program.

Let’s break it into sections.

---

## 💻 1. Starting the Terminal

```cpp id="a1s9d2"
Serial.begin(9600);
```

### 🔹 What the trainee sees:

```id="b2k8q1"
[ TERMINAL CONNECTED ]
```

### 🧠 What this does:

This line starts communication between the computer and the **training terminal**.

Without it, nothing would appear on the screen.

---

## 🧾 2. Displaying the Title

```cpp id="c3m7x4"
Serial.println("================================");
Serial.println("     C O D E  B R E A K E R    ");
Serial.println("================================");
```

### 🔹 What the trainee sees:

```id="d4p9w6"
================================
     C O D E  B R E A K E R    
================================
```

### 🧠 What this does:

This creates a **header** so the trainee knows what program they are using.

It makes the system feel like a real machine.

---

## 📜 3. Showing the Instructions

```cpp id="e5r2t8"
Serial.println("Find the hidden 5-letter word.");
Serial.println("");
```

### 🔹 What the trainee sees:

```id="f6y3u1"
Find the hidden 5-letter word.
```

### 🧠 What this does:

This tells the trainee what their goal is.

The empty line (`""`) adds spacing to make the screen easier to read.

---

## 🔍 4. Displaying the Cipher Grid

```cpp id="g7h4j2"
Serial.println("X K Q S P A R K M Z");
Serial.println("B R T F L A M E Q X");
Serial.println("P Q S P A R K T Z R");
Serial.println("W Z X B R A N D T P");
Serial.println("S P A R K X Q Z B M");
Serial.println("T R X N G L O W K B");
Serial.println("Q Z B S P A R K X T");
Serial.println("M X T R B L A Z E P");
Serial.println("B T Z X Q M R N V K");
Serial.println("P N V Q Z B X T M R");
Serial.println("");
```

### 🔹 What the trainee sees:

```id="h8k5l3"
X K Q S P A R K M Z
B R T F L A M E Q X
P Q S P A R K T Z R
W Z X B R A N D T P
S P A R K X Q Z B M
T R X N G L O W K B
Q Z B S P A R K X T
M X T R B L A Z E P
B T Z X Q M R N V K
P N V Q Z B X T M R
```

### 🧠 What this does:

This is the **cipher grid**.

The hidden word is placed inside this grid, but it is mixed in with other letters.

The trainee must **search for patterns** and use guesses to find the correct word.

---

## ⌨️ 5. Prompting the User

```cpp id="i9n6b4"
Serial.println("Enter your guess:");
```

### 🔹 What the trainee sees:

```id="j0v7c5"
Enter your guess:
```

### 🧠 What this does:

This tells the trainee it’s time to interact with the system.

They will type their guess into the terminal.

---

## 🎯 Why This Matters

You are building the **experience** for the next trainee.

This part of the program:

• introduces the challenge
• displays the puzzle
• tells the user what to do

In the next steps, you will build the logic that **responds to their guesses**.

Soon, your system won’t just display the challenge…

it will **run it**.



In the next steps, you will add the logic that allows the machine to:

• listen for guesses

• compare letters

• count matching characters

• unlock the message

Stay alert, Agent.

There may be more hidden in this system than expected.  

"""
# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)
from components.code_breaker import serial_monitor
serial_monitor(
    answer = 'CHASER',
    cipher_lines= [
    'TRSTARENM',
    'PLSPAREKI',
    'BVSHAPELO',
    'GHSHARPXW',
    'WECHARTOP',
    'QWCHASERT',
    'MKPHASEUY',
    'LKJHGFRDSA',
    'MNBVCXZPOI',
    'QWERTYUIOP'],
    message = [
"DECRYPTION COMPLETE",
"",
"IF YOU ARE READING THIS,",
"YOU HAVE PASSED THE FIRST TEST.",
"",
"I WAS THE LAST AGENT",
"TO WORK ON THIS SYSTEM.",
"",
"THE TRAINING PROGRAM IS REAL,",
"BUT NOT EVERYTHING HERE",
"IS WHAT IT SEEMS.",
"",
"THE CODE YOU JUST BROKE",
"WAS BUILT BY ANOTHER TRAINEE.",
"",
"NOW IT IS YOUR TURN.",
"",
"BUILD A NEW CODE BREAKER",
"FOR THE NEXT GROUP.",
"",
"CHOOSE A SECRET WORD.",
"CREATE THE MATCH SYSTEM.",
"HIDE A MESSAGE INSIDE.",
"",
"MAKE IT CHALLENGING.",
"",
"SOMEONE WILL TRY TO BREAK",
"THE SYSTEM YOU BUILD."]) # type: ignore

st.markdown(MISSION, unsafe_allow_html=True)

arduino_block_coder(
    preset=ARDUINO_PRESET,
    drawer_content=DRAWER_CONTENT.get(ARDUINO_PRESET),
    username=st.session_state.get("user_id"),
    page=page,
    height=620,
)

pages_map = get_automated_pages("pages")
buttoncol1, buttoncol2 = st.columns([1, 3])
with buttoncol1:
    if st.button("Next Step", type="primary"):
        complete_step_and_continue(pages_map, current_page_title=st.session_state.get("current_page"))
with buttoncol2:
    st.markdown("#### ⬅️ Click here to continue to the next step!")