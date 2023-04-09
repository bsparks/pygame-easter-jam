from .main_menu import MainMenu

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.main_menu = MainMenu(self)
        
        self.state = self.main_menu
        
    def startup(self):
        # do any global preloading?
        self.state.enter()
        
    def change_state(self, state):
        self.state.exit()
        self.state = state
        self.state.enter()
    
    def update(self, dt):
        self.state.update(dt)
    
    def draw(self):
        self.state.draw()