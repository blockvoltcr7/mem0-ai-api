import streamlit as st
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add the project root to the Python path
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from qdrant_client import QdrantClient
import yaml
from yaml.loader import SafeLoader
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Health Coach AI - Peptide Therapy Assistant",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .health-profile-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .login-form {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Data Models
class UserHealth(BaseModel):
    """User health profile data model."""
    peptide_usage: Optional[bool] = Field(default=None, description="Whether user uses peptides")
    bpc157_usage: Optional[bool] = Field(default=None, description="Whether user uses BPC-157")
    bpc157_dosage: Optional[str] = Field(default=None, description="BPC-157 dosage")
    bpc157_duration: Optional[str] = Field(default=None, description="Duration of BPC-157 use")
    health_goals: List[str] = Field(default_factory=list, description="User's health goals")
    medical_conditions: List[str] = Field(default_factory=list, description="User's medical conditions")
    current_medications: List[str] = Field(default_factory=list, description="User's current medications")
    onboarding_completed: bool = Field(default=False, description="Whether onboarding is completed")
    onboarding_date: Optional[datetime] = Field(default=None, description="Date of onboarding completion")

class HealthCoachConfig(BaseSettings):
    """Configuration settings for the Health Coach application."""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    qdrant_url: str = Field(..., env="QDRANT_URL")
    qdrant_use_https: bool = Field(default=True, env="QDRANT_USE_HTTPS")
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

# Initialize configuration
@st.cache_resource
def get_config():
    """Get application configuration."""
    return HealthCoachConfig()

