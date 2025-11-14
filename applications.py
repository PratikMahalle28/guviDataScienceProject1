import streamlit as st
import mysql.connector
import hashlib
import time
from datetime import datetime
import pandas as pd

# --- 1. Configuration & Constants ---
SUPPORTED_ROLES = ['Client', 'Support']
# Define categories for use in both UI and DB filtering
QUERY_CATEGORIES = ["Technical", "General Inquiry"]

# --- 2. Database Management Functions (MySQL) ---

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pratik28@", # <-- REPLACE WITH YOUR PASSWORD
            database='querysystem',
            autocommit=True
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        st.stop() # Stop the app if connection fails

def setup_database():
    """Create the users and queries tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # --- Add these lines to force a fresh start (TESTING ONLY) ---
        # cursor.execute("DROP TABLE IF EXISTS queries;")
        # cursor.execute("DROP TABLE IF EXISTS users;")
        # -------------------------------------------------------------

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(100) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('Client', 'Support'))
            );
        ''')
        
        # Create queries table (this now correctly includes 'category' in the initial creation)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                query_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                client_email VARCHAR(255) NOT NULL,
                client_mobile VARCHAR(20),
                query_heading VARCHAR(255) NOT NULL,
                query_description TEXT NOT NULL,
                query_created_time DATETIME DEFAULT CURRENT_TIMESTAMP, 
                query_closed_time DATETIME NULL,
                status VARCHAR(20) NOT NULL CHECK (status IN ('Open', 'Closed')),
                category VARCHAR(50) NULL, 
                assigned_support_id INT NULL,
                FOREIGN KEY (assigned_support_id) REFERENCES users(user_id)
            );
        ''')
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Error during table setup: {err}")
    finally:
        cursor.close()
        conn.close()


# --- 3. Authentication Functions (using hashlib.sha256) ---

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """Verify credentials against the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) # Fetch rows as dictionaries
    hashed_input_password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND hashed_password = %s"
    cursor.execute(query, (username, hashed_input_password))
    user = cursor.fetchone() 
    cursor.close()
    conn.close()
    return user

def register_user(username, password, role):
    """Register a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pass = hash_password(password)
    try:
        query = "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_pass, role))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        st.error(f"Error: Username '{username}' already exists.")
        return False
    except mysql.connector.Error as err:
        st.error(f"Database error during registration: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# --- 4. Query Management Functions (Updated) ---

def submit_new_query(email, mobile, heading, description, category):
    """Inserts a new 'Open' query into the queries table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO queries (client_email, client_mobile, query_heading, query_description, status, category) 
        VALUES (%s, %s, %s, %s, 'Open', %s)
        """
        # Note: assigned_support_id is NULL initially.
        cursor.execute(query, (email, mobile, heading, description, category))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Error submitting query: {err}")
        return False
    finally:
        cursor.close()
        conn.close()
        
def get_queries(status_filter=None, category_filter=None):
    """Fetches queries with optional status and category filters."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql_query = "SELECT * FROM queries WHERE 1=1"
    params = []

    if status_filter:
        sql_query += " AND status = %s"
        params.append(status_filter)
    if category_filter:
        sql_query += " AND category = %s"
        params.append(category_filter)
        
    sql_query += " ORDER BY query_created_time DESC"
    
    cursor.execute(sql_query, tuple(params))
    queries = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return queries


