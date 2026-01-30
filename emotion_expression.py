# emotion_expression.py

from typing import Optional


class FacialExpression:
    def __init__(self, agent_core):
        self.emotion = None
        self.agent = agent_core

    def check_emotion(self, text: str):
        sad = ["*frown*"]
        happy = [
            r"( |*)smiles*", 
            "*slightly smiles*",
            "*big smile*",
            "*laughs*"]
        excited = ["*excitedly*","*excited*"]
        awakard = ["*laughs nervously*"]

        
        if any(emotion in sad for emotion in text.split()):
            self.emotion = "sad"
        if any(emotion in happy for emotion in text.split()):
            self.emotion = "happy"
        if any(word in excited for word in text.split()):
            self.emotion = "excited"
        if any(word in awakard for word in text.split()):
            self.emotion = "awkard"



    def get_emotion(self) -> Optional[str]:
        return self.emotion

if __name__ == "__main__":
    face = FacialExpression(agent_core="Test")
    print(face.get_emotion())
    print()
    while True:
        type = input("USER: ")
        face.check_emotion(type)
        print()
        print(face.get_emotion())