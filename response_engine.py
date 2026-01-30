# response_engine.py - NOTE: i should change the names between prompt_engine and response_engine


from datetime import date, datetime
import uuid
from typing import Dict, List
import requests
from prompt_engine import Personailty
from autonomous_loop import AutonomousLoop
from agent_core import AgentCore
from user_memory import selfaware

class PromptEngine:
    def __init__(self,
                 agent_core,
                personailty,
                memory,
                 session_id: str,  
                 activation:date = datetime.utcnow(), 
                 model: str = "llama3.2:3b"):
        
        self.session_id = session_id
      
        
        self.core = agent_core
        self.personailty = personailty
        self.date = activation

        
        
        self.memory = memory
        

        self.api_url = "http://localhost:11434/api/chat"
        self.model = model

        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code != 200:
                raise ConnectionError("Ollama not running")
        except Exception as e:
            raise ConnectionError(
                "Ollama not found! Install it from https://ollama.com\n"
                f"Then run: ollama pull {model}"
                f"DETAILS: {e}"
            )
        
    def chat(self, response: str) -> str:
        print(f"RESPONSE: {response}\n\n")
        print(self.memory.prompt_detection("user", response))
        print()
        print(self.core._learn_number_(response))
        print()

        context = self.memory.get_relevant_context()
        print(f"CONTEXT: {context}\n\n")

        prompt_package = self.personailty.construct_full_prompt(
            response,
            context,
            agent_core=self.core,
            memory=self.memory
        )
        print(f"PROMPT PACKAGE: {prompt_package}")

        response = self._call_ollama(prompt_package)

        self.memory.prompt_detection("assistant", response)
        return response


    def _call_ollama(self, prompt_package: dict) -> str:
        """Call Ollama API"""
        # Build messages for Ollama format
        messages = [
            {"role": "system", "content": prompt_package["system_prompt"]}
        ]
        
        # Add conversation history
        messages.extend(prompt_package["messages"])
        
        # Add current message
        messages.append({
            "role": "user",
            "content": prompt_package["current_message"]
        })
        
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False  # Get complete response at once
                }, 
                timeout=600
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"]
            else:
                print(f"Response: {response.text}")
                print(f"Error: Ollama returned status {response.status_code}")
                return "I'm having trouble thinking right now. My mind feels foggy."
        except requests.exceptions.Timeout:
            return "Sorry, I'm thinking too slowly. Please give me a moment?"
        except requests.exceptions.ConnectionError:
            return "I can't seem to connect to my thoughts. Is Ollama running?"
        
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")
            return f"Something strange happened in my mind: {type(e).__name__}"
    
    def end_session(self):
        """Save memory"""
        self.memory.save_session()
        print(f"\n📊 Session stats: {self.memory.get_summary_stats()}")
    def reset_conversation(self):
        """Start fresh"""
        self.memory._clear_short_term_memory()