# Simple Authentication System
@st.cache_data
def load_user_config():
    """Load user configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config
    except Exception as e:
        st.error(f"Failed to load user configuration: {str(e)}")
        return None

def authenticate_user(username: str, password: str) -> Optional[Dict[str, str]]:
    """Authenticate user with simple username/password check."""
    config = load_user_config()
    if not config:
        return None
    
    users = config.get('credentials', {}).get('usernames', {})
    if username in users:
        user_data = users[username]
        if user_data.get('password') == password:
            return {
                'username': username,
                'name': user_data.get('name', username),
                'email': user_data.get('email', '')
            }
    return None

def render_login_form():
    """Render the login form."""
    st.markdown('<div class="main-header">🧬 Health Coach AI</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login", type="primary")
            
            if submit_button:
                if username and password:
                    user_data = authenticate_user(username, password)
                    if user_data:
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = user_data['username']
                        st.session_state['name'] = user_data['name']
                        st.session_state['email'] = user_data['email']
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials info
        st.info("""
        **Demo Credentials:**
        - Username: `demo_user`, Password: `demo123`
        - Username: `test_user`, Password: `test123`
        - Username: `admin_user`, Password: `admin123`
        """)
        
        # Show demo information
        with st.expander("ℹ️ About Health Coach AI"):
            st.markdown("""
            **Health Coach AI** is a demonstration application that showcases the power of Mem0 
            for maintaining conversational context in AI health coaching applications.
            
            **Features:**
            - 🧠 **Memory-Powered Conversations**: Uses Mem0 with Qdrant vector database
            - 🔒 **Simple Authentication**: User-specific sessions and data isolation
            - 📋 **Health Profile Management**: Comprehensive onboarding and profile tracking
            - 🧬 **Peptide Therapy Focus**: Specialized knowledge with safety emphasis
            - 💬 **Contextual Responses**: AI remembers your health profile and conversation history
            
            **Safety Notice:**
            This application is for educational purposes only. Always consult healthcare 
            professionals before starting any peptide therapy.
            """)

# Memory system initialization
@st.cache_resource
def initialize_memory_system():
    """Initialize Mem0 memory system with Qdrant backend."""
    try:
        config = get_config()
        
        # Create Qdrant client
        protocol = "https" if config.qdrant_use_https else "http"
        qdrant_client = QdrantClient(
            url=f"{protocol}://{config.qdrant_url}",
            port=None,
            timeout=30,
            prefer_grpc=False
        )
        
        # Configure Mem0
        mem0_config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "health_coach_memories",
                    "client": qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        memory = Memory.from_config(mem0_config)
        openai_client = OpenAI(api_key=config.openai_api_key)
        
        return memory, openai_client
        
    except Exception as e:
        st.error(f"Failed to initialize memory system: {str(e)}")
        return None, None

# Session state initialization
def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = False
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'email' not in st.session_state:
        st.session_state['email'] = None
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'user_health_profile' not in st.session_state:
        st.session_state['user_health_profile'] = UserHealth()

# Health profile functions
def save_health_profile(profile: UserHealth):
    """Save user health profile to session state."""
    st.session_state['user_health_profile'] = profile

def get_health_profile() -> UserHealth:
    """Get user health profile from session state."""
    return st.session_state.get('user_health_profile', UserHealth())

# Chat functions
def generate_ai_response(memory, openai_client, user_id: str, user_message: str, health_profile: UserHealth) -> str:
    """Generate AI response using Mem0 memory context and health profile."""
    try:
        # Search for relevant memories
        relevant_memories = memory.search(
            query=user_message,
            user_id=user_id,
            limit=5
        )
        
        memories_list = relevant_memories.get("results", [])
        memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
        
        # Create health profile context
        profile_context = ""
        if health_profile.onboarding_completed:
            profile_parts = []
            if health_profile.peptide_usage:
                profile_parts.append("User uses peptides")
            if health_profile.bpc157_usage:
                profile_parts.append(f"User uses BPC-157")
                if health_profile.bpc157_dosage:
                    profile_parts.append(f"BPC-157 dosage: {health_profile.bpc157_dosage}")
                if health_profile.bpc157_duration:
                    profile_parts.append(f"BPC-157 duration: {health_profile.bpc157_duration}")
            if health_profile.health_goals:
                profile_parts.append(f"Health goals: {', '.join(health_profile.health_goals)}")
            if health_profile.medical_conditions:
                profile_parts.append(f"Medical conditions: {', '.join(health_profile.medical_conditions)}")
            if health_profile.current_medications:
                profile_parts.append(f"Current medications: {', '.join(health_profile.current_medications)}")
            
            if profile_parts:
                profile_context = f"\n\nUser Health Profile:\n" + "\n".join(f"- {part}" for part in profile_parts)
        
        # Construct system prompt
        system_prompt = (
            "You are a knowledgeable AI health coach specializing in peptide therapy. "
            "You provide evidence-based information while emphasizing that peptides like BPC-157 "
            "are not FDA-approved for human use and should only be used under medical supervision. "
            "Always prioritize safety and recommend consulting healthcare professionals. "
            "Use the provided conversation history and health profile to give personalized responses."
            f"{profile_context}"
            f"\n\nRelevant conversation history:\n{memories_str}" if memories_str 
            else f"{profile_context}"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Generate response
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store conversation in memory
        conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
        memory.add(conversation_messages, user_id=user_id)
        
        return assistant_response
        
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your request: {str(e)}"

# UI Components
def render_health_profile_onboarding():
    """Render the health profile onboarding form."""
    st.markdown('<div class="main-header">🧬 Health Profile Setup</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Important Medical Disclaimer:</strong><br>
        This application is for educational purposes only. Peptides like BPC-157 are not FDA-approved 
        for human use. Always consult with a qualified healthcare professional before starting any 
        peptide therapy or making changes to your health regimen.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("health_profile_form"):
        st.subheader("📋 Basic Health Information")
        
        # Peptide usage
        peptide_usage = st.radio(
            "Do you currently use any peptides?",
            options=[None, True, False],
            format_func=lambda x: "Select an option" if x is None else ("Yes" if x else "No"),
            index=0
        )
        
        # BPC-157 specific information
        bpc157_usage = None
        bpc157_dosage = None
        bpc157_duration = None
        
        if peptide_usage:
            bpc157_usage = st.radio(
                "Do you use BPC-157 specifically?",
                options=[None, True, False],
                format_func=lambda x: "Select an option" if x is None else ("Yes" if x else "No"),
                index=0
            )
            
            if bpc157_usage:
                bpc157_dosage = st.selectbox(
                    "What is your BPC-157 dosage?",
                    options=["", "100mcg daily", "250mcg daily", "500mcg daily", "Other"],
                    index=0
                )
                
                if bpc157_dosage == "Other":
                    bpc157_dosage = st.text_input("Please specify your dosage:")
                
                bpc157_duration = st.selectbox(
                    "How long have you been using BPC-157?",
                    options=["", "Less than 1 week", "1-2 weeks", "2-4 weeks", "1-3 months", "More than 3 months"],
                    index=0
                )
        
        # Health goals
        st.subheader("🎯 Health Goals")
        health_goals = st.multiselect(
            "What are your primary health goals? (Select all that apply)",
            options=[
                "Tissue repair and healing",
                "Injury recovery",
                "Gut health improvement", 
                "Inflammation reduction",
                "Athletic performance",
                "General wellness",
                "Other"
            ]
        )
        
        if "Other" in health_goals:
            other_goal = st.text_input("Please specify your other health goal:")
            if other_goal:
                health_goals = [goal for goal in health_goals if goal != "Other"] + [other_goal]
        
        # Medical conditions
        st.subheader("🏥 Medical History")
        medical_conditions = st.multiselect(
            "Do you have any of the following medical conditions? (Select all that apply)",
            options=[
                "None",
                "Diabetes",
                "Heart disease",
                "High blood pressure",
                "Autoimmune conditions",
                "Digestive issues",
                "Chronic pain",
                "Other"
            ]
        )
        
        if "Other" in medical_conditions:
            other_condition = st.text_input("Please specify your other medical condition:")
            if other_condition:
                medical_conditions = [cond for cond in medical_conditions if cond != "Other"] + [other_condition]
        
        # Current medications
        current_medications_text = st.text_area(
            "List any current medications or supplements (one per line):",
            placeholder="e.g.\nVitamin D\nOmega-3\nMetformin"
        )
        
        current_medications = [med.strip() for med in current_medications_text.split('\n') if med.strip()]
        
        # Submit button
        submitted = st.form_submit_button("Complete Health Profile Setup", type="primary")
        
        if submitted:
            # Validate required fields
            if peptide_usage is None:
                st.error("Please indicate whether you use peptides.")
                return
            
            if peptide_usage and bpc157_usage is None:
                st.error("Please indicate whether you use BPC-157.")
                return
            
            if bpc157_usage and not bpc157_dosage:
                st.error("Please specify your BPC-157 dosage.")
                return
            
            if bpc157_usage and not bpc157_duration:
                st.error("Please specify how long you've been using BPC-157.")
                return
            
            # Create and save health profile
            profile = UserHealth(
                peptide_usage=peptide_usage,
                bpc157_usage=bpc157_usage,
                bpc157_dosage=bpc157_dosage if bpc157_dosage else None,
                bpc157_duration=bpc157_duration if bpc157_duration else None,
                health_goals=health_goals,
                medical_conditions=medical_conditions,
                current_medications=current_medications,
                onboarding_completed=True,
                onboarding_date=datetime.now()
            )
            
            save_health_profile(profile)
            
            st.markdown("""
            <div class="success-box">
                <strong>✅ Health Profile Completed!</strong><br>
                Your health profile has been saved. You can now start chatting with your AI health coach.
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2)
            st.rerun()

