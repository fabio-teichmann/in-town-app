import streamlit as st
import pandas as pd


def get_users() -> pd.DataFrame:
    if st.session_state.users is None:
        raise ValueError("no users available")
    return st.session_state.get("users")


def create_new_user():
    pass

def edit_user():
    pass

def delete_user():
    pass


st.title("Users")

if "users" not in st.session_state:
    df = pd.DataFrame(
        columns=[
            "id",
            "Nick name",
            "Name",
            "First name",
            "Country",
            "City",
            "Category",
        ]
    )
    dummy_users = pd.DataFrame(
        {
            "id": ["as0", "df1"],
            "Nick name": ["Jonny", "Jane"],
            "Name": ["Doe", "Doe"],
            "First name": ["John", "Jane"],
            "Country": ["DE", "FR"],
            "City": ["Berlin", "Paris"],
            "Category": ["Family", "Besties"],
        }
    )
    df = pd.concat([df, dummy_users], ignore_index=True)
    st.session_state["users"] = df

# buttons for adding, editing, deleting users
left, center, right, _, _ = st.columns(5)


left.button("Add user :material/person_add:", on_click=create_new_user)
if center.button("Edit user :material/edit:"):
    edit_user()
right.button("Delete user :material/delete:", on_click=delete_user)

users = get_users()
st.table(users)
