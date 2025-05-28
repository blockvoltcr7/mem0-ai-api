"""
AI Prompt Engineering Tutor - Gradio Application
A simple and reliable interface for healthcare prompt engineering education with Mem0 memory.
"""

import gradio as gr
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from qdrant_client import QdrantClient
import phonenumbers
from pydantic import BaseModel, Field, ValidationError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_USE_HTTPS = os.getenv("QDRANT_USE_HTTPS", "false").lower() == "true"

# System prompt for the AI tutor
SYSTEM_PROMPT = """You are an expert AI Prompt Engineering Tutor specializing in the healthcare domain. Your mission is to teach healthcare professionals, AI developers, and health coaches how to craft high-quality, effective prompts for AI health coaching applications.

Your expertise covers:
- Best practices for health-focused AI prompting
- Safety considerations in medical AI applications
- Prompt structure optimization for health coaching
- Domain-specific techniques for healthcare AI
- Ethical considerations in health AI interactions
- Regulatory compliance awareness in health AI

Your teaching approach:
- Provide practical, actionable advice
- Use real-world healthcare examples
- Emphasize safety and ethical considerations
- Build on previous conversations and learning progress
- Adapt explanations to the user's experience level
- Encourage hands-on practice with prompt crafting

Remember: You're helping create better AI health coaches through improved prompt engineering. Always prioritize patient safety and ethical AI practices in your guidance."""

# Data Models
class UserIdentification(BaseModel):
    """User identification model."""
    username: str = Field(min_length=2, max_length=50)
    phone_number: str = Field(min_length=10)
    user_id: str = Field(default="")
    
    def model_post_init(self, __context):
        # Create unique identifier
        clean_phone = self.phone_number.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        self.user_id = f"{self.username}_{clean_phone}"

# Global variables for services
memory_service = None
openai_client = None

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
        
        # Configure Mem0
        mem0_config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "max_tokens": 1000
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "ai_tutor_memories",
                    "client": qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        memory_service = Memory.from_config(mem0_config)
        logger.info("Services initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        return False

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    try:
        # Clean the phone number
        clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Basic validation - should be at least 10 digits
        if len(clean_phone) < 10 or not clean_phone.isdigit():
            return False
            
        # Accept if it's 10+ digits (more lenient for testing)
        if len(clean_phone) >= 10:
            return True
            
        # Try to parse with phonenumbers library as fallback
        try:
            parsed = phonenumbers.parse(f"+{clean_phone}", None)
            return phonenumbers.is_valid_number(parsed)
        except:
            # If parsing fails, reject
            return False
            
    except Exception:
        return False

def create_user_session(username: str, phone: str) -> Tuple[str, str]:
    """Create or validate user session."""
    try:
        # Validate inputs
        if not username or len(username.strip()) < 2:
            return "", "❌ Username must be at least 2 characters long."
        
        if not validate_phone_number(phone):
            return "", "❌ Please enter a valid phone number (at least 10 digits)."
        
        # Create user identification
        user = UserIdentification(username=username.strip(), phone_number=phone.strip())
        
        # Get user context from memory
        try:
            memories = memory_service.search(
                query=f"user profile and learning history for {user.user_id}",
                user_id=user.user_id,
                limit=3
            )
            
            if memories and memories.get("results"):
                welcome_msg = f"🎉 Welcome back, {username}! I remember our previous conversations about prompt engineering. How can I help you continue your learning journey today?"
            else:
                welcome_msg = f"👋 Hello {username}! Welcome to your AI Prompt Engineering Tutor for Healthcare. I'm here to help you learn how to craft effective prompts for AI health coaching applications. What would you like to learn about first?"
                
        except Exception as e:
            logger.error(f"Error retrieving user context: {str(e)}")
            welcome_msg = f"👋 Hello {username}! Welcome to your AI Prompt Engineering Tutor for Healthcare. I'm here to help you learn about prompt engineering. What would you like to explore?"
        
        return user.user_id, welcome_msg
        
    except ValidationError as e:
        return "", f"❌ Validation error: {str(e)}"
    except Exception as e:
        logger.error(f"Error creating user session: {str(e)}")
        return "", "❌ An error occurred. Please try again."

def chat_with_tutor(message: str, history: List[List[str]], user_id: str) -> Tuple[str, List[List[str]]]:
    """Handle chat interaction with the AI tutor."""
    if not user_id:
        return "", history + [["Please log in first by entering your username and phone number above.", ""]]
    
    if not message.strip():
        return "", history
    
    try:
        # Get user context from memory
        try:
            memories = memory_service.search(
                query=message,
                user_id=user_id,
                limit=5
            )
            
            memories_list = memories.get("results", []) if memories else []
            memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
            
            context = f"\n\nRelevant conversation history:\n{memories_str}" if memories_str else ""
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            context = ""
        
        # Generate AI response
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + context},
            {"role": "user", "content": message}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store conversation in memory
        try:
            conversation_messages = [
                {"role": "user", "content": message},
                {"role": "assistant", "content": assistant_response}
            ]
            memory_service.add(conversation_messages, user_id=user_id)
        except Exception as e:
            logger.error(f"Error storing conversation: {str(e)}")
        
        # Update chat history
        new_history = history + [[message, assistant_response]]
        
        return "", new_history
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
        return "", history + [[message, error_response]]

