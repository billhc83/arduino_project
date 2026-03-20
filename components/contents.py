from PIL import Image
import base64
from pathlib import Path

def img_to_base64(path):
    data = Path(path).read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = Path(path).suffix.lstrip(".")  # png, jpg, etc.
    return f"data:image/{ext};base64,{b64}"

from utils.utils import hover_zoom_html
engine_controls = hover_zoom_html("graphics/project_twelve_circuit.png", height=200, key="engine_schematic")
patrol_lights = hover_zoom_html("graphics/project_thirteen_circuit.png", height= 200, key="patrol_schematic" )

DRAWER_CONTENT = {
    "engine_start": {
        "title": "📘 Engine Start Guide",
        "tip": "Build the rules that control when the engine is allowed to run.",
        "tabs": {
            "mission": {
                "label": "🧠 Mission",
                "image_html": engine_controls,
                "content": """
    <h3>You are building an engine system with rules:</h3>
    <p>
    - The switch controls the whole system.
    - The button starts the engine.
    - The engine keeps running until the switch turns OFF.
    - If the switch is OFF, nothing runs.
    - The "If" blocks are filled in already no need to change them.

    Your job is to build these rules using blocks.
    </p>
"""
            },
            "wiring": {
                "label": "🔌 Wiring",
                "content": """
<b>Match each part to its pin:</b>
<p>

🔘 Arm Switch → Pin 9  
🔴 Engage Button → Pin 7  
💡 Engine Light → Pin 2  
🔊 Engine Buzzer → Pin 5  

Find the part in the diagram.  
Follow the wire.  
Match it to the pin.

</p>
"""
            },
            "logic": {
                "label": "🧩 Logic",
                "content": """
<b>🔘 Important Button Rule</b>
<p>
Look at the wiring diagram.

If the button connects to GND,
choose:

INPUT_PULLUP

That’s how this wiring style works.

<b>Understanding The "If" statements:</b>

The Arduino sees <b>HIGH</b> when the switch is <b>off</b> or the button is <b>not pressed</b>

The Arduino sees <b>LOW</b> when the switch is <b>on</b> or the button is <b>pressed</b>

So when we write <b>If digitalRead(switch or button pin) equals LOW</b>

The Arduino is checking to see if the switch is on or the button is pressed

<b>Think about the flow:</b>

IF switch is ON  
    Light ON
    IF button pressed  
        engine ON

IF switch is OFF (else)
    everything OFF  


Remember:
The switch is the boss.
</p>
"""
            }
        }
    },

    "codebreaker": [

    {
        "title": "Step 1 — The Variables 📦",
        "tip": "Set up your agent’s memory for the mission.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>Every agent needs memory for the mission. These memory containers are called variables.</p><p>We prepare three key pieces of memory for the code-breaking device:</p><ul><li>🔐 <b>answer</b> → the secret 5-letter code trainees must find. This is text, so it must be in quotes.</li><li>🔢 <b>likeness</b> → how many letters match the secret code. Start at 0.</li><li>🚪 <b>solved</b> → whether the code has been cracked. Start as false.</li></ul><p>Without these, the system won’t remember anything the trainee does.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Create a container called <b>answer</b> for the secret word \"SPARK\". Write the word in quotes because it is text.</p><p>2. Create a container called <b>likeness</b> to count correct letters. Start it at 0.</p><p>3. Create a container called <b>solved</b> to track if the code is cracked. Set it to false at the beginning.</p><p>These are the foundations for your agent’s memory. Make sure you name the containers exactly as above so the system can use them later.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>Think of these like secret pockets in an agent’s backpack. Each pocket has a purpose: one stores the code, one counts matches, one knows if the mission is complete. Without them, the agent can’t do the mission.</p>"
            }
        }
    },

    {
        "title": "Step 2 — Serial Begin 💻",
        "tip": "Activate communication with HQ (the screen).",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>Your device needs a way to talk to the trainee. This communication line is opened with <b>Serial.begin(9600)</b>.</p><p>Once open, the system can display the coded message grid the trainee will analyze.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Go to the setup section, which runs once at the start.</p><p>2. Turn on the communication line with the correct speed: 9600.</p><p>3. Display the code grid and instructions. Include lines that show the letters trainees will analyze, the instructions to guess, and a prompt to enter guesses.</p><p>Make sure this is all in the setup so it only runs once. This lets the trainee see the mission briefing clearly.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>Without opening this line, your agent stays silent. The trainee won’t see anything, even if all the other parts are working perfectly.</p>"
            }
        }
    },

    {
        "title": "Step 3 — Listen for Input ⌨️",
        "tip": "Wait for the trainee to send a guess from HQ.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>The device must wait until a trainee types a guess. We don’t want to read nothing.</p><p>Checking if new data is available ensures the system only acts when the trainee is ready.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Check if the communication line has new data.</p><p>2. Only proceed if there is data waiting — this opens the door for processing the guess.</p><p>This is like checking a secure mailbox: the agent only looks when a message is inside.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>Think of it as a secure lock. If you try to open it with nothing inside, nothing happens. The agent must wait for the trainee’s input to continue the mission.</p>"
            }
        }
    },

    {
        "title": "Step 4 — Read the Guess 📓",
        "tip": "Capture the trainee’s guess and clean it for analysis.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>Once input is detected, we store it in a variable called <b>guess</b>.</p><p>Cleaning the input ensures accuracy:</p><ul><li>✂️ Remove extra spaces at the start and end.</li><li>🔠 Convert all letters to uppercase so they match the secret code format.</li></ul>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Create a container called <b>guess</b>.</p><p>2. Take the trainee’s typed input and store it in <b>guess</b>.</p><p>3. Remove any extra spaces at the beginning or end.</p><p>4. Convert all letters to uppercase so the system can compare fairly with the secret code.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>This step prevents small mistakes like typing ' spark ' or 'Spark' from causing the system to fail. Every input is cleaned before checking.</p>"
            }
        }
    },

    {
        "title": "Step 5 — Reset the Score 🔄",
        "tip": "Prepare the device for a fresh comparison.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>Before checking the new guess, reset the <b>likeness</b> counter to 0.</p><p>This ensures each guess is measured independently.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Inside the input check, set <b>likeness</b> to 0 before counting matches.</p><p>2. Make sure this happens every time a new guess is entered.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>If we forget this, old scores would add to new ones, giving incorrect results. Resetting ensures fairness for each trainee.</p>"
            }
        }
    },

    {
        "title": "Step 6 — The Letter Checker 🔍",
        "tip": "Compare each letter in the guess with the secret code.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>We compare the guess to the answer letter by letter.</p><p>If a letter is correct and in the right position, it counts as a match. This increases <b>likeness</b>. We have provided this code so when you are ready continue to the next step.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Look at each of the 5 letters in the guess.</p><p>2. Compare each letter with the corresponding letter in the secret code.</p><p>3. Every time a letter matches exactly, add 1 to <b>likeness</b>.</p><p>4. This will give a score from 0 to 5 that shows how close the guess is.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>Correct letter AND correct position = point earned. This is the core of the training challenge.</p>"
            }
        }
    },

    {
        "title": "Step 7 — Show the Result 💬",
        "tip": "Report how close the guess was to HQ.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>After counting matches, we must show the trainee the result.</p><p>This gives feedback so the trainee can adjust their next guess.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Print a label like \"Likeness = \".</p><p>2. Print the value of <b>likeness</b> next to the label.</p><p>3. Make sure this happens for every guess so the trainee can learn from the feedback.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>Feedback creates a loop: guess → result → adjust → guess again. This helps the trainee improve their code-breaking skills.</p>"
            }
        }
    },

    {
        "title": "Step 8 — Win or Retry 🏁",
        "tip": "Decide if the trainee has cracked the code.",
        "tabs": {
            "explain": {
                "label": "📖 What & Why",
                "content": "<p>Now the system decides if the guess is correct.</p><p>If <b>likeness</b> equals 5, the code is fully correct. Otherwise, the trainee tries again.</p>"
            },
            "howto": {
                "label": "🔧 How To",
                "content": "<p>1. Check if <b>likeness</b> equals 5.</p><p>2. If yes:</p><ul><li>Show a success message: \"CODE CRACKED! ACCESS GRANTED.\"</li><li>Set <b>solved</b> to True.</li></ul><p>3. If no:</p><ul><li>Prompt the trainee: 'Try again:'</li></ul><p>This step makes the device behave like a real mission control, giving immediate results for the trainee’s action.</p>"
            },
            "logic": {
                "label": "🧠 Logic",
                "content": "<p>This is the mission’s final checkpoint. The previous steps build up to this decision point.</p>"
            }
        }
    },

    {
        "title": "Step 9 — Mission Complete 🏆",
        "tip": "Your agent’s code-breaking system is operational.",
        "tabs": {
            "explain": {
                "label": "📖 Debrief",
                "content": "<p>🟢 Code cracked. Excellent work, Agent!</p><p>You built a fully operational code-breaking device. It can:</p><ul><li>Receive input</li><li>Store and clean data</li><li>Compare and evaluate guesses</li><li>Report results</li><li>Decide if the mission is complete</li></ul><p>This mirrors real training systems used by agents in the field.</p>"
            },
            "howto": {
                "label": "🧠 What You Built",
                "content": "<p>You didn’t just write code… you built a complete loop:</p><p>⌨️ INPUT → 📓 STORE → 🔍 CHECK → 💬 OUTPUT → 🏁 RESULT</p><p>Every future program will follow this same pattern.</p>"
            },
            "logic": {
                "label": "🕵️ Final Message",
                "content": "<p>📡 Incoming transmission…</p><p>Agent, your system is now active and ready for the next trainees.</p><p>They will try to break the code you created. Stay sharp — you may need to improve or outsmart your own design in future missions.</p>"
            }
        }
    }
],

