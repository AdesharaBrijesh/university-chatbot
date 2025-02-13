from pymongo import MongoClient
from datetime import datetime
import streamlit as st
import bcrypt

# MongoDB connection
MONGO_URI = st.secrets["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client['university_chatbot']

# Collections
chat_collection = db['chat_history']
course_data_collection = db['course_data']
admin_collection = db['admins']

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
    """Verify admin credentials"""
    admin = admin_collection.find_one({"username": username})
    if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password']):
        return True
    return False

def save_chat(user_message, bot_response):
    """Save chat history to database"""
    chat_data = {
        "timestamp": datetime.now(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    chat_collection.insert_one(chat_data)

def get_chat_history():
    """Get all chat history"""
    return list(chat_collection.find().sort("timestamp", -1))

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
