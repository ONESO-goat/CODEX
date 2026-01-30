# autonomous_loop.py

import random
from pathlib import Path
from agent_core import AgentCore
from prompt_engine import Personailty
from datetime import datetime
import asyncio
import json



class AutonomousLoop:
    def __init__(self, user_id: str, agent_core, storage_path: str = "codex/brain"):
        self.core = agent_core # agent_core AgentCore
        self.user = user_id
        # self.personailty = personailty
        self.storage = Path(storage_path)
        self.thoughts = []
        self.short_term_thoughts = {}
        self.is_active: bool = True
        self.boot_occuring_thoughts()

    def boot_occuring_thoughts(self):
        self.save_thoughts()

    def save_thoughts(self):
        file_path = self.storage / f"{self.core.get_name()}_thoughts.json"
        with open(file_path, 'w') as f:
            json.dump(self.thoughts, f, indent=2)



    async def live(self):
        """Main existence loop"""

        while self.is_active:
            if random.random() < 0.05: # 5%
                thought = self.core.introspec()
                if thought:
                    self.thoughts.append({
                        "thoughts": thought,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    print(f"\n[Codex thinking]: {thought}\n")

            self.save_thoughts()

            self.core.update_age()
            

            await asyncio.sleep(1)


    async def initiate_conversation(self):
        """Codex starts a converstaion"""
        topics = [
            "Hey, I was just thinking about something...",
            "Can I ask you something random?",
            "You know what's weird?",
            f"I've been alive for {self.core.age:.2f} hours now. Time is strange."
        ]
        random_topic = random.choice(topics)

        # humans have thoughts that have reasoning behind it, 
        # some people speaking themselve
        self.short_term_thoughts[random_topic] = ...
        if len(self.short_term_thoughts.keys()) == 10:
            self.short_term_thoughts.popitem()
        print(f"\n[Codex]: {random_topic}\n")

    async def speak_your_mind(self, topic: str):
        if topic.isspace():
            return
        pattern = [
            r""
        ]


        if random.random() < 0.1:
            return f"You are randomly thinking about this topic: {topic}"
        
        # TRASH
    def create_folder(self, folder):
        folder = Path(folder)
        try:
            with open(folder, 'w') as f:
                json.dump(self.thoughts, f, indent=2)
        except Exception as e:
            print(f"There was an Error when creating file in => [autonomous_loop.py]. Details: {e}")

        
if __name__ == "__main__":
    ...
        