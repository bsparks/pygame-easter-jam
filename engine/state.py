class State:
    def __init__(self, game):
        self.game = game
        
    def enter(self):
        pass
    
    def exit(self):
        pass
    
    def handle_events(self, events):
        pass
        
    def update(self, dt):
        pass
    
    def draw(self, surface):
        pass