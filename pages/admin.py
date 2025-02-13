import streamlit as st
import pandas as pd
from database import (
    verify_admin,
    get_chat_history,
    get_course_data,
    update_course_data
)
import json
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(
    page_title="University Course Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_login():
    st.title("Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if verify_admin(username, password):
                st.session_state['admin_authenticated'] = True
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_admin_dashboard():
    st.title("Admin Dashboard")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Chat Analytics", "Course Data Management"])
    
    if page == "Chat Analytics":
        show_chat_analytics()
    else:
        show_course_management()

def show_chat_analytics():
    st.header("Chat Analytics")
    
    # Get chat history
    chats = get_chat_history()
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(chats)
    if not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Basic analytics
        st.subheader("Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Chats", len(df))
        with col2:
            st.metric("Unique Days", len(df['date'].unique()))
        with col3:
            st.metric("Today's Chats", len(df[df['date'] == datetime.now().date()]))
        
        # Chat history table
        st.subheader("Recent Chats")
        st.dataframe(
            df[['timestamp', 'user_message', 'bot_response']]
            .sort_values('timestamp', ascending=False)
            .head(50)
        )
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Complete Chat History",
            csv,
            "chat_history.csv",
            "text/csv"
        )
    else:
        st.info("No chat history available")

def show_course_management():
    st.header("Course Data Management")
    
    # Get current course data
    courses = get_course_data()
    
    # Display current data
    st.subheader("Current Course Data")
    
    # Convert to formatted string for editing
    courses_str = json.dumps(courses, indent=2)
    
    # Create an editor for the JSON
    edited_courses_str = st.text_area(
        "Edit course data (JSON format)",
        value=courses_str,
        height=400
    )
    
    if st.button("Update Course Data"):
        try:
            # Parse the edited JSON
            edited_courses = json.loads(edited_courses_str)
            
            # Validate the structure (you might want to add more validation)
            if not isinstance(edited_courses, dict):
                st.error("Invalid data structure")
                return
            
            # Update the database
            update_course_data(edited_courses)
            st.success("Course data updated successfully!")
            
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def admin_page():
    # Initialize session state
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False
    
    # Show login or dashboard based on authentication status
    if not st.session_state['admin_authenticated']:
        show_login()
    else:
        show_admin_dashboard()
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state['admin_authenticated'] = False
            st.rerun()

if __name__ == "__main__":
    admin_page()