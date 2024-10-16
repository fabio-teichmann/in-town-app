import streamlit as st
import pandas as pd


def get_categories():
    if "user_categories" not in st.session_state:
        return pd.DataFrame()
    return st.session_state.user_categories


@st.dialog("Add category")
def create_new_category():
    category = st.text_input(label="Category Name", key="user_category")
    categories = get_categories()
    button = st.button("Add Category")
    if button:
        id = len(categories) + 1
        category = pd.DataFrame(index=[0], data={"id": id, "Category": category})
        st.session_state.user_categories = pd.concat([categories, category], ignore_index=True)
        st.write(st.session_state.user_categories)
        st.rerun()

def edit_category():
    pass


def delete_category():
    pass


st.title("User Categories")

left, center, right, _ = st.columns(4)
left.button("Add category :material/add:", on_click=create_new_category)
center.button("Edit category :material/edit:", on_click=edit_category)
right.button("Delete category :material/delete:", on_click=delete_category)

if "user_categories" not in st.session_state:
    # add dummy data
    dummy_categories = pd.DataFrame(
        data={"id": [1, 2], "Category": ["Family", "Besties"]}
    )
    st.session_state.user_categories = dummy_categories

categories = get_categories()
st.table(categories)