def close_query_db(query_id, support_user_id):
    """
    Update a query status to 'Closed' and set the closure timestamp 
    and assign the support agent ID in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # MySQL's NOW() function handles the datetime auto-setting
        query = """
        UPDATE queries 
        SET status = 'Closed', query_closed_time = NOW(), assigned_support_id = %s
        WHERE query_id = %s AND status = 'Open'
        """
        cursor.execute(query, (support_user_id, query_id))
        conn.commit()
        # Check if any rows were affected
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        st.error(f"Error closing query in DB: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# --- 5. Streamlit UI Components & Navigation ---

def logout():
    st.session_state.clear()
    st.session_state['menu'] = 'login'
    st.rerun()

def render_login_page():
    st.title("User Login Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = verify_user(username, password)
        if user:
            st.session_state['authenticated'] = True
            st.session_state['user_role'] = user['role']
            st.session_state['username'] = user['username']
            st.session_state['user_id'] = user['user_id']
            st.success(f"Welcome {user['username']}! Redirecting...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password.")

def render_register_page():
    st.title("User Registration")
    new_username = st.text_input("Choose Username")
    new_password = st.text_input("Choose Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    new_role = st.selectbox("Role", SUPPORTED_ROLES)
    if st.button("Register"):
        if new_password == confirm_password:
            if register_user(new_username, new_password, new_role):
                st.success("Registration successful! You can now log in.")
                st.session_state['menu'] = 'login'
                time.sleep(1)
                st.rerun()
        else:
            st.error("Passwords do not match.")

def render_client_page():
    st.title(f"Welcome, Client {st.session_state['username']}")
    st.subheader("Submit a New Query")
    client_email = st.text_input("Contact Email", value=st.session_state['username'] if '@' in st.session_state['username'] else "")
    client_mobile = st.text_input("Contact Mobile (Optional)")
    query_category = st.selectbox("Category", QUERY_CATEGORIES) # Use the defined categories
    query_title = st.text_input("Query Title")
    query_details = st.text_area("Query Details")
    if st.button("Submit Query"):
        if query_title and query_details and client_email and query_category:
            if submit_new_query(client_email, client_mobile, query_title, query_details, query_category):
                st.success("Query submitted successfully! We will get back to you shortly.")
            else:
                st.error("Failed to submit query.")
        else:
            st.warning("Please fill in all required fields.")
    st.markdown("---")
    if st.button("Logout"):
        logout()

def render_support_page():
    st.title(f"Welcome, Support Team Member {st.session_state['username']}")
    
    st.subheader("View and Filter Queries")

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "Closed"])
    with col2:
        # Add "All" option to categories list
        category_filter = st.selectbox("Filter by Category", ["All"] + QUERY_CATEGORIES)

    status_db = status_filter if status_filter != "All" else None
    category_db = category_filter if category_filter != "All" else None
    
    queries = get_queries(status_db, category_db)

    st.write(f"Found {len(queries)} matching queries.")

    if queries:
        # Display queries in a dataframe for easy viewing
        df = pd.DataFrame(queries)
        # Reorder columns for better readability if desired
        df = df[['query_id', 'status', 'category', 'query_heading', 'client_email', 'query_created_time', 'query_closed_time', 'assigned_support_id']]
        st.dataframe(df)

        st.markdown("---")
        st.subheader("Select and Close an Open Query")

        open_queries = [q for q in queries if q['status'] == 'Open']

        if open_queries:
            query_options = {f"ID {q['query_id']}: {q['query_heading']} ({q['category']})": q['query_id'] for q in open_queries}
            selected_query_display = st.selectbox("Choose an Open Query to Close", list(query_options.keys()))
            
            if st.button("Close Selected Query"):
                selected_query_id = query_options[selected_query_display]
                # Action: On Closure: status is updated to "Closed" & query_closed_time is auto-set
                if close_query_db(selected_query_id, st.session_state['user_id']):
                    st.success(f"Query ID {selected_query_id} has been successfully closed and timestamped.")
                    st.rerun() # Refresh the page to reflect the new status
                else:
                    st.error("Failed to close query. It might already be closed or a DB error occurred.")
        else:
            st.info("No open queries available to close with current filters.")
    else:
        st.info("No queries found matching the selected criteria.")

    st.markdown("---")
    if st.button("Logout"):
        logout()
    
# --- 6. Main App Logic ---

def main():
    """Main function to run the Streamlit application."""
    # Initialize session state variables if they don't exist
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'menu' not in st.session_state:
        st.session_state['menu'] = 'login'
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None

    # Ensure database tables exist before running the app logic
    setup_database()

    # Navigation logic
    if st.session_state['authenticated']:
        if st.session_state['user_role'] == 'Client':
            render_client_page()
        elif st.session_state['user_role'] == 'Support':
            render_support_page()
    else:
        # Use a sidebar for navigation between login/register when not authenticated
        st.sidebar.title("Navigation")
        if st.session_state['menu'] == 'login':
            if st.sidebar.button("Go to Register"):
                st.session_state['menu'] = 'register'
                st.rerun()
            render_login_page()
        elif st.session_state['menu'] == 'register':
            if st.sidebar.button("Go to Login"):
                st.session_state['menu'] = 'login'
                st.rerun()
            render_register_page()

if __name__ == "__main__":
    main()

