import streamlit as st

st.title("My Groups")

display = ("male", "female")

options = list(range(len(display)))

value = st.selectbox("gender", options, format_func=lambda x: display[x])

st.write(value)