"patrol_alarm": {
    "title": "📘 Light Bar Control Guide",
    "tip": "Build the flashing pattern that controls the patrol light bar.",
    "tabs": {
        "mission": {
            "label": "🧠 Mission",
            "image_html": patrol_lights,
            "content": """
<h3>You are building the patrol vehicle light bar system.</h3>

<p>
The light bar must flash in a clear pattern so people can see the vehicle at night.
</p>

<p>
The system follows these rules:
</p>

<p>
- The switch controls the whole system.<br>
- If the button is OFF → all lights stay OFF.<br>
- If the button is ON(pressed) → the flashing pattern begins.<br>
- The lights flash one at a time.<br>
- The pattern repeats again and again.
</p>

<p>
Each light flash must use a short pause.
</p>

<p>
At Night Patrol Academy we use:<br>
<b>delay(150)</b>
</p>

<p>
Use this delay after each light turns ON and turns OFF.
</p>

<p>
Your job is to build the flashing pattern using blocks.
</p>
"""
        },
        "wiring": {
            "label": "🔌 Wiring",
            "content": """
<b>Match each part to its pin:</b>
<p>

🔘 Master Button → Pin 12  
🔴 Red Light → Pin 8  
🔵 Blue Light → Pin 6  
⚪ Clear Strobe Light → Pin 4  

Find the part in the diagram.  
Follow the wire.  
Match it to the pin.

</p>
"""
        },
        "logic": {
            "label": "🧩 Logic",
            "content": """
<b>🔘 Button Input Rule</b>
<p>

Look at the wiring diagram.

If the Button connects to GND,
choose:

INPUT_PULLUP

That is how this wiring style works.

<b>Understanding the Button:</b>

The Arduino sees <b>HIGH</b> when the Button is <b>OFF s(not pressed)</b>.

The Arduino sees <b>LOW</b> when the Button is <b>ON (pressed)</b>.

So when we write:

<b>If digitalRead(button pin) equals LOW</b>

The Arduino knows the system should run.

<b>Think about the pattern:</b>

IF button is ON (pressed)

Red light ON  
delay(150)  
Red light OFF  

Blue light ON  
delay(150)  
Blue light OFF  

Clear light ON  
delay(150)  
Clear light OFF  

Then the pattern repeats.

IF button is OFF (not pressed) (else)

All lights OFF.

Remember:

The button controls everything.
</p>
"""
        }
    }
}
}