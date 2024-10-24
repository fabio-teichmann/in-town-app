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
        id = max(categories["id"]) + 1
        category = pd.DataFrame(index=[0], data={"id": id, "Category": category})
        st.session_state.user_categories = pd.concat(
            [categories, category], ignore_index=True
        )
        st.write(st.session_state.user_categories)
        st.rerun()


def display_cat(option):
    for _, cat in get_categories().iterrows():
        if option == cat["id"]:
            return f"{cat['Category']}"


@st.dialog("Edit category")
def edit_category():
    categories = get_categories()

    cat_id = st.selectbox(
        label="Select Category", options=categories, format_func=display_cat
    )
    cat_name = categories.loc[categories["id"] == cat_id]["Category"].iloc[0]
    new_category = st.text_input(label="Category Name", value=cat_name)

    button = st.button("Edit Category")
    if button:
        categories.loc[categories["id"] == cat_id, "Category"] = new_category
        st.session_state.user_categories = categories
        st.rerun()


@st.dialog("Delete category")
def delete_category():
    categories = get_categories()
    cat_id = st.selectbox(
        label="Select Category", options=categories, format_func=display_cat
    )

    button = st.button("Delete Category")
    if button:
        categories = categories.loc[categories["id"] != cat_id]
        st.session_state.user_categories = categories
        st.rerun()


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
