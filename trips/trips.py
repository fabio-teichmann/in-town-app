import streamlit as st
import datetime
from in_town_app import logger


def get_upcoming_trips():
    trips = st.session_state.trips
    return [trip for trip in trips if trip["End Date"] >= datetime.date.today()]


def get_upcoming_trip(trip_id):
    trips = get_upcoming_trips()
    for trip in trips:
        if trip["id"] == trip_id:
            return trip
    logger.warning(f"Trip not found: {trip_id}")


def get_past_trips():
    trips = st.session_state.trips
    return [trip for trip in trips if trip["End Date"] < datetime.date.today()]


@st.dialog("Create new trip")
def create_new_trip():
    with st.form("create_trip"):
        left, _, right = st.columns([5, 1, 5])
        left.text_input("Destination:", placeholder="Berlin", key="destination")
        right.text_input("Country:", placeholder="DE", max_chars=2, key="country")

        st.date_input(
            label="Select the time period for your trip:",
            min_value=datetime.date.today(),
            value=[],
            format="DD.MM.YYYY",
            key="time_period",
        )

        if st.form_submit_button("Create new trip"):
            logger.info("creating new trip...")
            trip = {
                "id": f"as{len(st.session_state.trips)}",
                "Destination": st.session_state.destination,
                "Country": st.session_state.country,
                "Start Date": st.session_state.time_period[0],
                "End Date": st.session_state.time_period[1],
            }
            st.session_state.trips.append(trip)
            st.rerun()


def display_trip(option):
    for trip in get_upcoming_trips():
        if trip["id"] == option["id"]:
            return f"{trip['Destination']} ({trip['Country']}) - {trip['Start Date']} / {trip['End Date']}"


@st.dialog("Edit trip")
def edit_trip():
    trips = get_upcoming_trips()

    selected_trip = st.selectbox(
        "Choose your trip", options=trips, format_func=lambda x: display_trip(x)
    )

    left, _, right = st.columns([5, 1, 5])
    left.text_input(
        "Destination:", value=selected_trip["Destination"], key="destination"
    )
    right.text_input(
        "Country:", value=selected_trip["Country"], max_chars=2, key="country"
    )

    st.date_input(
        label="Select the time period for your trip:",
        min_value=datetime.date.today(),
        value=[selected_trip["Start Date"], selected_trip["End Date"]],
        format="DD.MM.YYYY",
        key="time_period",
    )

    if st.button("Edit trip", key="edit_trip"):
        logger.info("editing trip...")
        edited_trip = {
            "id": selected_trip["id"],
            "Destination": st.session_state.destination,
            "Country": st.session_state.country,
            "Start Date": st.session_state.time_period[0],
            "End Date": st.session_state.time_period[1],
        }
        for idx, trip in enumerate(st.session_state.trips):
            if trip["id"] == selected_trip["id"]:
                st.session_state.trips[idx] = edited_trip
        st.rerun()


@st.dialog("Delete trip")
def delete_trip():
    trips = get_upcoming_trips()

    selected_trip = st.selectbox(
        "Choose your trip", options=trips, format_func=lambda x: display_trip(x)
    )

    if st.button("Delete trip"):
        logger.info("deleting trip...")
        st.session_state.trips.remove(selected_trip)
        st.rerun()


# Page elements
st.title("Trips")

if "trips" not in st.session_state:
    dummy_trips = [
        {
            "id": "as0",
            "Destination": "Berlin",
            "Country": "DE",
            "Start Date": datetime.date.today(),
            "End Date": datetime.date.today(),
            "People Notified": None,
        },
        {
            "id": "as1",
            "Destination": "Paris",
            "Country": "FR",
            "Start Date": datetime.datetime.strptime("07.03.2024", "%d.%m.%Y").date(),
            "End Date": datetime.datetime.strptime("14.03.2024", "%d.%m.%Y").date(),
            "People Notified": None,
        },
    ]
    st.session_state["trips"] = dummy_trips

tab1, tab2 = st.tabs(["Upcoming trips", "Past trips"])


with tab1:
    # buttons for adding, editing, deleting trips
    left, center, right, _, _, _ = st.columns(6)

    left.button("Add trip", on_click=create_new_trip)
    if center.button("Edit trip"):
        edit_trip()
    right.button("Delete trip", on_click=delete_trip)

    upcoming_trips = get_upcoming_trips()
    st.table(upcoming_trips)

with tab2:
    past_trips = get_past_trips()
    st.table(past_trips)
