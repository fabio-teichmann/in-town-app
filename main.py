import streamlit as st


home_page = st.Page("in_town.py", title="Home", icon=":material/home:")
trips_page = st.Page("app_pages/trips.py", title="Trips", icon=":material/travel:")
groups_page = st.Page("app_pages/groups.py", title="Groups", icon=":material/groups:")

pg = st.navigation([home_page, trips_page, groups_page])

pg.run()
