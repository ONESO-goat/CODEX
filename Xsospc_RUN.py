# Xsospec_RUN.py -- I am using this file to run the AI
from agent_core import AgentCore
from autonomous_loop import AutonomousLoop
from prompt_engine import Personailty
from example import main
import sys
from response_engine import PromptEngine
from opinion_system import OpinionSystem
from user_memory import selfaware
from memory_search import MemorySearch
from emotion_expression import FacialExpression


class Codex:
    """Main orchestrator - the 'brain' of Codex"""

    def __init__(self, user_id):
        # ONE core
        self.core = AgentCore()
        
        # All systems share the core
        
        self.personality = Personailty()
        self.expression = FacialExpression(self.core)
        self.memory = selfaware(self.core, user_id)
        self.opinions = OpinionSystem(self.core)
        self.autonomous = AutonomousLoop(user_id,self.core)
        self.engine = PromptEngine(self.core, self.personality, self.memory, session_id=user_id)
        self.memorySearch = MemorySearch(user_memory=self.memory.get_current_user_info())
    
    def start(self):
        """Boot everything"""
        self.core.boot()
        self.autonomous.boot_occuring_thoughts()
        self.memory.load_user_data()
    
    def chat(self, message: str):
        """Main interaction"""
        return self.engine.chat(message)
    
    def get_selfaware(self):
        """Achieve User Memory data"""
        return self.memory
    
    def get_OpinionSystem(self):
        """Achieve Opinion System data"""
        return self.opinions
    
    def end_session(self):
        """End session, save data"""
        return self.engine.end_session()
    
    def reset_conversation(self):
        return self.engine.reset_conversation()
    
    def get_AgentCore(self):
        return self.core
    def get_AutonmiousLoop(self):
        return self.autonomous
    def get_PromptEngine(self):
        return self.engine
    def get_FacialExpression(self):
        return self.expression




if __name__ == "__main__":
    
    
    print("=" * 60)
    print("      CODEX")
    print("=" * 60)
    
    # Get username
    username = input("LOG IN OR SIGN UP: ").strip()
    
    if not username:
        username = "guest"
    
    print(f"\n👋 Welcome, {username}!")
    codex = Codex(user_id=username.lower())
    agent = codex.get_AgentCore()
    engine = codex.get_PromptEngine()
    face = codex.get_FacialExpression()
    loop = codex.get_AutonmiousLoop()
    aware = codex.get_selfaware()
    
    try:

        
        # Check if returning user
        stats = engine.memory.get_summary_stats()
        if stats['total_conversations'] > 0:
            print(f"📚 Returning user - {stats['total_conversations']} previous conversations")
            print(f"📅 Last seen: {stats['last_seen']}")
        else:
            print("✨ New user - starting fresh!")
        
        print()
    except ConnectionError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


    while True:
        user = input(f"{username}:  ")
        aware._learn_about_the_person(response=user)
        response = engine.chat(response=user)
        create_face = face.check_emotion(response)
        faceial_expression = face.get_emotion()
        import logging

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('codex_debug.log'),
                logging.StreamHandler()  # Also print to console
            ]
        )

        logger = logging.getLogger('Codex')

        # Then use it:
        logger.debug(f"Context: {response}")
        #logger.error(f"JSON creation failed: {e}")
        logger.info(f"User message: {user}\n\n\n\n")
        print(f"CODEX: {response}")



# My name is julius, I like to play overwatch, and my favorite number is 666

# my name is julius , numbers are 1 2 3 4 5 6 7 8 9 10 , what is your favorite out this bunch