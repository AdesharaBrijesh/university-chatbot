from pymongo import MongoClient
from datetime import datetime, timedelta
import streamlit as st
import bcrypt
import uuid
import json
from user_agents import parse
import pytz

# MongoDB connection
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client['university_chatbot']

# Collections
chat_collection = db['chat_history']
course_data_collection = db['course_data']
admin_collection = db['admins']
user_collection = db['users']

def init_database():
    """Initialize database with default admin and course data if empty"""
    # Add default admin if none exists
    if admin_collection.count_documents({}) == 0:
        default_admin = {
            "username": "admin",
            "password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        }
        admin_collection.insert_one(default_admin)

    # Add default course data if none exists
    if course_data_collection.count_documents({}) == 0:
        default_courses = {
            "courses": {
                "B.Tech": {
                    "duration": "4 years",
                    "fees": "60,000 INR per semester",
                    "semesters": 8,
                    "subjects": {
                        "Sem 1": ["Mathematics 1", "Physics", "Chemistry", "Engineering Mechanics", "Computer Programming"]
                    }
                },
                "B.Sc": {
                    "duration": "3 years",
                    "fees": "40,000 INR per semester",
                    "semesters": 6,
                    "subjects": {
                        "Sem 1": ["Biology", "Chemistry", "Physics", "Mathematics", "Computer Applications"]
                    }
                },
                "BCA": {
                    "duration": "3 years",
                    "fees": "50,000 INR per semester",
                    "semesters": 6,
                    "subjects": {
                        "Sem 1": ["C Programming", "Digital Electronics", "Mathematics", "Statistics", "English"]
                    }
                }
            }
        }
        course_data_collection.insert_one(default_courses)

def verify_admin(username, password):
    """Verify admin credentials and create session"""
    admin = admin_collection.find_one({"username": username})
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password']):
        # Create a session token
        session_token = str(uuid.uuid4())
        admin_collection.update_one(
            {"username": username},
            {"$set": {"session_token": session_token, "last_login": datetime.now()}}
        )
        return session_token
    return None

def verify_admin_session(session_token):
    """Verify admin session token"""
    if not session_token:
        return False
    try:
        # Check if session exists and is not expired (24 hours validity)
        admin = admin_collection.find_one({
            "session_token": session_token,
            "last_login": {"$gte": datetime.now() - timedelta(days=1)}
        })
        if admin:
            # Update last login time to extend session
            admin_collection.update_one(
                {"session_token": session_token},
                {"$set": {"last_login": datetime.now()}}
            )
            return True
        return False
    except:
        return False

def get_browser_fingerprint():
    """Generate a simple browser fingerprint"""
    user_agent = st.request_header("User-Agent", "")
    user_agent_info = parse(user_agent)
    fingerprint = {
        "browser": user_agent_info.browser.family,
        "os": user_agent_info.os.family,
        "device": user_agent_info.device.family,
        "ip": st.request_header("X-Forwarded-For", "").split(",")[0].strip()
    }
    return json.dumps(fingerprint)

def get_or_create_user_session():
    """Get or create a user session with improved tracking."""
    if 'user_id' not in st.session_state:
        user_id = str(uuid.uuid4())
        st.session_state.user_id = user_id
        
        # Create new user record
        user_collection.insert_one({
            'user_id': user_id,
            'created_at': datetime.now(),
            'last_active': datetime.now(),
            'access_count': 1
        })
    else:
        user_id = st.session_state.user_id
        
        # Update existing user's last active time and increment access count
        user_collection.update_one(
            {'user_id': user_id},
            {
                '$set': {'last_active': datetime.now()},
                '$inc': {'access_count': 1}
            }
        )
    
    return user_id

def save_chat(user_message, bot_response):
    """Save chat history to database with user ID and course inquiry tracking"""
    try:
        user_id = get_or_create_user_session()
        
        # Extract course information from the message
        courses = get_course_data()
        course_inquiry = None
        for course in courses.keys():
            if course.lower() in user_message.lower():
                course_inquiry = course
                break
        
        chat_data = {
            "timestamp": datetime.now(pytz.timezone('Asia/Kolkata')),
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "course_inquiry": course_inquiry
        }
        chat_collection.insert_one(chat_data)
    except Exception as e:
        st.error("An error occurred while saving the chat. Please try again.")
        print(f"Error saving chat: {str(e)}")  # Log the error for debugging

def get_chat_history(user_id=None):
    """Get chat history, optionally filtered by user_id"""
    query = {}
    if user_id:
        query["user_id"] = user_id
    return list(chat_collection.find(query).sort("timestamp", -1))

def get_course_data():
    """Get course data"""
    data = course_data_collection.find_one()
    return data['courses'] if data else {}

def update_course_data(courses):
    """Update course data"""
    course_data_collection.update_one(
        {}, 
        {"$set": {"courses": courses}}, 
        upsert=True
    )

def get_user_stats():
    """Get comprehensive user statistics."""
    try:
        now = datetime.now(pytz.timezone('Asia/Kolkata'))
        today_start = datetime.combine(now.date(), datetime.min.time())
        week_start = today_start - timedelta(days=7)
        month_start = today_start - timedelta(days=30)
        
        # Total users
        total_users = user_collection.count_documents({})
        
        # Active users today
        active_today = user_collection.count_documents({
            'last_active': {'$gte': today_start}
        })
        
        # New users today
        new_users_today = user_collection.count_documents({
            'created_at': {'$gte': today_start}
        })
        
        # Active users this week
        active_this_week = user_collection.count_documents({
            'last_active': {'$gte': week_start}
        })
        
        # Active users this month
        active_this_month = user_collection.count_documents({
            'last_active': {'$gte': month_start}
        })
        
        # Returning users
        returning_users = user_collection.count_documents({
            'access_count': {'$gt': 1}
        })
        
        # Daily active users for the last 7 days
        pipeline = [
            {
                '$match': {
                    'last_active': {'$gte': week_start}
                }
            },
            {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$last_active'
                        }
                    },
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]
        
        daily_active = list(user_collection.aggregate(pipeline))
        
        # Ensure we have data for all 7 days
        daily_active_users = []
        for i in range(7):
            date = (today_start - timedelta(days=i)).strftime('%Y-%m-%d')
            count = next((item['count'] for item in daily_active if item['_id'] == date), 0)
            daily_active_users.append({
                'date': date,
                'count': count
            })
        
        daily_active_users.sort(key=lambda x: x['date'])
        
        return {
            'total_users': total_users,
            'active_today': active_today,
            'new_users_today': new_users_today,
            'active_this_week': active_this_week,
            'active_this_month': active_this_month,
            'returning_users': returning_users,
            'daily_active_users': daily_active_users
        }
    except Exception as e:
        print(f"Error fetching user stats: {str(e)}")
        return {}

def get_course_inquiry_stats():
    """Get statistics about course inquiries"""
    pipeline = [
        {
            '$match': {
                'course_inquiry': {'$ne': None}
            }
        },
        {
            '$group': {
                '_id': '$course_inquiry',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        }
    ]
    
    course_stats = list(chat_collection.aggregate(pipeline))
    
    # Convert to format suitable for pie chart
    total_inquiries = sum(stat['count'] for stat in course_stats)
    course_distribution = {
        'labels': [stat['_id'] for stat in course_stats],
        'values': [stat['count'] for stat in course_stats],
        'total_inquiries': total_inquiries
    }
    
    return course_distribution
