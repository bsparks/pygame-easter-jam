from .main_menu import MainMenu
from .play import PlayState

# temp for testing
START_STATE = "main_menu"

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            "main_menu": MainMenu(self),
            "play": PlayState(self)
        }
        
        self.state = self.states[START_STATE]
        
    def startup(self):
        # do any global preloading?
        self.state.enter()
        
    def handle_events(self, events):
        self.state.handle_events(events)
        
    def change_state(self, state_name):
        self.state.exit()
        self.state = self.states[state_name]
        self.state.enter()
    
    def update(self, dt):
        self.state.update(dt)
    
    def draw(self):
        self.state.draw()