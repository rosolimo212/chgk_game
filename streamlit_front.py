import streamlit as st

import chgk_game_back as cgb

st.title("The CHGK Game")

if "results" not in st.session_state:
    st.session_state.results = ["—", "—", "—"]

# Row 1: Roll d20
left1, right1 = st.columns([2, 1])
with left1:
    if st.button("Roll d20", key="d20"):
        st.session_state.results[0] = cgb.get_d20()
        st.rerun()
with right1:
    st.metric("Result", st.session_state.results[0])

# Row 2: Roll d100
left2, right2 = st.columns([2, 1])
with left2:
    if st.button("Roll d100", key="d100"):
        st.session_state.results[1] = cgb.get_d100()
        st.rerun()
with right2:
    st.metric("Result", st.session_state.results[1])

# Row 3: Try to solve
left3, right3 = st.columns([2, 1])
with left3:
    difficulty = st.number_input(
        "Difficulty (1-100)",
        min_value=1,
        max_value=100,
        value=50,
        key="difficulty",
    )
    if st.button("Try to solve with difficulty {difficulty}".format(difficulty=difficulty), key="solve"):
        st.session_state.results[2] = cgb.try_d100(difficulty)
        st.rerun()
with right3:
    st.metric("Result", st.session_state.results[2])
