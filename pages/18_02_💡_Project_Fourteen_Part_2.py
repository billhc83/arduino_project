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

PAGE_TITLE       = "Project Fourteen Part 2: Code Cracker"   # shown in the assembly guide header
BANNER_IMAGE     = "graphics/code_cracker.png"            # top banner         # used in both tabs
ARDUINO_PRESET   = "cb_step1"      
# ════════════════════════════════════════════════════════════
#  INTRO MARKDOWN  — replace the triple-quoted block below
# ════════════════════════════════════════════════════════════

INTRO_MD = """
<div style="max-width: 850px; margin: auto;">

## 🕵️ Code Breaker – Phase 2

Agent, well done.

You successfully cracked the training code and unlocked the hidden message.
That means you passed the **Code Breaker Challenge**.

But the mission isn’t over.

Every year, a new group of trainees arrives at the spy academy.
Each group must complete the same challenge you just solved.

The problem is…

**someone has to build the training system.**

---

## 🛠 Your New Role

You are no longer just a trainee.

You are now part of the **training engineering team**.

Your job is to build a **new Code Breaker Machine** that the next class of trainees will use.

This machine must:

🔐 store a secret code
⌨ accept guesses from the terminal
🧠 compare each guess to the real code
📊 report how close the guess is

When a trainee finally guesses the correct code, the system will reveal the message — just like the one you unlocked.

---

## 🎯 Your Mission

You are going to rebuild the **Code Breaker System** step by step.

But this time, you understand how it works.

You will create the variables, logic, and comparisons that allow the computer to:

• read guesses
• compare letters
• count matches
• unlock the message

When you finish, the next class of trainees will face **your system**.

Let’s start building the new code breaker.

</div>
"""
WIRING_NOTES_MD = """
### 🔐 The Secret Password

##### String answer = "SPARK";

This line stores the secret code word.

The word must be inside quotes because it is a String.

A String is a piece of text made from letters.

##### Examples of Strings:

"HELLO"
"ROBOT"
"SPARK"

Our game will compare the player’s guess to this word.

If every letter matches, the player cracks the code!

### 🔢 Tracking the Score
##### int likeness = 0;

This variable keeps track of how many letters match.

The word int means integer, which is just a whole number.

Every time a letter matches the secret word, we will increase this number.

Example:

Guess:  STARK
Answer: SPARK

Matches:

S ✔
T ✖
A ✔
R ✔
K ✔

The program would count 4 matches, so:

##### likeness = 4

At the start of the game we set it to 0, because no letters have been checked yet.

### 🚦 Is the Game Finished?
##### bool solved = false;

This variable tells the program if the puzzle has been solved.

The word bool means boolean.

A boolean can only have two values:

true
false

Think of it like a switch:

false → the code is still locked
true  → the code has been cracked

When the game starts, we set this to false because the player hasn’t solved the puzzle yet.

Later in the program, when the guess matches the password, we will change it to:

solved = true

And the computer will announce:

ACCESS GRANTED! 🟢

### 🧠 What We Just Built

We created the three memory boxes that power our game:


answer ='SPARK' - This is the answer to our code

likeness = 0 - This counts the number of correct characters in the user guess

solved = False - This variable gets set to True when the guess is correct

Now the computer has everything it needs to run the code-cracking game.

Next, we’ll teach the Arduino how to listen for guesses from the player.
"""


# ════════════════════════════════════════════════════════════
#  PAGE RENDER — nothing below this line needs to change
# ════════════════════════════════════════════════════════════

page   = os.path.basename(__file__).replace(".py", "")
banner = Image.open(BANNER_IMAGE)

st.image(banner)
st.markdown(INTRO_MD, unsafe_allow_html=True)

if WIRING_NOTES_MD:
    st.markdown(WIRING_NOTES_MD)

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
