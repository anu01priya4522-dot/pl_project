import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Database connection
conn = sqlite3.connect("library.db", check_same_thread=False)

conn.execute("""
CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT,
    category TEXT,
    quantity INTEGER
)
""")

conn.commit()

st.title("📚 Library Management System")
st.write("Manage books easily using this application.")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Dashboard",
        "Add Book",
        "View Books",
        "Search Book",
        "Delete Book"
    ]
)

if menu == "Dashboard":

    st.header("Library Dashboard")

    total = conn.execute(
        "SELECT COUNT(*) FROM Books"
    ).fetchone()[0]

    st.metric("Total Book Records", total)

    st.success("Welcome to Library Management System!")

elif menu == "Add Book":

    st.header("Add New Book")

    name = st.text_input("Book Name")
    author = st.text_input("Author")
    category = st.selectbox(
        "Category",
        ["Programming", "Database", "Web", "Other"]
    )
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Add Book"):

        if name.strip():

            conn.execute("""
                INSERT INTO Books
                (book_name, author, category, quantity)
                VALUES (?, ?, ?, ?)
            """, (name, author, category, quantity))

            conn.commit()

            st.success("Book added successfully!")

        else:
            st.warning("Please enter the book name.")

elif menu == "View Books":

    st.header("All Books")

    df = pd.read_sql_query(
        "SELECT * FROM Books",
        conn
    )

    st.dataframe(df, use_container_width=True)

elif menu == "Search Book":

    st.header("Search Books")

    search = st.text_input("Enter book name")

    if st.button("Search"):

        df = pd.read_sql_query(
            "SELECT * FROM Books WHERE book_name LIKE ?",
            conn,
            params=(f"%{search}%",)
        )

        st.dataframe(df, use_container_width=True)

elif menu == "Delete Book":

    st.header("Delete Book")

    book_id = st.number_input(
        "Enter Book ID",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        cursor = conn.execute(
            "DELETE FROM Books WHERE book_id = ?",
            (int(book_id),)
        )

        conn.commit()

        if cursor.rowcount:
            st.success("Book deleted successfully!")
        else:
            st.warning("Book ID not found.")