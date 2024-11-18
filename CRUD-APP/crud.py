import streamlit as st
import mysql.connector

# Set Streamlit page
st.set_page_config(
    page_title="CRUD App",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# custom styling
st.markdown(
    """
    <style>
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        border: 1px solid #ddd;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .data-table th, .data-table td {
        text-align: left;
        padding: 10px;
        border: 1px solid #ddd;
    }
    .data-table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="form_db"
    )

# insert data 
def insert_data(name, email, age):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, age))
        conn.commit()
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

#  fetch data
def fetch_data():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()

# delete data
def delete_data(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        st.success(f"Deleted entry with ID {user_id}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# update data
def update_data(user_id, name, email, age):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s"
        cursor.execute(query, (name, email, age, user_id))
        conn.commit()
        st.success(f"Updated entry with ID {user_id}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Streamlit 
st.title("📝 CRUD App")

# Initialize session state
if 'data_updated' not in st.session_state:
    st.session_state.data_updated = False

# Input form
st.write("### Add New User")
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    submitted = st.form_submit_button("Submit")

if submitted:
    if name and email and age:
        insert_data(name, email, age)
        st.session_state.data_updated = True
    else:
        st.warning("Please fill out all fields.")

# Table
st.write("### User Table")
rows = fetch_data()

if rows:
    st.markdown(
        """
        <table class="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Age</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
        """,
        unsafe_allow_html=True,
    )

    for row in rows:
        col1, col2, col3, col4, col5 = st.columns([1, 3, 4, 2, 2])
        col1.markdown(f"<div>{row[0]}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div>{row[1]}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div>{row[2]}</div>", unsafe_allow_html=True)
        col4.markdown(f"<div>{row[3]}</div>", unsafe_allow_html=True)
        
        # Buttons for editing and deleting
        if col5.button("Edit", key=f"edit_{row[0]}"):
            name = row[1]
            email = row[2]
            age = row[3]
            with st.form("edit_form"):
                new_name = st.text_input("Name", value=name)
                new_email = st.text_input("Email", value=email)
                new_age = st.number_input("Age", min_value=1, max_value=120, step=1, value=age)
                submit_edit = st.form_submit_button("Update")

            if submit_edit:
                update_data(row[0], new_name, new_email, new_age)
                st.session_state.data_updated = True

        if col5.button("Delete", key=f"delete_{row[0]}"):
            delete_data(row[0])
            st.session_state.data_updated = True

    st.markdown("</tbody></table>", unsafe_allow_html=True)
else:
    st.info("No data available.")

# refresh the data
if st.session_state.data_updated:
    st.session_state.data_updated = False
    st.rerun()  
