import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from components.arduino_blocks import arduino_block_coder
st.set_page_config(page_title="My Arduino Tool", layout= "wide")
st.title("Build Your Sketch")

arduino_block_coder(preset = 'Blink') 