#!/usr/bin/env python3
"""
Interactive Mem0 + Qdrant CLI Demo

This script provides an interactive command-line interface for demonstrating
Mem0's memory capabilities with Qdrant vector database. Perfect for team demos
and manual testing of the peptide coaching scenario or any other use case.

Features:
- Interactive chat with AI that remembers conversations
- Persistent memory storage in Qdrant
- User isolation and switching
- Memory search and management
- Real-time feedback and statistics
- Colored output for better UX

Usage:
    python scripts/interactive_mem0_qdrant_cli.py

Author: AI Tutor Development Team
Version: 1.0
"""

import os
import sys
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class InteractiveMem0CLI:
    """
    Interactive CLI for Mem0 + Qdrant demonstrations.
    
    This class provides a user-friendly interface for testing and demonstrating
    Mem0's memory capabilities with persistent Qdrant storage.
    """
    
    def __init__(self, user_id: Optional[str] = None):
        """
        Initialize the interactive CLI.
        
        Args:
            user_id: Optional user ID. If not provided, a unique one will be generated.
        """
        self.user_id = user_id or f"demo_user_{uuid.uuid4().hex[:8]}"
        self.conversation_count = 0
        self.start_time = time.time()
        
        print(f"{Colors.HEADER}🧠 Initializing Interactive Mem0 + Qdrant CLI Demo{Colors.ENDC}")
        print(f"{Colors.OKBLUE}User ID: {self.user_id}{Colors.ENDC}")
        
        # Validate environment
        self._validate_environment()
        
        # Initialize components
        self._initialize_qdrant_client()
        self._initialize_memory()
        self._initialize_openai_client()
        
        print(f"{Colors.OKGREEN}✅ All components initialized successfully!{Colors.ENDC}")
    
    def _validate_environment(self) -> None:
        """Validate required environment variables."""
        print(f"{Colors.OKCYAN}🔍 Validating environment...{Colors.ENDC}")
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(f"{Colors.FAIL}❌ OPENAI_API_KEY not found in environment variables{Colors.ENDC}")
        
        if not os.getenv("QDRANT_URL"):
            raise ValueError(f"{Colors.FAIL}❌ QDRANT_URL not found in environment variables{Colors.ENDC}")
        
        print(f"{Colors.OKGREEN}✅ Environment validation passed{Colors.ENDC}")
    
    def _initialize_qdrant_client(self) -> None:
        """Initialize Qdrant client with proper settings."""
        print(f"{Colors.OKCYAN}🔗 Connecting to Qdrant...{Colors.ENDC}")
        
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_use_https = os.getenv("QDRANT_USE_HTTPS", "true").lower() == "true"
        protocol = "https" if qdrant_use_https else "http"
        
        self.qdrant_client = QdrantClient(
            url=f"{protocol}://{qdrant_url}",
            port=None,
            timeout=30,
            prefer_grpc=False
        )
        
        # Test connection
        try:
            collections = self.qdrant_client.get_collections()
            print(f"{Colors.OKGREEN}✅ Connected to Qdrant: {len(collections.collections)} collections available{Colors.ENDC}")
        except Exception as e:
            raise ConnectionError(f"{Colors.FAIL}❌ Failed to connect to Qdrant: {str(e)}{Colors.ENDC}")
    
    def _initialize_memory(self) -> None:
        """Initialize Mem0 memory with Qdrant backend."""
        print(f"{Colors.OKCYAN}🧠 Initializing Mem0 memory system...{Colors.ENDC}")
        
        config = {
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
                    "collection_name": "mem0_interactive_demo",
                    "client": self.qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        self.memory = Memory.from_config(config)
        print(f"{Colors.OKGREEN}✅ Mem0 memory system initialized{Colors.ENDC}")
    
    def _initialize_openai_client(self) -> None:
        """Initialize OpenAI client."""
        print(f"{Colors.OKCYAN}🤖 Initializing OpenAI client...{Colors.ENDC}")
        self.openai_client = OpenAI()
        print(f"{Colors.OKGREEN}✅ OpenAI client initialized{Colors.ENDC}")
    
    def generate_ai_response(self, user_message: str) -> str:
        """
        Generate AI response using Mem0 memory context.
        
        Args:
            user_message: User's input message
            
        Returns:
            AI assistant's response
        """
        print(f"{Colors.OKCYAN}🔍 Searching for relevant memories...{Colors.ENDC}")
        
        # Search for relevant memories
        relevant_memories = self.memory.search(
            query=user_message,
            user_id=self.user_id,
            limit=5
        )
        
        memories_list = relevant_memories.get("results", [])
        memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
        
        print(f"{Colors.OKBLUE}📚 Found {len(memories_list)} relevant memories{Colors.ENDC}")
        
        # Construct system prompt with memory context
        system_prompt = (
            "You are a knowledgeable AI assistant with access to conversation history. "
            "Use the provided memories to give contextual and personalized responses. "
            "If the conversation involves health topics like peptides, always emphasize "
            "the importance of medical supervision and that such substances may not be "
            "FDA-approved for human use. Keep responses helpful but concise."
            f"\n\nRelevant conversation history:\n{memories_str}" if memories_str 
            else "You are a knowledgeable AI assistant."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Generate response
        print(f"{Colors.OKCYAN}🤖 Generating AI response...{Colors.ENDC}")
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store conversation in memory
        print(f"{Colors.OKCYAN}💾 Storing conversation in memory...{Colors.ENDC}")
        conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
        self.memory.add(conversation_messages, user_id=self.user_id)
        
        self.conversation_count += 1
        return assistant_response
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about current memory usage."""
        try:
            # Search for memories using a broad term
            all_memories = self.memory.search(query="user", user_id=self.user_id, limit=100)
            memory_count = len(all_memories.get("results", []))
            
            return {
                "total_memories": memory_count,
                "user_id": self.user_id,
                "conversations": self.conversation_count,
                "uptime_seconds": time.time() - self.start_time,
                "uptime_formatted": self._format_duration(time.time() - self.start_time)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format."""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        else:
            return f"{seconds/3600:.1f} hours"
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories for a specific query."""
        try:
            search_results = self.memory.search(
                query=query, 
                user_id=self.user_id, 
                limit=limit
            )
            return search_results.get("results", [])
        except Exception as e:
            print(f"{Colors.FAIL}❌ Memory search failed: {str(e)}{Colors.ENDC}")
            return []
    
    def switch_user(self, new_user_id: str) -> None:
        """Switch to a different user ID."""
        old_user = self.user_id
        self.user_id = new_user_id
        print(f"{Colors.OKGREEN}✅ Switched from user '{old_user}' to '{self.user_id}'{Colors.ENDC}")
    
    def print_help(self) -> None:
        """Print help information about available commands."""
        help_text = f"""
{Colors.HEADER}🧠 Interactive Mem0 + Qdrant CLI Demo - Available Commands{Colors.ENDC}

{Colors.BOLD}Basic Usage:{Colors.ENDC}
  - Just type your message to chat with the AI
  - Type 'exit' or 'quit' to end the session

{Colors.BOLD}Special Commands:{Colors.ENDC}
  {Colors.OKCYAN}/help{Colors.ENDC}              - Show this help message
  {Colors.OKCYAN}/stats{Colors.ENDC}             - Show memory and session statistics
  {Colors.OKCYAN}/search <query>{Colors.ENDC}    - Search memories for specific content
  {Colors.OKCYAN}/user <user_id>{Colors.ENDC}    - Switch to a different user ID
  {Colors.OKCYAN}/newuser{Colors.ENDC}           - Generate and switch to a new random user ID
  {Colors.OKCYAN}/memories{Colors.ENDC}          - Show all memories for current user
  {Colors.OKCYAN}/demo{Colors.ENDC}              - Run the BPC-157 peptide coaching demo

{Colors.BOLD}Demo Examples:{Colors.ENDC}
  {Colors.WARNING}Hi, I'm interested in peptide therapy{Colors.ENDC}
  {Colors.WARNING}I'm using BPC-157 for tissue repair at 250mcg daily{Colors.ENDC}
  {Colors.WARNING}What peptide am I using?{Colors.ENDC}
  {Colors.WARNING}/search BPC-157{Colors.ENDC}
  {Colors.WARNING}/stats{Colors.ENDC}

{Colors.BOLD}Features:{Colors.ENDC}
  ✅ Persistent memory storage in Qdrant
  ✅ User isolation and switching
  ✅ Contextual AI responses
  ✅ Real-time memory search
  ✅ Session statistics
        """
        print(help_text)
    
    def run_peptide_demo(self) -> None:
        """Run the BPC-157 peptide coaching demo scenario."""
        print(f"\n{Colors.HEADER}🧬 Running BPC-157 Peptide Coaching Demo{Colors.ENDC}")
        print(f"{Colors.OKBLUE}This demo will simulate the peptide coaching scenario automatically.{Colors.ENDC}")
        
        demo_messages = [
            "Hi!",
            "I'm currently using BPC-157 for tissue repair and wound healing. I started taking it last week at 250mcg daily.",
            "What peptide am I using?",
            "How long should I continue taking it?"
        ]
        
        for i, message in enumerate(demo_messages, 1):
            print(f"\n{Colors.WARNING}📋 Demo Step {i}/4{Colors.ENDC}")
            print(f"{Colors.BOLD}👤 Demo User:{Colors.ENDC} {message}")
            
            response = self.generate_ai_response(message)
            print(f"{Colors.BOLD}🤖 AI:{Colors.ENDC} {response}")
            
            if i < len(demo_messages):
                input(f"\n{Colors.OKCYAN}⏸️  Press Enter to continue to next step...{Colors.ENDC}")
        
        print(f"\n{Colors.OKGREEN}✅ Demo completed! The AI now has memory of the BPC-157 conversation.{Colors.ENDC}")
    
    def show_all_memories(self) -> None:
        """Show all memories for the current user."""
        print(f"\n{Colors.HEADER}📚 All Memories for User: {self.user_id}{Colors.ENDC}")
        
        memories = self.search_memories("user", limit=50)
        
        if not memories:
            print(f"{Colors.WARNING}No memories found for this user.{Colors.ENDC}")
            return
        
        for i, memory in enumerate(memories, 1):
            print(f"{Colors.OKBLUE}  {i}.{Colors.ENDC} {memory.get('memory', 'N/A')}")
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands starting with '/'.
        
        Args:
            user_input: The user's input string
            
        Returns:
            True if a command was handled, False otherwise
        """
        if not user_input.startswith('/'):
            return False
        
        parts = user_input[1:].split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == "help":
            self.print_help()
            
        elif command == "stats":
            stats = self.get_memory_stats()
            print(f"\n{Colors.HEADER}📊 Session Statistics{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Total memories: {stats.get('total_memories', 'N/A')}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Conversations: {stats.get('conversations', 0)}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Current user: {stats.get('user_id', 'N/A')}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Session duration: {stats.get('uptime_formatted', 'N/A')}{Colors.ENDC}")
            
        elif command == "search":
            if not args:
                print(f"{Colors.FAIL}❌ Please provide a search query. Example: /search BPC-157{Colors.ENDC}")
                return True
                
            results = self.search_memories(args)
            if results:
                print(f"\n{Colors.HEADER}🔍 Found {len(results)} memories for '{args}'{Colors.ENDC}")
                for i, result in enumerate(results, 1):
                    print(f"{Colors.OKBLUE}  {i}.{Colors.ENDC} {result.get('memory', 'N/A')}")
            else:
                print(f"{Colors.WARNING}🔍 No memories found for '{args}'{Colors.ENDC}")
                
        elif command == "user":
            if not args:
                print(f"{Colors.OKBLUE}Current user ID: {self.user_id}{Colors.ENDC}")
                print(f"{Colors.OKCYAN}To change user: /user <new_user_id>{Colors.ENDC}")
                return True
                
            self.switch_user(args.strip())
            
        elif command == "newuser":
            new_user_id = f"demo_user_{uuid.uuid4().hex[:8]}"
            self.switch_user(new_user_id)
            
        elif command == "memories":
            self.show_all_memories()
            
        elif command == "demo":
            self.run_peptide_demo()
            
        else:
            print(f"{Colors.FAIL}❌ Unknown command: /{command}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Type /help for available commands{Colors.ENDC}")
            
        return True
    
    def run_interactive_session(self) -> None:
        """Run the main interactive CLI session."""
        # Print welcome message
        print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}🧠 Welcome to Interactive Mem0 + Qdrant CLI Demo!{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Model: gpt-4o-mini{Colors.ENDC}")
        print(f"{Colors.OKBLUE}User ID: {self.user_id}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Storage: Qdrant ({os.getenv('QDRANT_URL')}){Colors.ENDC}")
        print(f"{Colors.OKCYAN}Type /help for commands or just start chatting!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Try the peptide demo with: /demo{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}")
        
        try:
            while True:
                try:
                    # Get user input
                    user_input = input(f"\n{Colors.BOLD}💬 You:{Colors.ENDC} ").strip()
                    
                    # Check for exit commands
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print(f"{Colors.OKGREEN}👋 Goodbye! Thanks for testing Mem0 + Qdrant!{Colors.ENDC}")
                        break
                    
                    # Skip empty input
                    if not user_input:
                        continue
                    
                    # Handle special commands
                    if self.handle_command(user_input):
                        continue
                    
                    # Process regular chat message
                    print(f"{Colors.BOLD}🤖 AI:{Colors.ENDC} ", end="", flush=True)
                    response = self.generate_ai_response(user_input)
                    print(response)
                    
                except KeyboardInterrupt:
                    print(f"\n\n{Colors.OKGREEN}👋 Session interrupted. Goodbye!{Colors.ENDC}")
                    break
                    
                except Exception as e:
                    print(f"{Colors.FAIL}❌ An error occurred: {str(e)}{Colors.ENDC}")
                    print(f"{Colors.OKCYAN}You can continue chatting or type 'exit' to quit.{Colors.ENDC}")
                    
        except Exception as e:
            print(f"{Colors.FAIL}❌ Fatal error: {str(e)}{Colors.ENDC}")
        
        finally:
            # Print session summary
            stats = self.get_memory_stats()
            print(f"\n{Colors.HEADER}📊 Session Summary{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Conversations: {stats.get('conversations', 0)}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Memories stored: {stats.get('total_memories', 'N/A')}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}  Session duration: {stats.get('uptime_formatted', 'N/A')}{Colors.ENDC}")

def main():
    """Main entry point for the interactive CLI."""
    try:
        # Parse command line arguments
        user_id = None
        if len(sys.argv) > 1:
            user_id = sys.argv[1]
            print(f"{Colors.OKBLUE}Using provided user ID: {user_id}{Colors.ENDC}")
        
        # Initialize and run the CLI
        cli = InteractiveMem0CLI(user_id=user_id)
        cli.run_interactive_session()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Fatal error: {str(e)}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Please check your environment configuration and try again.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main() 