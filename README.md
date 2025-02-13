# 🎓 University Course Assistant Chatbot 🤖

Welcome to the **University Course Assistant Chatbot** – your AI-powered guide for navigating university courses, admissions, and campus life! Built with cutting-edge AI and designed for students by students. 🌟

![Chatbot Demo](https://via.placeholder.com/800x400.png?text=Chatbot+Interface+Demo)
*Interactive chat interface with real-time responses*

---

## 🚀 Features That Make Life Easier

### 🤖 **Smart Conversational AI**
- Natural Q/A about courses, fees, subjects, and admission criteria
- Context-aware responses powered by **Google Gemini Pro**
- Handles both general and specific university queries

### 📊 **Admin Power Dashboard**
- **Real-time Analytics**: Visualize chat trends and user interactions
- **Data Management**: Update course info, fees, and university details
- **Export Magic**: Download chat histories as CSV with one click
- **User Insights**: Track popular queries and response effectiveness

### � **Always Learning**
- MongoDB database stores conversations for continuous improvement
- Modular architecture for easy feature additions
- Daily backup system for data security

### 💬 Rich Interaction
- Persistent chat history (never lose your conversation!)
- Quick-action sidebar with sample questions
- Support ticket integration for human assistance

---

## 🛠️ Tech Stack Powering the Magic

| **Area**       | **Technologies**                                                                 |
|-----------------|----------------------------------------------------------------------------------|
| **AI Engine**   | ![Google Gemini](https://img.shields.io/badge/Google_Gemini_Pro-4285F4?style=flat&logo=google&logoColor=white) |
| **Backend**     | ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white) |
| **Frontend**    | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) |
<!-- | **DevOps**      | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white) | -->

---

## ⚡ Quick Start Guide

### Prerequisites
- Python 3.10+
- Google Cloud account (for Gemini API)
- MongoDB Atlas account (free tier works!)

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdesharaBrijesh/university-chatbot.git
   cd university-chatbot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure secrets**
   Create `.streamlit/secrets.toml` with:
   ```toml
   GOOGLE_API_KEY = "your_google_api_key"
   MONGO_URI = "your_mongodb_connection_string"
   ```

5. **Launch the app!**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Live Demo & Admin Access

👉 **Public Chat Interface**: [Live Demo](https://university-chatbot-brijesh.streamlit.app/)  
🔒 **Admin Dashboard**: `/admin` route (password protected)

*Admin credentials available to contributors – reach out!*

---

## 📸 See It in Action

| **Chat Interface** | **Admin Dashboard** |
|--------------------|----------------------|
| ![Chat Preview](https://via.placeholder.com/400x250.png?text=Student+View) | ![Admin Preview](https://via.placeholder.com/400x250.png?text=Admin+View) |

---

## 🤝 How to Contribute

We 💜 contributors! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch:  
   `git checkout -b amazing-feature`
3. **Commit** your changes:  
   `git commit -m 'Add some amazing feature'`
4. **Push** to the branch:  
   `git push origin amazing-feature`
5. Open a **Pull Request**

**First time contributing?** Check our [Good First Issues](https://github.com/AdesharaBrijesh/university-chatbot/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)!

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❓ Need Help? Found a Bug?

Open an [issue](https://github.com/AdesharaBrijesh/university-chatbot/issues) or reach out to our team:

📧 **Email**: [adesharabrijesh8@gmail.com](mailto:adesharabrijesh8@gmail.com)  
<!-- 💬 **Discord**: [Join our server](https://discord.gg/your-invite-link) -->

---

Made with ❤️ by Brijesh Adeshara and **AMAZING CONTRIBUTORS** like YOU!  

[![Star on GitHub](https://img.shields.io/github/stars/AdesharaBrijesh/university-chatbot.svg?style=social)](https://github.com/AdesharaBrijesh/university-chatbot/stargazers)  
*Give us a star if you find this useful!* ⭐