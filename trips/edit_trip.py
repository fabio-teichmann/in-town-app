import streamlit as st
from trips.trips import (
    get_upcoming_trips,
    get_upcoming_trip,
    ProcessOptions,
    process_trip,
)
import datetime

st.title("Edit Trip")

trips = get_upcoming_trips()
options = [trip.id for trip in trips]


def display_trip(_id):
    for trip in get_upcoming_trips():
        if trip["id"] == _id:
            return f"{trip.Destination} ({trip.Country}) - {trip['Start Date']} / {trip['End Date']}"


trip_id = st.selectbox(
    "Choose your trip", options=options, format_func=lambda x: display_trip(x)
)
st.session_state.trip_id = trip_id


if st.button("Edit trip", key="edit_trip"):
    with st.form("edit_trip"):
        trip = get_upcoming_trip(trip_id)

        left, _, right = st.columns([5, 1, 5])
        left.text_input("Destination:", value=trip.Destination, key="destination")
        right.text_input("Country:", value=trip.Country, max_chars=2, key="country")

        st.date_input(
            label="Select the time period for your trip:",
            min_value=datetime.date.today(),
            value=[trip["Start Date"], trip["End Date"]],
            format="DD.MM.YYYY",
            key="time_period",
        )
        st.session_state.process_option = ProcessOptions.edit

        if st.form_submit_button("Submit changes", on_click=process_trip):
            pass

if st.button("Back to overview"):
    st.switch_page("trips/trips.py")
