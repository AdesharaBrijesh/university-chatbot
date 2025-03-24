import streamlit as st
import pandas as pd
from database import (
    verify_admin,
    get_chat_history,
    get_course_data,
    update_course_data
)
import json
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# Must be the first Streamlit command
st.set_page_config(
    page_title="University Course Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-label {
        color: #666;
        font-size: 14px;
    }
    .bot-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .bot-card h3 {
        color: #333;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

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
    st.title("Chatbot Overview")
    
    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Overview", "Chat Analytics", "Course Data Management"])
    
    if page == "Overview":
        show_overview()
    elif page == "Chat Analytics":
        show_chat_analytics()
    else:
        show_course_management()

def show_overview():
    # Date range selector
    col1, col2 = st.columns([3, 1])
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.now())
    
    # Get chat history
    chats = get_chat_history()
    df = pd.DataFrame(chats)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        filtered_df = df[
            (df['date'] >= start_date) & 
            (df['date'] <= end_date)
        ]
        
        # Key Metrics
        st.subheader("Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Total Sessions</div>
                </div>
            """.format(len(filtered_df['date'].unique())), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Total Messages</div>
                </div>
            """.format(len(filtered_df)), unsafe_allow_html=True)
            
        with col3:
            avg_response_time = 9  # This should be calculated from actual data
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{} Mins</div>
                    <div class="metric-label">Average Session Time</div>
                </div>
            """.format(avg_response_time), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Unique Chatters</div>
                </div>
            """.format(len(filtered_df['user_id'].unique() if 'user_id' in filtered_df.columns else 0)), 
            unsafe_allow_html=True)
        
        # Bot Types Section
        st.subheader("Create New Bot")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="bot-card">
                    <h3>Course Assistant</h3>
                    <p>Engage with students through an AI-powered course assistant</p>
                    <a href="#" style="color: #0066cc;">Configure</a>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="bot-card">
                    <h3>FAQ Bot</h3>
                    <p>Answer common student questions automatically</p>
                    <a href="#" style="color: #0066cc;">Configure</a>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="bot-card">
                    <h3>Study Guide Bot</h3>
                    <p>Help students prepare for exams and assignments</p>
                    <a href="#" style="color: #0066cc;">Configure</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No chat history available")

def show_chat_analytics():
    st.header("Chat Analytics")
    
    # Date range selector
    col1, col2 = st.columns([3, 1])
    with col1:
        start_date = st.date_input("Analytics Start Date", datetime.now() - timedelta(days=30))
        end_date = st.date_input("Analytics End Date", datetime.now())
    
    # Get chat history
    chats = get_chat_history()
    df = pd.DataFrame(chats)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        filtered_df = df[
            (df['date'] >= start_date) & 
            (df['date'] <= end_date)
        ]
        
        # Detailed Analytics
        st.subheader("Chat Metrics")
        
        # Chat history in a more modern table
        st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #333; margin-bottom: 15px;">Recent Conversations</h3>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            filtered_df[['timestamp', 'user_message', 'bot_response']]
            .sort_values('timestamp', ascending=False)
            .head(50),
            use_container_width=True
        )
        
        # Download button with better styling
        st.markdown("""
            <div style="margin-top: 15px;">
        """, unsafe_allow_html=True)
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 Download Chat History",
            csv,
            "chat_history.csv",
            "text/csv",
            key='download-csv'
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("No chat history available for the selected date range")

def show_course_management():
    st.header("Course Data Management")
    
    # Get current course data
    courses = get_course_data()
    
    # Display current data with better styling
    st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <h3 style="color: #333; margin-bottom: 15px;">Course Configuration</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Convert to formatted string for editing
    courses_str = json.dumps(courses, indent=2)
    
    # Create an editor for the JSON with better styling
    st.markdown("""
        <div style="margin-top: 20px; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    edited_courses_str = st.text_area(
        "Edit course data (JSON format)",
        value=courses_str,
        height=400
    )
    
    if st.button("💾 Update Course Data", key='update-course-data'):
        try:
            # Parse the edited JSON
            edited_courses = json.loads(edited_courses_str)
            
            # Validate the structure
            if not isinstance(edited_courses, dict):
                st.error("❌ Invalid data structure")
                return
            
            # Update the database
            update_course_data(edited_courses)
            st.success("✅ Course data updated successfully!")
            
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

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