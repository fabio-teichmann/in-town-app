import streamlit as st


def create_group():
    pass


def edit_group():
    pass


def delete_group():
    pass


st.title("My Groups")

left, mid, right, _ = st.columns(4)

left.button("Create group :material/group_add:", on_click=create_group)
mid.button("Edit group :material/edit:", on_click=edit_group)
right.button("Delete group :material/delete:", on_click=delete_group)

empty_groups = [
    {
        "id": None,
        "name": None,
        "members": [],
    }
]
st.table(empty_groups)
