import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import pytz
from database import init_database, get_course_data, save_chat

# Must be the first Streamlit command
st.set_page_config(
    page_title="University Course Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize database
init_database()

# Configure Gemini AI
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Get course data from database
data = {"courses": get_course_data()}

# Create a context for the AI
context = f"""
You are a helpful university admission counselor chatbot. You have information about the following courses:

{json.dumps(data, indent=2)}

Key points to remember:
1. Always be polite and professional
2. Provide accurate information about courses based on the data provided
3. Handle general queries and greetings naturally
4. If asked about information not in the data, politely say you can only provide information about the listed courses
5. Keep responses concise but informative
6. Use appropriate emojis to make responses engaging
7. Format responses using markdown for better readability

Example interactions:
- Greet users warmly
- Answer questions about course duration, fees, and subjects
- Provide guidance on admission process
- Handle small talk naturally
- Stay focused on academic and admission related queries
"""

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # This will store (user_msg, bot_msg, timestamp) tuples
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

def get_ai_response(user_input):
    try:
        prompt = f"Context: {context}\n\nUser: {user_input}\n\nResponse:"
        response = st.session_state.chat.send_message(prompt)
        save_chat(user_input, response.text)
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error. Please try asking your question again. Error: {str(e)}"

# Example questions
example_questions = [
    "Hi! Can you help me with course information?",
    "What courses do you offer?",
    "Tell me about B.Tech program",
    "What is the fee structure for BCA?",
    "What subjects are taught in B.Sc first semester?",
    "How long is the B.Tech program?",
    "What are the subjects in BCA?",
    "Tell me about admission process",
    "What is the duration of B.Sc?",
    "Can you compare B.Tech and BCA programs?"
]

def set_question(question):
    st.session_state.current_question = question

# Custom CSS (same as before)
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        height: 42px;
        margin-top: 6%;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #E3F2FD;
    }
    .bot-message {
        background-color: #F5F5F5;
    }
    .example-question {
        background-color: #f8f9fa;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .example-question:hover {
        background-color: #e9ecef;
        transform: translateX(5px);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("./Resources/Logo.png", caption="University Logo")
    st.title("Course Assistant")
    st.markdown("---")
    st.info("👋 Welcome to our interactive course assistant! I'm here to help you explore our academic programs and answer your questions about admissions.")
    
    # Example Questions Section
    st.markdown("### 💭 Example Questions")
    st.markdown("Click on any question to try it out:")
    
    for question in example_questions:
        if st.button(f"🔹 {question}", key=f"btn_{question}", 
                    help="Click to ask this question",
                    use_container_width=True):
            set_question(question)
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("• [University Website](#)")
    st.markdown("• [Admission Portal](#)")
    st.markdown("• [Student Dashboard](#)")
    
    st.markdown("### 📞 Contact Support")
    st.markdown("📞 Helpline: 1800-XXX-XXXX")
    st.markdown("📧 Email: admissions@university.edu")

# Main chat interface
st.title("🎓 University Course Assistant")
st.markdown("---")

# Chat container
chat_container = st.container()

# Display chat history
for message_data in st.session_state.chat_history:
    with chat_container:
        col1, col2 = st.columns([6,4])
        
        # Handle both formats of chat history (with and without timestamp)
        if len(message_data) == 3:
            user, bot, timestamp = message_data
        else:
            user, bot = message_data
            timestamp = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M')
            
        with col1:
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {user}
                    <small style="color: gray;">{timestamp}</small>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Assistant:</strong> {bot}
                </div>
                <small style="color: gray;">{timestamp}</small>
            """, unsafe_allow_html=True)

# Input container
st.markdown("---")
input_col1, input_col2 = st.columns([6, 1])
with input_col1:
    user_input = st.text_input("Ask your question here...", 
                              value=st.session_state.current_question,
                              key="input", 
                              placeholder="e.g., What courses do you offer?")
with input_col2:
    st.text(" ")
    send_button = st.button("Send 📤", use_container_width=True)

if send_button and user_input:
    # Get AI response
    ai_response = get_ai_response(user_input)
    
    # Get current time in IST
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M')
    
    # Update chat history with timestamp
    st.session_state.chat_history.append((user_input, ai_response, current_time))
    
    # Clear input
    st.session_state.current_question = ""
    st.rerun()

# Footer
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        © 2025 Brijesh Adeshara. All rights reserved.
    </div>
    """, 
    unsafe_allow_html=True
)
