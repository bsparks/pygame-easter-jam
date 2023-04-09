import pygame

class Timer:
    def __init__(self, duration, position = (0, 0), font=None):
        self.position = position
        self.duration = duration
        self.paused = False
        self.running = False
        self.time = duration
        if font is None:
            self.font = pygame.font.SysFont("Arial", 16)
        else:
            self.font = font
        self.complete_listeners = []
        
    def add_complete_listener(self, listener):
        self.complete_listeners.append(listener)
        
    def start(self):
        self.running = True
        
    def pause(self):
        self.paused = True
        
    def resume(self):
        self.paused = False
        
    def reset(self):
        self.time = self.duration
        
    def on_timer_complete(self):
        self.running = False
        for listener in self.complete_listeners:
            listener()
        
    def update(self, dt):
        if self.running and not self.paused:
            self.time -= dt
            if self.time <= 0:
                self.on_timer_complete()
                
    def draw(self, surface):
        minutes = self.time // 1000 // 60
        seconds = self.time // 1000 % 60
        timer_text = self.font.render("{:02d}:{:02d}".format(minutes, seconds), True, "white")
        position = (self.position[0] - timer_text.get_width() // 2, self.position[1] - timer_text.get_height() // 2)
        surface.blit(timer_text, position)