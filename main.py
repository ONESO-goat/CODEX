from response_engine import PromptEngine
from user_memory import selfaware
from autonomous_loop import AutonomousLoop
import asyncio
import threading
import sys
from Xsospc_RUN import Codex

def run_autonomous_loop(system):
    asyncio.run(system.live())
def main():

    print("================")
    print("      CODEX     ")
    print("================")

    try:

        agent = Codex(user_id="cli_user")
            
            
        autonomous_thread = threading.Thread(
                    target=run_autonomous_loop, 
                    args=(agent.autonomous,),
                    daemon=True
                )
        autonomous_thread.start()
        print("✅✅✅ Agent initialized with local Ollama!\n")
    except ConnectionError as e:
        print(f"❌❌❌ Error: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                agent.end_session()
                print("\nBye")
                break
            
            if user_input.lower() == 'reset':
                agent.reset_conversation()
                print("\n🔄 Conversation reset!\n")
                continue
            
            if user_input.lower() == 'stats':
                stats = agent.memory.get_summary_stats()
                print(f"\n📊 Memory Stats:")
                for key, value in stats.items():
                    print(f"  - {key}: {value}")
                print()
                continue
            
            print("\n=> CODEX: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print(f"EMOTION: {}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            agent.end_session()
            break

if __name__ == "__main__":
    main()