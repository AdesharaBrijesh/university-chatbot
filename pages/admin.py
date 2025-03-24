import streamlit as st
import pandas as pd
from database import (
    verify_admin,
    verify_admin_session,
    get_chat_history,
    get_course_data,
    update_course_data,
    get_user_stats,
    get_course_inquiry_stats
)
import json
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import plotly.express as px

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
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #0066cc;
        margin: 10px 0;
    }
    .metric-label {
        color: #666;
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
    .sidebar-content {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #333;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        margin: 0.2rem 0;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateX(5px);
    }
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .admin-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .section-title {
        color: #333;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.2rem;
    }
    .chart-container {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }
    .date-range-container {
        display: flex;
        gap: 15px;
        align-items: center;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def show_login():
    st.markdown("""
        <div class="login-container">
            <h2 style="text-align: center; margin-bottom: 2rem;">Admin Login</h2>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            session_token = verify_admin(username, password)
            if session_token:
                st.session_state['admin_session_token'] = session_token
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_admin_dashboard():
    # Header with logout button
    st.markdown("""
        <div class="admin-header">
            <h1 style="margin: 0;">📊 Chatbot Analytics Dashboard</h1>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="color: #666;">Welcome, Admin</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with improved styling
    with st.sidebar:
        st.image("./Resources/Logo.png", use_container_width=True)
        
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header">🎯 Navigation</div>', unsafe_allow_html=True)
        page = st.radio(
            "Navigation Menu",
            ["Overview", "Chat Analytics", "Course Data Management"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Admin Actions
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header">⚙️ Admin Actions</div>', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state['admin_session_token'] = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if page == "Overview":
        show_overview()
    elif page == "Chat Analytics":
        show_chat_analytics()
    else:
        show_course_management()

def show_overview():
    # Get user statistics
    user_stats = get_user_stats()
    course_stats = get_course_inquiry_stats()
    
    # User Statistics Section
    st.markdown("""
        <div class="section-container">
            <div class="section-title">👥 User Statistics</div>
            <div class="metric-grid">
                <div class="metric-card" style="background-color: #E3F2FD;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">👤 Total Users</div>
                </div>
                <div class="metric-card" style="background-color: #F3E5F5;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">✨ Active Today</div>
                </div>
                <div class="metric-card" style="background-color: #E8F5E9;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">🆕 New Users Today</div>
                </div>
                <div class="metric-card" style="background-color: #FFF3E0;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">🔄 Returning Users</div>
                </div>
                <div class="metric-card" style="background-color: #FFEBEE;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">📅 Active This Week</div>
                </div>
                <div class="metric-card" style="background-color: #F3E5F5;">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">📆 Active This Month</div>
                </div>
                <div class="metric-card" style="background-color: #E0F7FA;">
                    <div class="metric-value">{}%</div>
                    <div class="metric-label">📈 Return Rate</div>
                </div>
            </div>
        </div>
    """.format(
        user_stats["total_users"],
        user_stats["active_today"],
        user_stats["new_users_today"],
        user_stats["returning_users"],
        user_stats["active_this_week"],
        user_stats["active_this_month"],
        round(user_stats["returning_users"] / user_stats["total_users"] * 100 if user_stats["total_users"] > 0 else 0)
    ), unsafe_allow_html=True)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Course Inquiry Distribution
        st.markdown("""
            <div class="section-container">
                <div class="section-title">📚 Course Inquiry Distribution</div>
                <div class="chart-container">
        """, unsafe_allow_html=True)
        
        # Create pie chart
        fig = px.pie(
            values=course_stats['values'],
            names=course_stats['labels'],
            title='Course Inquiry Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hole=.3
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=30, b=0, l=0, r=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
            <div style="text-align: center; margin-top: 15px;">
                <div class="metric-card" style="background-color: #E3F2FD;">
                    <div class="metric-value">{course_stats['total_inquiries']}</div>
                    <div class="metric-label">📊 Total Course Inquiries</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # User Engagement Trend
        st.markdown("""
            <div class="section-container">
                <div class="section-title">📈 Daily Active Users</div>
                <div class="chart-container">
        """, unsafe_allow_html=True)
        
        # Create a DataFrame for the chart
        daily_active_df = pd.DataFrame(user_stats["daily_active_users"])
        daily_active_df['date'] = pd.to_datetime(daily_active_df['date'])
        
        # Create line chart with Plotly for better styling
        fig = px.line(
            daily_active_df,
            x='date',
            y='count',
            title='Daily Active Users (Last 7 Days)',
            labels={'count': 'Active Users', 'date': 'Date'}
        )
        
        fig.update_layout(
            height=400,
            margin=dict(t=30, b=0, l=0, r=0),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Date range selector for chat analytics
    st.markdown("""
        <div class="section-container">
            <div class="section-title">📅 Chat Analytics Date Range</div>
            <div class="date-range-container">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30),
            key="overview_start_date",
            help="Select start date for filtering data"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now(),
            key="overview_end_date",
            help="Select end date for filtering data"
        )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Get chat history
    chats = get_chat_history()
    df = pd.DataFrame(chats)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        filtered_df = df[
            (df['date'] >= start_date) & 
            (df['date'] <= end_date)
        ]
        
        # Chat Metrics
        st.markdown("""
            <div class="section-container">
                <div class="section-title">💬 Chat Metrics</div>
        """, unsafe_allow_html=True)
        
        metrics = [
            (len(filtered_df['date'].unique()), "📊 Total Sessions", "#E3F2FD"),
            (len(filtered_df), "💬 Total Messages", "#F3E5F5"),
            (9, "⏱️ Average Session Time (Mins)", "#E8F5E9"),
            (len(filtered_df['user_id'].unique()) if 'user_id' in filtered_df.columns else 0, "👥 Unique Chatters", "#FFF3E0")
        ]
        
        # Create two columns for the metrics
        col1, col2 = st.columns(2)
        
        with col1:
            for value, label, color in metrics[:2]:
                st.markdown(f"""
                    <div class="metric-card" style="background-color: {color};">
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            for value, label, color in metrics[2:]:
                st.markdown(f"""
                    <div class="metric-card" style="background-color: {color};">
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No chat history available")

def show_chat_analytics():
    st.header("Chat Analytics")
    
    # Date range selector with better styling
    st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <h3 style="color: #333; margin-bottom: 15px;">Date Range</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 4])
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30),
            key="analytics_start_date",
            help="Select start date for filtering analytics"
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now(),
            key="analytics_end_date",
            help="Select end date for filtering analytics"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Get chat history
    chats = get_chat_history()
    df = pd.DataFrame(chats)
    
    if not df.empty:
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        filtered_df = df[
            (df['date'] >= start_date) & 
            (df['date'] <= end_date)
        ]
        
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
        st.markdown("</div></div>", unsafe_allow_html=True)
        
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
    # Check for existing session
    if 'admin_session_token' not in st.session_state:
        st.session_state['admin_session_token'] = None
    
    # Verify session token
    if not st.session_state['admin_session_token'] or not verify_admin_session(st.session_state['admin_session_token']):
        show_login()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    admin_page()