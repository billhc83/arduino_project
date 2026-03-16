# ── Code Breaker Progression Series ──────────────────────────────────
# 8 steps. Each step locks previous work as //## codeblocks and adds
# exactly one new piece. The game does not work until step 8.
#
# Cipher — SPARK hidden among decoys FLAME, BRAND, GLOW, BLAZE
#
# Usage:
#   from codebreaker_presets import CODEBREAKER_PRESETS
#   PRESETS.update(CODEBREAKER_PRESETS)

_CIPHER = """  //## Serial.println("================================");
  //## Serial.println("     C O D E  B R E A K E R    ");
  //## Serial.println("================================");
  //## Serial.println("Find the hidden 5-letter word.");
  //## Serial.println("");
  //## Serial.println("X K Q S P A R K M Z");
  //## Serial.println("B R T F L A M E Q X");
  //## Serial.println("P Q S P A R K T Z R");
  //## Serial.println("W Z X B R A N D T P");
  //## Serial.println("S P A R K X Q Z B M");
  //## Serial.println("T R X N G L O W K B");
  //## Serial.println("Q Z B S P A R K X T");
  //## Serial.println("M X T R B L A Z E P");
  //## Serial.println("B T Z X Q M R N V K");
  //## Serial.println("P N V Q Z B X T M R");
  //## Serial.println("");
  //## Serial.println("Enter your guess:");"""

CODEBREAKER_PRESETS = {

    # ─────────────────────────────────────────────────────────────────
    # Step 1 — The Variables
    # Student fills in the three global variables.
    # Setup and loop are empty. Nothing runs yet.
    # ─────────────────────────────────────────────────────────────────
    'cb_step1': {
        'sketch': """
String answer = "SPARK";
int likeness = 0;
bool solved = false;

void setup() {
}

void loop() {
}
""",
        'fill_values': False,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 2 — Serial Begin
    # Variables locked. Student adds Serial.begin in setup.
    # The cipher display is locked in setup — uploading now prints
    # the cipher to the serial monitor. First satisfying moment.
    # ─────────────────────────────────────────────────────────────────
    'cb_step2': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  Serial.begin(9600);
%(cipher)s
}

void loop() {
}
""" % {'cipher': _CIPHER},
        'fill_values': True,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 3 — Listening for Input
    # Student builds the outer if: Serial.available() > 0
    # Body is empty. Concept: only act when something has been typed.
    # ─────────────────────────────────────────────────────────────────
    'cb_step3': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  if (Serial.available() > 0) {
  }
}
""" % {'cipher': _CIPHER},
        'fill_conditions': False,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 4 — Reading the Guess
    # If condition locked. Student adds Serial.readString inside the if.
    # Concept: capture what the player typed into a variable called guess.
    # ─────────────────────────────────────────────────────────────────
    'cb_step4': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  //## if (Serial.available() > 0) {
  String guess = Serial.readString();
  //##   guess.trim();
  //##   guess.toUpperCase();
  //## }
}
""" % {'cipher': _CIPHER},
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 5 — Reset the Score
    # Student adds setvar likeness = 0 inside the if.
    # Concept: clear the score before each new guess so we count fresh.
    # ─────────────────────────────────────────────────────────────────
    'cb_step5': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  //## if (Serial.available() > 0) {
  //##   String guess = Serial.readString();
  //##   guess.trim();
  //##   guess.toUpperCase();
  likeness = 0;
  //## }
}
""" % {'cipher': _CIPHER},
        'fill_values': False,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 6 — The Letter Checker (Explain Only)
    # Nothing for the student to fill in this step.
    # The locked for loop is explained on the page.
    # Concept: it checks one letter at a time and adds 1 to likeness
    # every time a letter is in the right spot.
    # ─────────────────────────────────────────────────────────────────
    'cb_step6': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  //## if (Serial.available() > 0) {
  //##   String guess = Serial.readString();
  //##   guess.trim();
  //##   guess.toUpperCase();
  //##   likeness = 0;
  //##   for (int i = 0; i < 5; i++) { if (guess[i] == answer[i]) { likeness++; } }
  //## }
}
""" % {'cipher': _CIPHER},
        'fill_conditions': True,
        'fill_values': True,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 7 — Print the Result
    # Student adds Serial.print("Likeness = ") and Serial.println(likeness)
    # Concept: send the score back to the player after every guess.
    # ─────────────────────────────────────────────────────────────────
    'cb_step7': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  //## if (Serial.available() > 0) {
  //##   String guess = Serial.readString();
  //##   guess.trim();
  //##   guess.toUpperCase();
  //##   likeness = 0;
  //##   for (int i = 0; i < 5; i++) { if (guess[i] == answer[i]) { likeness++; } }
  Serial.print("Likeness = ");
  Serial.println(likeness);
  //## }
}
""" % {'cipher': _CIPHER},
        'fill_values': False,
    },

    # ─────────────────────────────────────────────────────────────────
    # Step 8 — Win or Try Again (Complete Game)
    # Student builds if likeness == 5 with win message and solved = true,
    # plus the else with Try again. Game is now fully working.
    # ─────────────────────────────────────────────────────────────────
    'cb_step8': {
        'sketch': """
//## String answer = "SPARK";
//## int likeness = 0;
//## bool solved = false;

void setup() {
  //## Serial.begin(9600);
%(cipher)s
}

void loop() {
  //## if (Serial.available() > 0) {
  //##   String guess = Serial.readString();
  //##   guess.trim();
  //##   guess.toUpperCase();
  //##   likeness = 0;
  //##   for (int i = 0; i < 5; i++) { if (guess[i] == answer[i]) { likeness++; } }
  //##   Serial.print("Likeness = ");
  //##   Serial.println(likeness);
  if (likeness == 5) {
    Serial.println("CODE CRACKED! ACCESS GRANTED.");
    solved = true;
  } else {
    Serial.println("Try again:");
  }
  //## }
}
""" % {'cipher': _CIPHER},
        'fill_conditions': False,
        'fill_values': False,
    },

}
