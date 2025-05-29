"""
Health Coach AI - Peptide Therapy Assistant (Gradio)
Converted from Streamlit to Gradio with same functionality and 3 demo users.
"""

import gradio as gr
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
import logging
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from qdrant_client import QdrantClient
from pydantic import BaseModel, Field, ValidationError

# Load environment variables from parent directory
load_dotenv(Path(__file__).parent.parent / ".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_USE_HTTPS = os.getenv("QDRANT_USE_HTTPS", "false").lower() == "true"

# Demo Users Configuration
DEMO_USERS = {
    "john": {
        "name": "John Smith",
        "email": "john@healthcoach.ai",
        "user_id": "john_demo_user"
    },
    "jane": {
        "name": "Jane Doe", 
        "email": "jane@healthcoach.ai",
        "user_id": "jane_demo_user"
    },
    "jarvis": {
        "name": "Jarvis Wilson",
        "email": "jarvis@healthcoach.ai", 
        "user_id": "jarvis_demo_user"
    }
}

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

# Global variables for services
memory_service = None
openai_client = None
user_profiles = {}  # Store user profiles in memory

def initialize_services():
    """Initialize Mem0 and OpenAI services."""
    global memory_service, openai_client
    
    try:
        # Initialize OpenAI client
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Create Qdrant client
        protocol = "https" if QDRANT_USE_HTTPS else "http"
        qdrant_client = QdrantClient(
            url=f"{protocol}://{QDRANT_URL}",
            port=None,
            timeout=30,
            prefer_grpc=False
        )
        
        # Generate unique collection name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_name = f"health_coach_memories_{timestamp}"
        
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
                    "collection_name": collection_name,
                    "client": qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        memory_service = Memory.from_config(mem0_config)
        logger.info(f"Services initialized successfully with collection: {collection_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        return False

def save_health_profile_to_memory(user_id: str, profile: UserHealth):
    """Save health profile to Mem0 for persistence."""
    try:
        profile_data = {
            "type": "health_profile",
            "peptide_usage": profile.peptide_usage,
            "bpc157_usage": profile.bpc157_usage,
            "bpc157_dosage": profile.bpc157_dosage,
            "bpc157_duration": profile.bpc157_duration,
            "health_goals": profile.health_goals,
            "medical_conditions": profile.medical_conditions,
            "current_medications": profile.current_medications,
            "onboarding_completed": profile.onboarding_completed,
            "onboarding_date": profile.onboarding_date.isoformat() if profile.onboarding_date else None
        }
        
        # Store as a memory with specific metadata
        memory_service.add(
            f"User health profile: {json.dumps(profile_data)}",
            user_id=user_id,
            metadata={"type": "health_profile"}
        )
        logger.info(f"Health profile saved to memory for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to save health profile to memory: {str(e)}")

def load_health_profile_from_memory(user_id: str) -> Optional[UserHealth]:
    """Load health profile from Mem0 if it exists."""
    try:
        # Search for health profile memories
        results = memory_service.search(
            query="health profile peptide usage BPC-157",
            user_id=user_id,
            limit=10
        )
        
        # Look for health profile data
        for result in results.get("results", []):
            memory_text = result.get("memory", "")
            if "User health profile:" in memory_text and '"type": "health_profile"' in memory_text:
                # Extract JSON data
                json_start = memory_text.find("{")
                if json_start != -1:
                    profile_json = memory_text[json_start:]
                    profile_data = json.loads(profile_json)
                    
                    # Reconstruct UserHealth object
                    onboarding_date = None
                    if profile_data.get("onboarding_date"):
                        onboarding_date = datetime.fromisoformat(profile_data["onboarding_date"])
                    
                    profile = UserHealth(
                        peptide_usage=profile_data.get("peptide_usage"),
                        bpc157_usage=profile_data.get("bpc157_usage"),
                        bpc157_dosage=profile_data.get("bpc157_dosage"),
                        bpc157_duration=profile_data.get("bpc157_duration"),
                        health_goals=profile_data.get("health_goals", []),
                        medical_conditions=profile_data.get("medical_conditions", []),
                        current_medications=profile_data.get("current_medications", []),
                        onboarding_completed=profile_data.get("onboarding_completed", False),
                        onboarding_date=onboarding_date
                    )
                    
                    logger.info(f"Health profile loaded from memory for user {user_id}")
                    return profile
                    
    except Exception as e:
        logger.error(f"Failed to load health profile from memory: {str(e)}")
    
    return None

def get_user_profile(user_id: str) -> UserHealth:
    """Get user health profile from memory or load from Mem0."""
    if user_id not in user_profiles:
        # Try to load from Mem0 first
        stored_profile = load_health_profile_from_memory(user_id)
        if stored_profile:
            user_profiles[user_id] = stored_profile
        else:
            user_profiles[user_id] = UserHealth()
    return user_profiles[user_id]

def save_user_profile(user_id: str, profile: UserHealth):
    """Save user health profile to both memory and Mem0."""
    user_profiles[user_id] = profile
    # Also save to Mem0 for persistence
    save_health_profile_to_memory(user_id, profile)

def create_user_session(selected_user: str) -> Tuple[str, str, str, str]:
    """Create or validate user session."""
    if not selected_user or selected_user == "Select a user...":
        return "", "", "", "❌ Please select a user to continue."
    
    user_data = DEMO_USERS.get(selected_user)
    if not user_data:
        return "", "", "", "❌ Invalid user selection."
    
    user_id = user_data["user_id"]
    user_name = user_data["name"]
    user_email = user_data["email"]
    
    # Get user profile (this will now load from Mem0 if available)
    profile = get_user_profile(user_id)
    
    if profile.onboarding_completed:
        status_msg = f"✅ Welcome back, {user_name}! Your health profile is loaded. Ready to chat!"
    else:
        status_msg = f"✅ Logged in as {user_name}. You can start chatting or complete your health profile for personalized advice."
    
    return user_id, user_name, user_email, status_msg

def generate_ai_response_stream(user_id: str, user_message: str, health_profile: UserHealth):
    """Generate streaming AI response using Mem0 memory context and health profile."""
    try:
        # Search for relevant memories
        relevant_memories = memory_service.search(
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
        else:
            profile_context = "\n\nNote: User hasn't completed their health profile yet. Provide general information and encourage them to complete their profile for personalized advice."
        
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
        
        # Initialize response accumulator
        assistant_response = ""
        
        # Stream the response from OpenAI
        stream = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )
        
        # Process streaming response
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                assistant_response += chunk_content
                yield chunk_content, assistant_response
        
        # Store conversation in memory after streaming completes
        try:
            conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
            memory_service.add(conversation_messages, user_id=user_id)
        except Exception as e:
            logger.error(f"Error storing conversation: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        error_msg = f"I apologize, but I encountered an error while processing your request: {str(e)}"
        yield error_msg, error_msg

def chat_with_coach(message: str, history: List[Dict], user_id: str):
    """Handle chat interaction with the AI health coach with streaming responses."""
    if not user_id:
        error_message = {"role": "assistant", "content": "Please select a user first to start chatting."}
        yield "", history + [error_message]
        return
    
    if not message.strip():
        yield "", history
        return
    
    # Get user health profile
    health_profile = get_user_profile(user_id)
    
    # Add user message to history immediately
    new_history = history + [{"role": "user", "content": message}]
    yield "", new_history
    
    # Add empty assistant message that we'll stream into
    new_history = new_history + [{"role": "assistant", "content": ""}]
    
    # Stream the AI response
    try:
        for chunk_content, full_response in generate_ai_response_stream(user_id, message, health_profile):
            # Update the last message in history with the accumulated response
            new_history[-1]["content"] = full_response
            yield "", new_history
    except Exception as e:
        logger.error(f"Error in chat streaming: {str(e)}")
        error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        new_history[-1]["content"] = error_response
        yield "", new_history

def clear_chat_history(user_id: str) -> Tuple[List, str]:
    """Clear chat history."""
    if not user_id:
        return [], "Please select a user first."
    return [], "Chat history cleared. How can I help you with your peptide therapy questions?"

def complete_health_profile(user_id: str, peptide_usage: str, bpc157_usage: str, 
                          bpc157_dosage: str, bpc157_duration: str, health_goals: List[str],
                          medical_conditions: List[str], medications_text: str) -> Tuple[str, bool]:
    """Complete user health profile setup."""
    if not user_id:
        return "❌ Please select a user first.", False
    
    try:
        # Parse peptide usage
        if peptide_usage == "Select an option":
            return "❌ Please indicate whether you use peptides.", False
        peptide_bool = peptide_usage == "Yes"
        
        # Parse BPC-157 usage
        bpc157_bool = None
        if peptide_bool:
            if bpc157_usage == "Select an option":
                return "❌ Please indicate whether you use BPC-157.", False
            bpc157_bool = bpc157_usage == "Yes"
            
            if bpc157_bool:
                if not bpc157_dosage or bpc157_dosage == "Select dosage":
                    return "❌ Please specify your BPC-157 dosage.", False
                if not bpc157_duration or bpc157_duration == "Select duration":
                    return "❌ Please specify how long you've been using BPC-157.", False
        
        # Parse medications
        medications = [med.strip() for med in medications_text.split('\n') if med.strip()] if medications_text else []
        
        # Create and save health profile
        profile = UserHealth(
            peptide_usage=peptide_bool,
            bpc157_usage=bpc157_bool,
            bpc157_dosage=bpc157_dosage if bpc157_bool else None,
            bpc157_duration=bpc157_duration if bpc157_bool else None,
            health_goals=health_goals,
            medical_conditions=medical_conditions,
            current_medications=medications,
            onboarding_completed=True,
            onboarding_date=datetime.now()
        )
        
        save_user_profile(user_id, profile)
        
        return "✅ Health profile completed successfully! You can now start chatting with your AI health coach.", True
        
    except Exception as e:
        logger.error(f"Error completing health profile: {str(e)}")
        return f"❌ Error saving profile: {str(e)}", False

def get_health_profile_summary(user_id: str) -> str:
    """Get formatted health profile summary."""
    if not user_id:
        return "Please select a user first."
    
    profile = get_user_profile(user_id)
    
    if not profile.onboarding_completed:
        # Check if this is a completely new profile or user skipped
        has_any_data = (
            profile.peptide_usage is not None or 
            profile.bpc157_usage is not None or 
            profile.health_goals or 
            profile.medical_conditions or 
            profile.current_medications
        )
        
        if has_any_data:
            return "## 📋 Health Profile Status\n\n**Status:** Partially completed\n\nYou can continue chatting with general advice or complete your profile for personalized recommendations."
        else:
            return "## 📋 Health Profile Status\n\n**Status:** Not started\n\nYou can start chatting immediately for general advice, or complete your health profile for personalized recommendations tailored to your specific needs."
    
    summary_parts = ["## 📋 Your Health Profile\n"]
    
    # Basic peptide info
    summary_parts.append(f"**Peptide Usage:** {'Yes' if profile.peptide_usage else 'No'}")
    
    if profile.bpc157_usage:
        summary_parts.append(f"**BPC-157 Usage:** Yes")
        summary_parts.append(f"**Dosage:** {profile.bpc157_dosage or 'Not specified'}")
        summary_parts.append(f"**Duration:** {profile.bpc157_duration or 'Not specified'}")
    elif profile.bpc157_usage is False:
        summary_parts.append(f"**BPC-157 Usage:** No")
    
    # Health goals
    if profile.health_goals:
        summary_parts.append(f"\n**Health Goals:**")
        for goal in profile.health_goals:
            summary_parts.append(f"• {goal}")
    
    # Medical conditions
    if profile.medical_conditions and "None" not in profile.medical_conditions:
        summary_parts.append(f"\n**Medical Conditions:**")
        for condition in profile.medical_conditions:
            summary_parts.append(f"• {condition}")
    elif "None" in profile.medical_conditions:
        summary_parts.append(f"\n**Medical Conditions:** None reported")
    
    # Medications
    if profile.current_medications:
        summary_parts.append(f"\n**Current Medications:**")
        for med in profile.current_medications:
            summary_parts.append(f"• {med}")
    
    summary_parts.append(f"\n**Profile Completed:** {profile.onboarding_date.strftime('%Y-%m-%d %H:%M') if profile.onboarding_date else 'Unknown'}")
    summary_parts.append(f"\n*Your profile is stored persistently and will be available in future sessions.*")
    
    return "\n".join(summary_parts)

def reset_user_profile(user_id: str) -> Tuple[str, str, str, str, List, List, str]:
    """Reset user health profile for re-onboarding."""
    if not user_id:
        return "Select an option", "Select an option", "Select dosage", "Select duration", [], [], ""
    
    # Reset profile
    profile = UserHealth()
    save_user_profile(user_id, profile)
    
    return "Select an option", "Select an option", "Select dosage", "Select duration", [], [], ""

# Initialize services on startup
services_initialized = initialize_services()

def create_interface():
    """Create the Gradio interface."""
    
    with gr.Blocks(title="Health Coach AI - Peptide Therapy Assistant", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🧬 Health Coach AI - Peptide Therapy Assistant
        
        Welcome to your AI-powered health coach specializing in peptide therapy education and guidance.
        
        **⚠️ Important Medical Disclaimer:**  
        This application is for educational purposes only. Peptides like BPC-157 are not FDA-approved for human use. Always consult with qualified healthcare professionals before starting any peptide therapy.
        
        **Features:**
        - 🧠 **Memory-Powered Conversations**: Remembers your health profile and conversation history
        - 🧬 **Peptide Therapy Focus**: Specialized knowledge in peptide therapy and safety
        - 👥 **Demo Users**: Choose from John, Jane, or Jarvis for testing
        - 📋 **Health Profile Management**: Comprehensive onboarding and profile tracking
        - ⚡ **Real-time Streaming**: Get immediate response as the AI generates answers
        - 🔄 **Fresh Sessions**: Each app restart creates a new memory collection for clean testing
        """)
        
        if not services_initialized:
            gr.Markdown("⚠️ **Service Initialization Error**: Please check your environment variables (OPENAI_API_KEY, QDRANT_URL)")
            return app
        
        # User selection section
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 👤 User Selection")
                user_dropdown = gr.Dropdown(
                    label="Select Demo User",
                    choices=["Select a user...", "john", "jane", "jarvis"],
                    value="Select a user...",
                    interactive=True
                )
                login_btn = gr.Button("🔑 Login as Selected User", variant="primary")
                
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Session Status")
                session_status = gr.Textbox(
                    label="Status",
                    value="Please select a user to begin",
                    interactive=False
                )
                current_user = gr.State("")
                current_user_name = gr.State("")
                current_user_email = gr.State("")
        
        # Main interface with tabs
        with gr.Tabs():
            # Health Profile Setup Tab
            with gr.TabItem("📋 Health Profile Setup"):
                gr.Markdown("### Complete Your Health Profile")
                gr.Markdown("*Optional: Complete your health profile for personalized recommendations, or skip to chat with general advice.*")
                
                with gr.Row():
                    with gr.Column():
                        peptide_usage = gr.Dropdown(
                            label="Do you currently use any peptides?",
                            choices=["Select an option", "Yes", "No"],
                            value="Select an option"
                        )
                        
                        bpc157_usage = gr.Dropdown(
                            label="Do you use BPC-157 specifically?",
                            choices=["Select an option", "Yes", "No"],
                            value="Select an option"
                        )
                        
                        bpc157_dosage = gr.Dropdown(
                            label="BPC-157 Dosage",
                            choices=["Select dosage", "100mcg daily", "250mcg daily", "500mcg daily", "Other"],
                            value="Select dosage"
                        )
                        
                        bpc157_duration = gr.Dropdown(
                            label="Duration of BPC-157 use",
                            choices=["Select duration", "Less than 1 week", "1-2 weeks", "2-4 weeks", "1-3 months", "More than 3 months"],
                            value="Select duration"
                        )
                    
                    with gr.Column():
                        health_goals = gr.CheckboxGroup(
                            label="Health Goals (select all that apply)",
                            choices=[
                                "Tissue repair and healing",
                                "Injury recovery", 
                                "Gut health improvement",
                                "Inflammation reduction",
                                "Athletic performance",
                                "General wellness"
                            ]
                        )
                        
                        medical_conditions = gr.CheckboxGroup(
                            label="Medical Conditions (select all that apply)",
                            choices=[
                                "None",
                                "Diabetes",
                                "Heart disease", 
                                "High blood pressure",
                                "Autoimmune conditions",
                                "Digestive issues",
                                "Chronic pain"
                            ]
                        )
                        
                        medications_input = gr.Textbox(
                            label="Current Medications/Supplements (one per line)",
                            placeholder="e.g.\nVitamin D\nOmega-3\nMetformin",
                            lines=5
                        )
                
                with gr.Row():
                    complete_profile_btn = gr.Button("✅ Complete Health Profile", variant="primary")
                    skip_profile_btn = gr.Button("⏭️ Skip Profile & Start Chatting", variant="secondary")
                    reset_profile_btn = gr.Button("🔄 Reset Profile", variant="secondary")
                
                profile_status = gr.Textbox(
                    label="Profile Status",
                    interactive=False
                )
            
            # Chat Interface Tab
            with gr.TabItem("💬 AI Health Coach Chat"):
                # Health profile summary
                profile_summary = gr.Markdown("Select a user to start chatting. Complete your health profile for personalized advice, or chat directly for general information.")
                
                # Chat interface
                chatbot = gr.Chatbot(
                    height=500,
                    type="messages",
                    value=[]  # Start with empty messages list
                )
                
                gr.Markdown("💬 **Chat Guide**: Ask about peptide therapy, BPC-157, or health optimization. I can provide general advice or personalized recommendations based on your profile.")
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Ask about peptide therapy, BPC-157, or health optimization...",
                        scale=4,
                        max_lines=3
                    )
                    send_btn = gr.Button("📤 Send", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat")
                    refresh_profile_btn = gr.Button("🔄 Refresh Profile")
        
        # Demo users info
        gr.Markdown("""
        ### 👥 Demo Users
        - **John Smith** - New to peptide therapy, interested in learning
        - **Jane Doe** - Experienced with BPC-157, focused on athletic performance  
        - **Jarvis Wilson** - Health enthusiast exploring gut health improvement
        
        Each user maintains separate health profiles and conversation memories.
        """)
        
        # Event handlers
        def handle_login(selected_user):
            user_id, user_name, user_email, status = create_user_session(selected_user)
            if user_id:
                profile_summary_text = get_health_profile_summary(user_id)
                return status, user_id, user_name, user_email, profile_summary_text
            else:
                return status, "", "", "", "Please select a user and complete login."
        
        def handle_complete_profile(user_id, peptide_usage, bpc157_usage, bpc157_dosage, 
                                  bpc157_duration, health_goals, medical_conditions, medications):
            status, success = complete_health_profile(
                user_id, peptide_usage, bpc157_usage, bpc157_dosage, 
                bpc157_duration, health_goals, medical_conditions, medications
            )
            if success:
                profile_summary_text = get_health_profile_summary(user_id)
                return status, profile_summary_text
            return status, "Profile incomplete."
        
        def handle_skip_profile(user_id):
            if not user_id:
                return "❌ Please select a user first.", "Please select a user first."
            
            # Set a minimal profile indicating the user skipped
            profile = get_user_profile(user_id)
            profile.onboarding_completed = False  # Keep as False since they skipped
            save_user_profile(user_id, profile)
            
            status = "⏭️ Profile skipped. You can start chatting with general advice. Complete your profile anytime for personalized recommendations."
            summary = "## 📋 Health Profile Status\n\n**Status:** Skipped - Using general advice mode\n\nYou can complete your health profile anytime by filling out the form above for personalized recommendations."
            
            return status, summary
        
        def handle_reset_profile(user_id):
            reset_values = reset_user_profile(user_id)
            status = "Profile reset. Please complete the setup again or skip to start chatting."
            summary = "Profile reset."
            return reset_values + (status, summary)
        
        def handle_refresh_profile(user_id):
            return get_health_profile_summary(user_id)
        
        def handle_clear(user_id):
            return clear_chat_history(user_id)
        
        # Wire up events
        login_btn.click(
            handle_login,
            inputs=[user_dropdown],
            outputs=[session_status, current_user, current_user_name, current_user_email, profile_summary]
        )
        
        complete_profile_btn.click(
            handle_complete_profile,
            inputs=[current_user, peptide_usage, bpc157_usage, bpc157_dosage, bpc157_duration, 
                   health_goals, medical_conditions, medications_input],
            outputs=[profile_status, profile_summary]
        )
        
        skip_profile_btn.click(
            handle_skip_profile,
            inputs=[current_user],
            outputs=[profile_status, profile_summary]
        )
        
        reset_profile_btn.click(
            handle_reset_profile,
            inputs=[current_user],
            outputs=[peptide_usage, bpc157_usage, bpc157_dosage, bpc157_duration, 
                    health_goals, medical_conditions, medications_input, profile_status, profile_summary]
        )
        
        refresh_profile_btn.click(
            handle_refresh_profile,
            inputs=[current_user],
            outputs=[profile_summary]
        )
        
        send_btn.click(
            chat_with_coach,
            inputs=[msg_input, chatbot, current_user],
            outputs=[msg_input, chatbot]
        )
        
        msg_input.submit(
            chat_with_coach,
            inputs=[msg_input, chatbot, current_user],
            outputs=[msg_input, chatbot]
        )
        
        clear_btn.click(
            handle_clear,
            inputs=[current_user],
            outputs=[chatbot, profile_status]
        )
        
        # Footer
        gr.Markdown("""
        ---
        **🔬 Technology Stack:** Gradio + OpenAI GPT-4o-mini + Mem0 + Qdrant  
        **🔒 Privacy:** Each user's data is isolated and secure  
        **⚠️ Disclaimer:** For educational purposes only. Consult healthcare professionals for medical advice.
        """)
    
    # Enable queue for streaming support
    app.queue()
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True
    ) 