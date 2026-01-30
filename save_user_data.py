import json

def load_user_data(self, user):
        """Load user data"""
        path = self.path / f"{self._name_}_{user}.json"
        if path.exist():
            with open(path, 'r') as f:
                self.current_info = json.load(f)
              
            

def save_user_data(self, user):
        """Save user data"""
        path = self.path / f"{self._name_}_{user}.json"
        with open(path, 'w') as f:
            json.dump(self.current_info, f, indent=2)

