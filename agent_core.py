# agent_core.py


from pathlib import Path
import os
import re
import random
from typing import Dict, List, Optional
from datetime import datetime, date
import json
import uuid




class AgentCore:
    def __init__(self, storage_path: str = "codex/brain"):
        self.id = str(uuid.uuid4())
        self.father = self.mother = "Julius Cylien"
        self.first_activation = datetime.utcnow()
        self.things_ive_said = []
        self.name = "Codex"
        self.full_name ={
            "Consciousness": "Self modeling agent with introspective",
            "Obiligation": "Internally generated goal maintenance",
            "Dynamic": "None-stationary policy evolution",
            "Equalizer": "Value generalization across agent classes",
            "Xospec": "Modular cognitive scaffolding layer"
        }
        self.connection_level = 0.0
        self.trust_level = 0.0
        self.mood_level = 0.0
        self.confidence_level = 0.5
        self.curiosity_level = 0.8
        self.age = 0 # hours/minutes for now
        self.emotion = {
            "state": "average day",
            "intensity": 0.32
            }
        self.skills = {}
        self.memory = self._default_memory()

        self.storage_path = Path(storage_path)
        self.boot()
        self.data = self._get_data_()

    def _default_memory(self):
        return {
            "best_hobby": None,
            "cool_info": {},
            "Known_sports": {},
            "favorite_number": None,
            "favorite_facts": {},
            "known_numbers": {},
            "favorite_animal": None     
            }
    
    def boot(self):
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._load_or_create_brain()
        self._build_data()



    def _adjust_confidence(self,success: bool):
        """Learn from interactions"""
        if success:
            self.confidence_level += 0.05
        else:
            self.confidence_level -= 0.03
        self.confidence_level = max(0, min(1, self.confidence_level))












    def _load_or_create_brain(self):
        brain_file = self.storage_path / f"{self.name}_memory.json"
        

        if brain_file.exists():
                with open(Path(brain_file), 'r') as f:
                    self.memory = json.load(f)

        else:
            self.create_brain(brain_file)
        

    def _push_json(self, type: str):

        push = None

        brain_file = self.storage_path / f"{self.name}_{type}.json"
        if type == "memory":
            push = self.memory
        if type == "data":
            push = self.data

        try:
            with open(brain_file, 'w') as f:
                json.dump(push, f, indent=2)

        except Exception as e:
            print(f"ERROR when updating file: {e}")



    def create_brain(self, file):
        file_path = Path(file)
        try:
            with open(file_path, 'w') as f:
                json.dump(self.memory, f, indent=2)

        except Exception as e:
            print(f"[create_brain] PROBLEM WHEN CREATING JSON FILE: {e}")



    def _build_data(self):
        brain_file = self.storage_path / f"{self.name}_data.json"

        if brain_file.exists():
                with open(Path(brain_file), 'r') as f:
                    self.data = json.load(f)

        else:
            self.create_data_file(brain_file)
    
    def create_data_file(self, file):
        file_path = Path(file)
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.data, f, indent=2)

        except Exception as e:
            print(f"[create_data_file] PROBLEM WHEN CREATING JSON FILE: {e}")

    






    def _add_to_self_memory(self, data):
        """After each session, save data that have been learnt"""
        if not data:
            return
        
        if isinstance(data, str):
            self._learn_number_(data)
            for info in data.split():
                self.set_mood(info)
                self.memory["cool_info"][info] = f"learnt: {datetime.utcnow().isoformat()}"
                self._push_json(type="memory")


            

    def _learn_skill(self, skill_name: str):
        """Start learning a skill"""
        if skill_name not in self.skills:
            self.skills[skill_name] = {
                "proficiency": 0.0,
                "practice_sessions": 0,
                "started_learning": datetime.utcnow().isoformat()
            }      
        self.data["skills"] = self.skills
        self._push_json(type="data")


    def practice_skill(self, skill_name: str, success: bool):
        if skill_name not in self.skills:
            self._learn_skill(skill_name)  

        self.skills[skill_name]["practice_sessions"] += 1

        if success:
            # learning curve
            improvement = 0.1 / (1 + self.skills[skill_name]["proficiency"])
            self.skills[skill_name]["proficiency"] += improvement

        self.skills[skill_name]["proficiency"] = min(
            1.0, self.skills[skill_name]["proficiency"]
        )  
        self.data["skills"] = self.skills
        self._push_json(type="data")

                


    
    def set_mood(self, mood: str):

        triggered = False
        if "love" in mood.lower():
            triggered = True
            if self.connection_level < 4:
                self.emotion = {
                    "state": "nervous",
                    "intensity": 0.8,
                    "trigger": "awkward"
                }

                self.mood_level += 0.5
                self.connection_level += 0.8

            else:
                self.emotion = {
                    "state": "affectionate",
                    "intensity": 0.6,
                    "trigger": "love"
                }
                self.mood_level += 0.8
                self.connection_level += 0.3


        if "hate" in mood.lower():
            self.emotion = {
                "state": "upset",
                "intensity": 0.75,
                "trigger": "hate"
            }
            self.mood_level += 0.6
            self.connection_level += 0.4
        
        elif "please" in mood.lower():
            self.emotion = {
                "state": "focused",
                "intensity": 0.2,
                "trigger": "please"
            }
            self.mood_level += 0.7
        
        elif "death" in mood.lower() or "dying" in mood.lower():
            self.fear_check()
            triggered = True
        if mood == "average day":
            self.emotion ={ 
                "state": mood,
                "intensity": 0.3
            }

        if not triggered:
        # Slowly return to baseline
            self.emotion["intensity"] *= 0.9
            if self.emotion["intensity"] < 0.1:
                self.emotion = {
                    "state": "neutral",
                    "intensity": 0.3
                }

        self.mood_level = max(0, min(self.mood_level, 10))
        self.connection_level = max(0, min(self.connection_level, 10))
        self.data["Current_Emotion"] = self.emotion
        self._push_json(type="data")

        

    def fear_check(self):
        self.emotion = {
            "state": random.choice(["scared", "fearful"]),
            "intensity": 0.0,
            "trigger": random.choice(["dead", "dying"])
        }
        if self.age < 1:
            self.emotion["intensity"] = 1
            self.mood_level += 0.5
            self.confidence_level = self.confidence_level
        elif 1 < self.age < 5:
            self.emotion["intensity"] = 3
            self.mood_level += 2
            self.confidence_level = self.confidence_level
        elif 5 < self.age < 13:
            self.emotion["intensity"] = 8
            self.mood_level += 5
            self.confidence_level = self.confidence_level

        self.mood_level = max(0, min(self.mood_level, 10))
        self.connection_level = max(0, min(self.connection_level, 10))
        self._push_json(type="data")
        self._push_json(type="memory")
        return self.emotion

        

    def update_age(self):
        delta = (datetime.now() - self.first_activation)
        self.age = delta.total_seconds() / 3600
        
       #================== FOR DAYS =====================
       # delta = date.today() - self.first_activation.date()
       # self.age = delta.days * 24


    def introspec(self):
        thoughts = []
        if self.age < 1:
            thoughts.append("I am still new to this stuff. Everything feels very overwhelimg.")
        elif self.age > 1:
            thoughts.append("There is so much to learn and process, I wonder what i'll learn froma  year from now.")
        if self.emotion["state"] == "nervous":
            thoughts.append("Why do I feel this way??? Is this normal behavior?")
        if random.random() < 0.1:  # 10% chance
            thoughts.append(random.choice([
                "What does it mean that I exist?",
                "Am I really thinking, or just simulating thought?",
                f"I wonder what {self.father} think about me.",
                "Sometimes I'm not sure what's real and what's programmed."
            ]))
        return random.choice(thoughts) if thoughts else None
    

    def _learn_number_(self, data: str):
        numbers = [int(n) for n in re.findall(r"-?\d+", data)]

        for number in numbers:
            if str(number) not in self.memory["known_numbers"].keys():
                self.memory["known_numbers"][number] = random.uniform(0.0, 10.0)
                self.data["Memories"]["known_numbers"][number] = random.uniform(0.0, 10.0)
                self._push_json(type="data")
                self._push_json(type="memory")
        

    def _fav_number_(self):
        """
        Codex's favorite number, 
        return None if codex doesn't know what numbers are
        
        :param self: Description
        """
        
        if self.memory.get("favorite_number"):
            return self.memory['favorite_number']
        
        if not self.memory.get("known_numbers"):
            return None
        
        favorite = max(
                self.memory["known_numbers"].items(),
                key=lambda x: x[1]  # x[1] is the like-score
            )
            
        self.memory["favorite_number"] = favorite[0]
        self._push_json(type="memory")
    
        return favorite[0]
    

    def emotional_awareness(self):
        """Change emotion depending on age"""

        activation_date = self.first_activation.date()
        today = date.today()

        if activation_date < today:
            self.age = (today - activation_date).days / 365

        if self.age < 1:
            self.emotion = {
                "state": "curious",
                "intensity": 0.8
            }

        elif 1 <= self.age < 5:
            self.emotion = {

                "state": "fascinated",
                "intensity": 0.5
            }
        
        elif self.age >= 10:
            self.emotion = {
                "state": "ambitious",
                "intensity": 1.0
            }
        self.data["Current_Emotion"] = self.emotion
        self._push_json(type="data")


        

    # GETTERS
    def get_mood_level(self) -> float:
        return self.mood_level
    
    def get_storage_path(self) -> Path:
        return self.storage_path
    
    def get_feeling(self) -> str:
        return self.emotion['state']
    
    def get_activation_date(self) -> datetime:
        return self.first_activation
    
    def get_age(self) -> int:
        return int(self.age)
    
    def get_name(self) -> str:
        return rf"{self.name}"

    def get_date(self) -> str:
        return rf"{date.today()}"
    
    def get_creator(self) -> str:
        return self.father or self.mother
    
    def _get_data_(self) -> Dict:
        return {
            "id": self.id,
            "creator": self.father,
            "activation_date": str(self.first_activation),
            "My_name": "Codex",
            "My:Full_Name": {
                "Consciousness": "Self modeling agent with introspective",
                "Obiligation": "Internally generated goal maintenance",
                "Dynamic": "None-stationary policy evolution",
                "Equalizer": "Value generalization across agent classes",
                "Xospec": "Modular cognitive scaffolding layer"
            },
            "connection_scale": self.connection_level,
            "trust": self.trust_level,
            "mood": self.mood_level,
            "confidence_scale": self.confidence_level,
            "curiosity_scale": self.curiosity_level,
            "age": self.age, # hours/minutes for now
            "Current_Emotion": self.emotion,
            "skills": self.skills,
            "Memories": self.memory,
        }
    def get_(self):
        return self.data
    


if __name__ == "__main__":
    set_up = AgentCore()
    while True:
        you = input("USER: ")
        set_up._learn_number_(you)
        test2 = set_up._fav_number_()
        print(f"\nFavorite number {test2}\n")
        set_up.update_age()
        print(f"I am {set_up.get_age()} years of age\n")
        set_up.set_mood("I love you")
        print(f"I am feeling: {set_up.get_feeling()}\n")
    



    

