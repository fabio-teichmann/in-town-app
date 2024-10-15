import streamlit as st
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


home_page = st.Page("home.py", title="Home", icon=":material/home:")
trips_page = st.Page("trips/trips.py", title="Overview", icon=":material/travel:")
trips_edit = st.Page("trips/edit_trip.py", title="Edit Trip", icon=":material/edit:")
groups_page = st.Page("groups.py", title="Groups", icon=":material/groups:")
users_page = st.Page("groups/users.py", title="Users", icon=":material/person:")
user_category_page = st.Page(
    "groups/user_categories.py", title="User Categories", icon=":material/badge:"
)

pg = st.navigation(
    {
        "Home": [home_page],
        "Trips": [trips_page, trips_edit],
        "Groups": [groups_page, users_page, user_category_page],
    }
)

pg.run()
