import pygame

class ProgressBar:
    def __init__(self, position, size, color, max_value, value=0):
        self.position = position
        self.size = size
        self.color = color
        self.max_value = max_value
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        if self._value > self.max_value:
            self._value = self.max_value
        elif self._value < 0:
            self._value = 0
    
    def draw(self, surface):
        pygame.draw.rect(surface, "black", (self.position[0], self.position[1], self.size[0], self.size[1]))
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size[0] * (self.value / self.max_value), self.size[1]))