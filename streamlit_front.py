import streamlit as st

import chgk_game_back as cgb

st.title("CHGK Game")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("get_d20"):
        result = cgb.get_d20()
        st.write(f"**Result:** {result}")

with col2:
    if st.button("get_d100"):
        result = cgb.get_d100()
        st.write(f"**Result:** {result}")

with col3:
    difficulty = st.number_input(
        "Difficulty (1-100)",
        min_value=1,
        max_value=100,
        value=50,
        key="difficulty",
    )
    if st.button("Try to solve"):
        result = cgb.try_d100(difficulty)
        st.write(f"**Result:** {result}")
