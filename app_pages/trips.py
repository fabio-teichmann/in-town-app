import streamlit as st
import pandas as pd
import datetime
import enum
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_upcoming_trips():
    trips = st.session_state.trips
    return [
        trip for _, trip in trips.iterrows() if trip["End Date"] > datetime.date.today()
    ]


def get_upcoming_trip(trip_id):
    trips = get_upcoming_trips()
    for trip in trips:
        if trip["id"] == trip_id:
            return trip
    logger.warning(f"Trip not found: {trip_id}")


def get_past_trips():
    trips = st.session_state.trips
    return [
        trip
        for _, trip in trips.iterrows()
        if trip["End Date"] <= datetime.date.today()
    ]


def add_trip(trip):
    trips = st.session_state.trips
    trip = pd.DataFrame(data=trip, index=[0])
    st.session_state.trips = pd.concat([trips, trip], axis=0, ignore_index=True)


# def edit_trip(trip, trip_id):
#     logger.info("editing trip...")
#     pass


class ProcessOptions(enum.Enum):
    create = "create"
    edit = "edit"
    delete = "delete"


def process_trip():
    process_option = st.session_state.get("process_option", None)
    if process_option is None:
        logger.warning("no process_option set...")
        return

    elif process_option == ProcessOptions.create:
        logger.info("creating new trip...")
        trip = {
            "id": "er3",
            "Destination": st.session_state.destination,
            "Country": st.session_state.country,
            "Start Date": st.session_state.time_period[0],
            "End Date": st.session_state.time_period[1],
        }
        add_trip(trip)

    elif process_option == ProcessOptions.edit:
        logger.info("editing trip...")
        trip = {
            "id": "er3",
            "Destination": st.session_state.destination,
            "Country": st.session_state.country,
            "Start Date": st.session_state.time_period[0],
            "End Date": st.session_state.time_period[1],
        }
        trips = st.session_state.trips
        trip = pd.DataFrame(data=trip, index=[0])
        st.session_state.trips = pd.concat([trips, trip], axis=0, ignore_index=True)

    elif process_option == ProcessOptions.delete:
        logger.info("deleting trip...")

    else:
        raise NotImplementedError(f"Unknown process option: {process_option}")

    st.session_state.process_option = None


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
            st.session_state.process_option = ProcessOptions.create
            process_trip()
            st.rerun()


@st.dialog("Edit trip")
def edit_trip():
    trips = get_upcoming_trips()
    options = [trip.id for trip in trips]

    def display_trip(_id):
        for trip in get_upcoming_trips():
            if trip["id"] == _id:
                return f"{trip.Destination} ({trip.Country}) - {trip['Start Date']} / {trip['End Date']}"

    trip_id = st.selectbox("Choose your trip", options=options, format_func=lambda x: display_trip(x))
    st.write(trip_id)

    if st.button("Edit trip"):
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

            if st.form_submit_button("Submit changes"):
                st.session_state.process_option = ProcessOptions.edit
                process_trip()
                st.rerun()
            if st.form_submit_button("Cancel"):
                edit_trip()


@st.dialog("Delete trip")
def delete_trip():
    trips = get_upcoming_trips()
    options = []
    if len(trips) != 0:
        options = [
            f"{trip.Destination} ({trip.Country}) - {trip['Start Date']} / {trip['End Date']}"
            for trip in trips
        ]
    st.selectbox("Choose your trip", options=options)

    if st.button("Delete trip"):
        st.session_state.process_option = ProcessOptions.delete
        process_trip()
        st.rerun()


# Page elements
st.title("Trips")

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
    dummy_trips = pd.DataFrame(
        {
            "id": ["as0", "df1"],
            "Destination": ["Berlin", "Paris"],
            "Country": ["DE", "FR"],
            "Start Date": [
                datetime.datetime.strptime("10.10.2024", "%d.%m.%Y").date(),
                datetime.datetime.strptime("07.03.2024", "%d.%m.%Y").date(),
            ],
            "End Date": [
                datetime.datetime.strptime("21.10.2024", "%d.%m.%Y").date(),
                datetime.datetime.strptime("14.03.2024", "%d.%m.%Y").date(),
            ],
            "People Notified": [None, None],
        }
    )
    df = pd.concat([df, dummy_trips], ignore_index=True)
    st.session_state["trips"] = df

tab1, tab2 = st.tabs(["Upcoming trips", "Past trips"])


with tab1:
    # buttons for adding, editing, deleting trips
    left, center, right, _, _, _ = st.columns(6)

    left.button("Add trip", on_click=create_new_trip)
    center.button("Edit trip", on_click=edit_trip)
    right.button("Delete trip", on_click=delete_trip)

    upcoming_trips = get_upcoming_trips()
    st.table(upcoming_trips)

with tab2:
    past_trips = get_past_trips()
    st.table(past_trips)
