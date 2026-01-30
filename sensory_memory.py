from datetime import datetime


class SensoryMemory:
    """What is happening at the current moment"""
    def __init__(self):
        self.current_input = None
        self.attention_focus = []
        self.recent_stimuli = []
    
    def _current_moment(self):
        date = ...