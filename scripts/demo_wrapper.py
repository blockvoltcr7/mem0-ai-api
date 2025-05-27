#!/usr/bin/env python3
"""
Demo Wrapper for Mem0 + Qdrant CLI

This wrapper provides an interactive demo experience using the working test components
to avoid architecture compatibility issues while still demonstrating all features.
"""

import os
import sys
import uuid
import time
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

class DemoWrapper:
    """Wrapper class for demonstrating Mem0 + Qdrant functionality."""
    
    def __init__(self):
        """Initialize the demo wrapper."""
        self.user_id = f"demo_user_{uuid.uuid4().hex[:8]}"
        self.conversation_count = 0
        self.start_time = time.time()
        
        print("🧠 Initializing Mem0 + Qdrant Demo...")
        print(f"👤 User ID: {self.user_id}")
        
        self._initialize_components()
        print("✅ All components initialized successfully!")
    
    def _initialize_components(self):
        """Initialize all required components."""
        # Validate environment
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("❌ OPENAI_API_KEY not found")
        if not os.getenv("QDRANT_URL"):
            raise ValueError("❌ QDRANT_URL not found")
        
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_use_https = os.getenv("QDRANT_USE_HTTPS", "true").lower() == "true"
        protocol = "https" if qdrant_use_https else "http"
        
        self.qdrant_client = QdrantClient(
            url=f"{protocol}://{qdrant_url}",
            port=None,
            timeout=30,
            prefer_grpc=False
        )
        
        # Initialize Mem0 memory
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
                    "collection_name": "mem0_demo_wrapper",
                    "client": self.qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        self.memory = Memory.from_config(config)
        self.openai_client = OpenAI()
    
    def generate_response(self, user_message: str) -> str:
        """Generate AI response with memory context."""
        print(f"🔍 Searching memories for: '{user_message[:30]}...'")
        
        # Search for relevant memories
        relevant_memories = self.memory.search(
            query=user_message,
            user_id=self.user_id,
            limit=5
        )
        
        memories_list = relevant_memories.get("results", [])
        memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
        
        print(f"📚 Found {len(memories_list)} relevant memories")
        
        # Construct system prompt
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
        print("🤖 Generating AI response...")
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store conversation in memory
        print("💾 Storing conversation in memory...")
        conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
        self.memory.add(conversation_messages, user_id=self.user_id)
        
        self.conversation_count += 1
        return assistant_response
    
    def run_peptide_demo(self):
        """Run the automated peptide coaching demo."""
        print("\n🧬 Running BPC-157 Peptide Coaching Demo")
        print("=" * 50)
        
        demo_messages = [
            "Hi!",
            "I'm currently using BPC-157 for tissue repair and wound healing. I started taking it last week at 250mcg daily.",
            "What peptide am I using?",
            "How long should I continue taking it?"
        ]
        
        for i, message in enumerate(demo_messages, 1):
            print(f"\n📋 Demo Step {i}/4")
            print(f"👤 User: {message}")
            
            response = self.generate_response(message)
            print(f"🤖 AI: {response}")
            
            if i < len(demo_messages):
                input("\n⏸️  Press Enter to continue...")
        
        print("\n✅ Demo completed!")
    
    def search_memories(self, query: str):
        """Search memories for a specific query."""
        print(f"\n🔍 Searching memories for: '{query}'")
        
        results = self.memory.search(query=query, user_id=self.user_id, limit=10)
        memories = results.get("results", [])
        
        if memories:
            print(f"Found {len(memories)} memories:")
            for i, memory in enumerate(memories, 1):
                print(f"  {i}. {memory.get('memory', 'N/A')}")
        else:
            print("No memories found.")
    
    def show_stats(self):
        """Show session statistics."""
        try:
            all_memories = self.memory.search(query="user", user_id=self.user_id, limit=100)
            memory_count = len(all_memories.get("results", []))
            
            duration = time.time() - self.start_time
            duration_str = f"{duration:.1f} seconds" if duration < 60 else f"{duration/60:.1f} minutes"
            
            print(f"\n📊 Session Statistics")
            print(f"  Total memories: {memory_count}")
            print(f"  Conversations: {self.conversation_count}")
            print(f"  Current user: {self.user_id}")
            print(f"  Session duration: {duration_str}")
        except Exception as e:
            print(f"❌ Error getting stats: {str(e)}")
    
    def interactive_mode(self):
        """Run interactive mode."""
        print("\n" + "=" * 70)
        print("🧠 Interactive Mem0 + Qdrant Demo")
        print("=" * 70)
        print("Commands:")
        print("  'demo' - Run peptide coaching demo")
        print("  'search <query>' - Search memories")
        print("  'stats' - Show statistics")
        print("  'quit' - Exit")
        print("  Or just type a message to chat!")
        print("=" * 70)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'demo':
                    self.run_peptide_demo()
                elif user_input.lower().startswith('search '):
                    query = user_input[7:].strip()
                    if query:
                        self.search_memories(query)
                    else:
                        print("❌ Please provide a search query")
                elif user_input.lower() == 'stats':
                    self.show_stats()
                elif user_input:
                    response = self.generate_response(user_input)
                    print(f"🤖 AI: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

def main():
    """Main entry point."""
    print("🎪 Mem0 + Qdrant Demo Wrapper")
    print("This demo showcases memory capabilities with persistent storage.")
    
    try:
        demo = DemoWrapper()
        
        # Ask user what they want to do
        print("\nWhat would you like to do?")
        print("1. Run automated peptide coaching demo")
        print("2. Interactive chat mode")
        print("3. Quick test and exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            demo.run_peptide_demo()
            demo.show_stats()
        elif choice == "2":
            demo.interactive_mode()
        elif choice == "3":
            # Quick test
            print("\n🧪 Running quick test...")
            response = demo.generate_response("Hello, I'm testing the system")
            print(f"🤖 AI: {response}")
            demo.show_stats()
        else:
            print("Invalid choice. Running interactive mode...")
            demo.interactive_mode()
            
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 