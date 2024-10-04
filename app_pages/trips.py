import streamlit as st
import pandas as pd

st.title("Trips")

tab1, tab2 = st.tabs(["Upcoming trips", "Past trips"])


@st.dialog("Create new trip")
def create_new_trip():
    pass


@st.dialog("Edit trip")
def edit_trip():
    pass


@st.dialog("Delete trip")
def delete_trip():
    pass


with tab1:
    # buttons for adding, editing, deleting trips
    left, center, right, _, _, _ = st.columns(6)

    left.button("Add trip", on_click=create_new_trip)
    center.button("Edit trip", on_click=edit_trip)
    right.button("Delete trip", on_click=delete_trip)

    if "trips" not in st.session_state:
        df = pd.DataFrame(
            columns=[
                "Destination",
                "Country",
                "Start Date",
                "End Date",
                "People Notified",
            ]
        )
        st.session_state["trips"] = df

    st.table(st.session_state.trips)


with tab2:
    if "trips" not in st.session_state:
        df = pd.DataFrame(
            columns=[
                "Destination",
                "Country",
                "Start Date",
                "End Date",
                "People Notified",
            ]
        )
        st.session_state["trips"] = df

    st.table(st.session_state.trips)
