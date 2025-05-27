#!/usr/bin/env python3
"""
Peptide Coaching Demo Script

This script demonstrates the real-world Mem0 + Qdrant use case for peptide health coaching.
It runs through the specific BPC-157 scenario outlined in the task documentation.

Usage:
    python scripts/run_peptide_coaching_demo.py

Requirements:
    - OPENAI_API_KEY in environment
    - QDRANT_URL in environment (Railway deployment)
    - mem0 and dependencies installed

Author: AI Tutor Development Team
Version: 1.0
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory

# Load environment variables
load_dotenv()

class PeptideCoachingDemo:
    """Demo class for peptide coaching scenario."""
    
    def __init__(self):
        """Initialize the demo with Qdrant-backed Mem0."""
        print("🧬 Initializing Peptide Coaching Demo...")
        
        # Validate environment
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        if not os.getenv("QDRANT_URL"):
            raise ValueError("QDRANT_URL not found in environment variables")
        
        # Configure Mem0 with Qdrant using custom client approach
        from qdrant_client import QdrantClient
        
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_use_https = os.getenv("QDRANT_USE_HTTPS", "true").lower() == "true"
        protocol = "https" if qdrant_use_https else "http"
        
        # Create Qdrant client with proper timeout settings for Railway
        qdrant_client = QdrantClient(
            url=f"{protocol}://{qdrant_url}",
            port=None,
            timeout=30,
            prefer_grpc=False
        )
        
        self.config = {
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
                    "collection_name": "mem0_peptide_demo",
                    "client": qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        # Initialize components
        self.memory = Memory.from_config(self.config)
        self.openai_client = OpenAI()
        self.user_id = "demo_user_bpc157"
        
        print(f"✅ Connected to Qdrant at {protocol}://{qdrant_url}")
        print(f"✅ Using collection: mem0_peptide_demo")
        print(f"✅ Demo user ID: {self.user_id}")
    
    def generate_response(self, user_message: str) -> str:
        """Generate AI response with memory context."""
        print(f"\n🔍 Searching memories for: '{user_message[:30]}...'")
        
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
            "You are a knowledgeable AI health coach specializing in peptide therapy. "
            "You provide evidence-based information while emphasizing that peptides like BPC-157 "
            "are not FDA-approved for human use and should only be used under medical supervision. "
            "Use the provided conversation history to give personalized responses. "
            "Keep responses concise but informative."
            f"\n\nRelevant conversation history:\n{memories_str}" if memories_str 
            else "You are a knowledgeable AI health coach specializing in peptide therapy."
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
        conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
        self.memory.add(conversation_messages, user_id=self.user_id)
        print("💾 Conversation stored in Qdrant")
        
        return assistant_response
    
    def run_demo_scenario(self):
        """Run the complete BPC-157 peptide coaching scenario."""
        print("\n" + "="*60)
        print("🧬 PEPTIDE COACHING DEMO - BPC-157 SCENARIO")
        print("="*60)
        
        print("\nThis demo shows how Mem0 + Qdrant enables persistent memory")
        print("for AI health coaching applications.\n")
        
        # Scenario steps
        scenarios = [
            {
                "step": 1,
                "description": "Initial Greeting",
                "user_input": "Hi!",
                "expected": "AI should greet the user warmly"
            },
            {
                "step": 2,
                "description": "User Shares Peptide Information",
                "user_input": "I'm currently using BPC-157 for tissue repair and wound healing. I started taking it last week at 250mcg daily.",
                "expected": "AI should acknowledge and store this information"
            },
            {
                "step": 3,
                "description": "Memory Retrieval Test",
                "user_input": "What peptide am I using?",
                "expected": "AI should recall BPC-157 and dosage information"
            },
            {
                "step": 4,
                "description": "Contextual Follow-up",
                "user_input": "How long should I continue taking it?",
                "expected": "AI should provide contextual advice about BPC-157"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n📋 STEP {scenario['step']}: {scenario['description']}")
            print(f"Expected: {scenario['expected']}")
            print("-" * 50)
            
            print(f"👤 User: {scenario['user_input']}")
            
            # Generate response
            response = self.generate_response(scenario['user_input'])
            
            print(f"🤖 AI: {response}")
            
            # Pause between steps
            if scenario['step'] < len(scenarios):
                input("\n⏸️  Press Enter to continue to next step...")
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Show memory verification
        self.verify_memory_persistence()
    
    def verify_memory_persistence(self):
        """Verify that memories were properly stored."""
        print("\n🔍 MEMORY VERIFICATION")
        print("-" * 30)
        
        # Search for BPC-157 related memories
        search_results = self.memory.search(
            query="BPC-157 peptide dosage",
            user_id=self.user_id,
            limit=10
        )
        
        memories = search_results.get("results", [])
        
        print(f"📊 Total memories stored: {len(memories)}")
        
        if memories:
            print("\n📝 Stored memories:")
            for i, memory in enumerate(memories[:5], 1):
                print(f"  {i}. {memory.get('memory', 'N/A')[:100]}...")
        
        # Test memory recall
        print("\n🧠 Testing memory recall...")
        recall_response = self.generate_response("Remind me about my peptide usage")
        print(f"🤖 Recall test: {recall_response[:150]}...")
        
        print("\n✅ Memory verification complete!")
    
    def interactive_mode(self):
        """Run interactive mode for manual testing."""
        print("\n🎮 INTERACTIVE MODE")
        print("Type your messages to chat with the AI")
        print("Type 'exit' to quit, 'demo' to run the full scenario")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'demo':
                    self.run_demo_scenario()
                    continue
                
                if not user_input:
                    continue
                
                response = self.generate_response(user_input)
                print(f"🤖 AI: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

def main():
    """Main entry point."""
    try:
        demo = PeptideCoachingDemo()
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            demo.interactive_mode()
        else:
            demo.run_demo_scenario()
            
            # Ask if user wants to continue in interactive mode
            choice = input("\n🎮 Would you like to continue in interactive mode? (y/n): ")
            if choice.lower().startswith('y'):
                demo.interactive_mode()
    
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 