def render_health_profile_summary():
    """Render a summary of the user's health profile."""
    profile = get_health_profile()
    
    if not profile.onboarding_completed:
        return
    
    with st.expander("📋 Your Health Profile", expanded=False):
        st.markdown('<div class="health-profile-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Peptide Usage:**", "Yes" if profile.peptide_usage else "No")
            if profile.bpc157_usage:
                st.write("**BPC-157 Usage:**", "Yes")
                st.write("**Dosage:**", profile.bpc157_dosage or "Not specified")
                st.write("**Duration:**", profile.bpc157_duration or "Not specified")
        
        with col2:
            if profile.health_goals:
                st.write("**Health Goals:**")
                for goal in profile.health_goals:
                    st.write(f"• {goal}")
            
            if profile.medical_conditions and "None" not in profile.medical_conditions:
                st.write("**Medical Conditions:**")
                for condition in profile.medical_conditions:
                    st.write(f"• {condition}")
        
        if profile.current_medications:
            st.write("**Current Medications:**")
            for med in profile.current_medications:
                st.write(f"• {med}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Update Health Profile"):
            # Reset onboarding to allow updates
            profile.onboarding_completed = False
            save_health_profile(profile)
            st.rerun()

def render_chat_interface():
    """Render the main chat interface."""
    st.markdown('<div class="main-header">🤖 AI Health Coach</div>', unsafe_allow_html=True)
    
    # Initialize memory system
    memory, openai_client = initialize_memory_system()
    
    if memory is None or openai_client is None:
        st.error("Failed to initialize the AI system. Please check your configuration.")
        return
    
    # Health profile summary
    render_health_profile_summary()
    
    # Chat history
    st.subheader("💬 Conversation")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 AI Coach:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask your AI health coach about peptide therapy...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.spinner("🤔 AI Coach is thinking..."):
            user_id = st.session_state.username
            health_profile = get_health_profile()
            
            ai_response = generate_ai_response(
                memory, openai_client, user_id, user_input, health_profile
            )
        
        # Add AI response to history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Rerun to display new messages
        st.rerun()

def render_sidebar():
    """Render the sidebar with user information and controls."""
    with st.sidebar:
        st.markdown("### 👤 User Information")
        st.write(f"**Name:** {st.session_state.name}")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Email:** {st.session_state.email}")
        
        st.markdown("---")
        
        # Memory statistics
        st.markdown("### 📊 Session Stats")
        st.write(f"**Messages:** {len(st.session_state.chat_history)}")
        
        profile = get_health_profile()
        if profile.onboarding_completed:
            st.write("**Profile:** ✅ Complete")
            st.write(f"**Setup Date:** {profile.onboarding_date.strftime('%Y-%m-%d') if profile.onboarding_date else 'Unknown'}")
        else:
            st.write("**Profile:** ❌ Incomplete")
        
        st.markdown("---")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Logout
        if st.button("🚪 Logout"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Main application
def main():
    """Main application function."""
    initialize_session_state()
    
    # Check authentication status
    if not st.session_state.get('authentication_status', False):
        render_login_form()
    else:
        # User is authenticated
        render_sidebar()
        
        # Check if user needs onboarding
        health_profile = get_health_profile()
        
        if not health_profile.onboarding_completed:
            render_health_profile_onboarding()
        else:
            render_chat_interface()

if __name__ == "__main__":
    main() 