import streamlit as st


def get_categories():
    if "user_categories" not in st.session_state:
        return [{}]
    return st.session_state.user_categories


@st.dialog("Add category")
def create_new_category():
    category = st.text_input(label="Category Name", key="user_category")
    categories = get_categories()
    button = st.button("Add Category")
    if button:
        id = len(categories) + 1
        category = {"id": id, "Category": category}
        st.session_state.user_categories.append(category)
        st.rerun()


def display_cat(option):
    for cat in get_categories():
        if option["id"] == cat["id"]:
            return f"{cat['Category']}"


@st.dialog("Edit category")
def edit_category():
    categories = get_categories()

    selected_category = st.selectbox(
        label="Select Category", options=categories, format_func=display_cat
    )
    new_category = st.text_input(
        label="Category Name", value=selected_category["Category"]
    )

    button = st.button("Edit Category")
    if button:
        for cat in categories:
            if cat["id"] == selected_category["id"]:
                cat["Category"] = new_category
        st.session_state.user_categories = categories
        st.rerun()


@st.dialog("Delete category")
def delete_category():
    categories = get_categories()
    selected_category = st.selectbox(
        label="Select Category", options=categories, format_func=display_cat
    )

    button = st.button("Delete Category")
    if button:
        categories.remove(selected_category)
        st.session_state.user_categories = categories
        st.rerun()


st.title("User Categories")

left, center, right, _ = st.columns(4)
left.button("Add category :material/add:", on_click=create_new_category)
center.button("Edit category :material/edit:", on_click=edit_category)
right.button("Delete category :material/delete:", on_click=delete_category)

if "user_categories" not in st.session_state:
    # add dummy data
    dummy_categories = [
        {
            "id": 1,
            "Category": "Family",
        },
        {
            "id": 2,
            "Category": "Besties",
        },
    ]
    st.session_state.user_categories = dummy_categories

categories = get_categories()
st.table(categories)