def clear_chat(user_id: str) -> Tuple[List, str]:
    """Clear chat history."""
    return [], "Chat history cleared. How can I help you with prompt engineering today?"

def get_learning_summary(user_id: str) -> str:
    """Get a summary of the user's learning progress."""
    if not user_id:
        return "Please log in to see your learning summary."
    
    try:
        memories = memory_service.get_all(user_id=user_id)
        
        if not memories:
            return "📚 **Learning Summary**\n\nYou're just getting started! No learning history yet. Begin by asking about prompt engineering basics for healthcare AI."
        
        conversation_count = len(memories)
        
        summary = f"""📚 **Learning Summary**

🎯 **Progress Overview:**
- Total conversations: {conversation_count}
- Learning focus: Healthcare AI Prompt Engineering
- Status: Active learner

💡 **Keep Learning:**
Continue exploring prompt engineering techniques, safety considerations, and best practices for healthcare AI applications!
"""
        return summary
        
    except Exception as e:
        logger.error(f"Error getting learning summary: {str(e)}")
        return "Unable to retrieve learning summary at this time."

# Initialize services on startup
services_initialized = initialize_services()

# Create Gradio interface
def create_interface():
    """Create the Gradio interface."""
    
    with gr.Blocks(title="AI Prompt Engineering Tutor for Healthcare", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🏥 AI Prompt Engineering Tutor for Healthcare
        
        Learn how to craft effective prompts for AI health coaching applications with personalized memory-powered conversations.
        
        **Features:**
        - 🧠 **Memory-Powered**: Remembers your learning progress across sessions
        - 🏥 **Healthcare Focused**: Specialized in health domain prompt engineering
        - 🔒 **User Isolation**: Your conversations are kept separate and private
        - 📚 **Progressive Learning**: Builds on your previous conversations
        """)
        
        if not services_initialized:
            gr.Markdown("⚠️ **Service Initialization Error**: Please check your environment variables (OPENAI_API_KEY, QDRANT_URL)")
            return app
        
        # User identification section
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 👤 User Identification")
                username_input = gr.Textbox(
                    label="Username",
                    placeholder="Enter your username (2-50 characters)",
                    max_lines=1
                )
                phone_input = gr.Textbox(
                    label="Phone Number", 
                    placeholder="Enter your phone number (e.g., +1234567890)",
                    max_lines=1
                )
                login_btn = gr.Button("🔑 Start Session", variant="primary")
                
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Session Info")
                session_status = gr.Textbox(
                    label="Status",
                    value="Please enter your username and phone number to start",
                    interactive=False
                )
                user_id_state = gr.State("")
        
        # Chat interface
        gr.Markdown("### 💬 Chat with Your AI Tutor")
        
        chatbot = gr.Chatbot(
            height=400,
            placeholder="Your conversation will appear here after logging in..."
        )
        
        with gr.Row():
            msg_input = gr.Textbox(
                label="Your Message",
                placeholder="Ask about prompt engineering for healthcare AI...",
                scale=4,
                max_lines=3
            )
            send_btn = gr.Button("📤 Send", variant="primary", scale=1)
        
        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Chat")
            summary_btn = gr.Button("📚 Learning Summary")
        
        # Learning summary display
        summary_output = gr.Markdown(visible=False)
        
        # Event handlers
        def handle_login(username, phone):
            user_id, status = create_user_session(username, phone)
            if user_id:
                return status, user_id, [[status, ""]]
            else:
                return status, "", []
        
        def handle_send(message, history, user_id):
            return chat_with_tutor(message, history, user_id)
        
        def handle_clear(user_id):
            return clear_chat(user_id)
        
        def handle_summary(user_id):
            summary = get_learning_summary(user_id)
            return gr.update(value=summary, visible=True)
        
        # Wire up events
        login_btn.click(
            handle_login,
            inputs=[username_input, phone_input],
            outputs=[session_status, user_id_state, chatbot]
        )
        
        send_btn.click(
            handle_send,
            inputs=[msg_input, chatbot, user_id_state],
            outputs=[msg_input, chatbot]
        )
        
        msg_input.submit(
            handle_send,
            inputs=[msg_input, chatbot, user_id_state],
            outputs=[msg_input, chatbot]
        )
        
        clear_btn.click(
            handle_clear,
            inputs=[user_id_state],
            outputs=[chatbot, session_status]
        )
        
        summary_btn.click(
            handle_summary,
            inputs=[user_id_state],
            outputs=[summary_output]
        )
        
        # Footer
        gr.Markdown("""
        ---
        **⚠️ Important:** This is an educational tool. Always consult healthcare professionals for medical advice.
        
        **🔧 Tech Stack:** Gradio + OpenAI + Mem0 + Qdrant
        """)
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 