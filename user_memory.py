# user_memory.py


from datetime import date, datetime
from pathlib import Path
import re
import asyncio
import json
from agent_core import AgentCore
import uuid
from typing import List, Dict, Optional


class selfaware:
    def __init__(self, agent_core, user_id: str, date: date = date.today()):
        self.user_database_id = str(uuid.uuid4())
        self.booting_info = agent_core
        self.path = self.booting_info.get_storage_path()
        self._name_ = self.booting_info.get_name()
        self.date = date

        self.buffer: List[Dict] = []
        self.user_id = user_id
        self.max_speech = 100
        self.information = []

        self.current_info = {
            "id": self.user_database_id,
            "name": None,
            "nickname": None,
            "todays_date": str(date),
            "facts": {},
            "preferences": {},
            "conversation_count": 0,
            "last_interaction": None, 
            "topics_mentioned": []
        }
        self.load_user_data()










    def load_user_data(self):
        """Load user data"""
        path = self.path / f"{self._name_}_{self.user_id}.json"
        if path.exists():
            with open(path, 'r') as f:
                self.current_info = json.load(f)
        else:
            self.create_user_file(path)


    def create_user_file(self, path):
        """
        Docstring for create_user_file
        
        :param self: Create user data json
        :param path: Path, example: "codex/brain/example.json
        """
        path = Path(path)
        try:
            with open(path, 'w') as f:
                json.dump(self.current_info, f, indent=2)
        except Exception as e:
            print(f"There was an error when creating user data, DETAILS: {e}")
            

    def save_user_data(self):
        """Save user data"""
        path = self.path / f"{self._name_}_{self.user_id}.json"
        with open(Path(path), 'w') as f:
            json.dump(self.current_info, f, indent=2)
            self.assign_new_json()


    def assign_new_json(self):
        path = self.path / f"{self._name_}_{self.user_id}.json"
        try:
            with open(path, 'r') as f:
                self.current_info = json.load(f)
        except Exception as e: 
            print(f"[assign_new_json] => There was an error when creating json file: {e}")



    def prompt_detection(self, role: str, response: str, metadata: Optional[Dict] = None):

        info = {
            "role": role,
            "response": response,
            "date": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        if len(self.buffer) > self.max_speech:
            self.buffer.pop(0)
        
        if role.lower() == "user":
            self._learn_about_the_person(response)
            self.booting_info.set_mood(response)

            


        if role.lower() == "assistant": 
            self.booting_info.introspec()

        self.buffer.append(info)

    
        

    def _learn_about_the_person(self, response: str):
        response = response.lower()
        facts_pattern = [
            # Explicit preferences
            r"I enjoy (\w+)",
            r"I like (\w+)",
            r"I love (\w+)",
            
            # Activity mentions
            r"I (?:was|am) playing (\w+)",
            r"I play (\w+)",
            r"I (?:was|am) (?:doing|watching) (\w+)",
            
            # Interests
            r"I'm interested in (\w+)",
            r"I'm into (\w+)",
            
            # Ownership/experience
            r"I have (?:a|an) (\w+)",
            r"I own (?:a|an) (\w+)"
        ]
        for pattern in facts_pattern:
            match = re.search(pattern, response)
            if match:
                fact = match.group(1)
                if fact not in self.current_info["facts"]:
                    self.current_info["facts"][fact] = {

                        "python": {
                            "mood": "Liked",
                            "sentiment": 0.9,
                            "confidence": 0.7,
                            "last_mentioned": str(datetime.utcnow().isoformat())
                        }
                    }

    
        disliked_facts_pattern =[
            r"I don't enjoy doing (\w+)",
            r"I don't like (\w+)",
            r"I'm not interested in (\w+)"
        ]

        for pattern in disliked_facts_pattern:
            match = re.search(pattern, response)
            if match:
                disliked_fact = match.group(1)
                if disliked_fact not in self.current_info["facts"]:
                    self.current_info["facts"][disliked_fact] = {

                        "python": {
                            "mood": "Disliked",
                            "sentiment": 0.9,
                            "confidence": 0.7,
                            "last_mentioned": str(datetime.utcnow().isoformat())
                        }
                    }

        hated_facts_pattern =[
            r"I hate doing (\w+)",
            r"I can't stand (\w+)",
        ]
        for pattern in hated_facts_pattern:
            match = re.search(pattern, response)
            if match:
                fact = match.group(1)
                if fact not in self.current_info["facts"]:
                    self.current_info["facts"][fact] = {

                        "python": {
                            "mood": "Hated",
                            "sentiment": 0.9,
                            "confidence": 0.7,
                            "last_mentioned": str(datetime.utcnow().isoformat())
                        }
                    }
                    self.save_user_data()

        favorite_patterns = [
            (r"I love (\w+)", 1),
            (r"I absolutely (?:love|like) (\w+)", 1)
        ]

        for pattern, group_num in favorite_patterns:
            match = re.search(pattern, response.lower())
            if match and match not in self.current_info["facts"]:
                fact = match.group(group_num)
                if fact not in self.current_info["facts"]:
                    self.current_info["facts"][fact] = {
                            "mood": "Loved",
                            "sentiment": 0.9,
                            "confidence": 0.7,
                            "last_mentioned": datetime.utcnow().isoformat()
                        }
                    self.save_user_data()


        nickname_pattern = [
            r"People (sometimes|also) call me (\w+)",
            r"I rather be called (\w+)",
        ]
        for pattern in nickname_pattern:
            match = re.search(pattern, response)

            if match and not self.current_info["nickname"]:
                self.current_info["nickname"] = match.group(1)

            

        identity_pattern = [
    r"(?:^|\s)I am (\w+)",  # Must start sentence or after space
    r"(?:^|\s)[Mm]y [Nn]ame (?:is|was) (\w+)",
    r"(?:^|\s)(?:You can )?[Cc]all me (\w+)",
    r"(?:^|\s)I'm (\w+)",  # Add this too
]

        for pattern in identity_pattern: 
            match = re.search(pattern, response)
            if match:
                potential_name = match.group(1).capitalize()
                if potential_name not in ["my", "your", "the", "a", "and"]:
                    self.current_info["name"] = potential_name
                    self.reconize_user(self.current_info["name"])

        feelings_pattern = [
            r"I love you",
            r"(You are|You're) my everything",
            r"I miss you"
        ]

        for pattern in feelings_pattern:
            match = re.search(pattern, response)
            if match:
                # TODO: change the mood of the bot
                self.booting_info.set_mood(match.group(0))

        prefer_patterns = [
            r"I prefer (\w+)",
            r"I prefer this (\w+)",
            r"I have a preference for (\w+)",
            r"I preferably want (\w+)",
            r"preferably (\w+)",
            r"I rather (have|get) (\w+)"
        ]
        for pattern in prefer_patterns:
            match = re.search(pattern, response)
            if match:
                prefers = match.group(1)
                self.current_info["preferences"][prefers] = "positive"
                self.save_user_data()


        activity_patterns = [
        (r"I (?:was|am|been) playing (\w+(?:\s+\w+)*)", "activity", "Liked"),
        (r"I play (\w+(?:\s+\w+)*)", "activity", "Liked"),
        (r"I watch (\w+(?:\s+\w+)*)", "activity", "Liked"),
        (r"I listen to (\w+(?:\s+\w+)*)", "activity", "Liked"),
    ]
    
        for pattern, category, default_mood in activity_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                fact_name = match.strip()
            
                if fact_name not in self.current_info["facts"]:
                    self.current_info["facts"][fact_name] = {
                        "category": category,
                        "mood": default_mood,
                        "sentiment": 0.7,
                        "confidence": 0.6,
                        "first_mentioned": datetime.utcnow().isoformat(),
                        "mention_count": 1
                    }
                    self.save_user_data()
                else:
                    # Reinforce existing fact
                    self.current_info["facts"][fact_name]["mention_count"] += 1
                    self.current_info["facts"][fact_name]["confidence"] = min(
                        1.0,
                        self.current_info["facts"][fact_name]["confidence"] + 0.1
                    )
                    self.save_user_data()
        number_preference_pattern = [
    r"[Mm]y favorite number is (\d+)",
    r"[Mm]y favorite is (\d+)",
        ]

        for pattern in number_preference_pattern:
            match = re.search(pattern, response)
            if match:
                number = int(match.group(1))
                self.current_info["preferences"]["favorite_number"] = number
                
                # Also learn it as a fact
                self.current_info["facts"][f"favorite_number_{number}"] = {
                    "mood": "Loved",
                    "sentiment": 1.0,
                    "confidence": 0.9,
                    "first_mentioned": datetime.utcnow().isoformat()
        }
        game_patterns = [
    r"I (?:love|like|enjoy|play) (?:games like )?(\w+)",
    r"(\w+) or (\w+)",  # "pac man or subway surfers"
]

        for pattern in game_patterns:
            matches = re.findall(pattern, response.lower())
            for match in matches:
                game = match if isinstance(match, str) else match[0]
            
                if game not in ["i", "you", "my", "your", "the"]:
                    if game not in self.current_info["facts"]:
                        self.current_info["facts"][game] = {
                        "category": "game",
                        "mood": "Liked",
                        "confidence": 0.7,
                        "first_mentioned": datetime.utcnow().isoformat()
                    }
        self.save_user_data()

    def reconize_user(self, user):
        if not user or user != self.current_info["name"]:
            return
        facts = [f'-{fact}' for fact in self.current_info["facts"].keys()]
        prefer = [f'- {prefer}' for prefer in self.current_info["preferences"].keys()]
        topics = [f'-{topic}' for topic in self.current_info["topics_mentioned"]]
        return f"""You are talking to {user}. 
        Here are your knowledge of this person: 

        NAME:
        {user}
        
        FACTS: 
        {facts}

        PREFERENCE:
        {prefer}

        TOPICS YOU GUYS HAVE DISCUSSED:
        {topics}

        



"""


    def save_session(self):
        """Save session after end of session"""
        self.current_info["conversation_count"] += 1
        self.current_info["last_interaction"] = datetime.now().isoformat()

        path = self.booting_info.get_storage_path()


        main_path = path / f"{self.user_id}.json"
        with open(main_path, 'w') as f:
            json.dump(self.current_info, f,indent=2)
    
    def get_summary_stats(self) -> Dict:
        return {
            "total_conversations": self.current_info["conversation_count"],
            "facts": len(self.current_info["facts"]),
            "preferences_learned": len(self.current_info["preferences"]),
            "last_seen": self.current_info.get("last_interaction", "Never")
            }

    def get_relevant_context(self) -> Dict:


        context = {
            "conversation_history": self.buffer[-50:],
            "user_info": {
                "name": self.current_info.get("name"),
                "known_facts": self.current_info.get("facts"), #[:5],  # Top 5 facts
                "preferences": self.current_info.get("preferences", {}),
                "is_returning_user": self.current_info["conversation_count"] > 0
            },
            "emotional_state": self.booting_info.get_feeling(),
            "session_metadata": {
                "message_count": len(self.buffer),
                "topics_discussed": self.current_info.get("topics_discussed", [])[-3:]
            }
        }
        
        return context

    def _clear_short_term_memory(self):
        self.buffer = []
        self.booting_info.set_mood("average day")
    
    def _save_conversations(self, role: str):
        # TODO: fix this
        pass

    def get_user(self):
        return self.user_id
    def get_current_user_info(self):
        return self.current_info


        
if __name__ == "__main__":
    aware = selfaware(user_id="Testing", agent_core=AgentCore())






