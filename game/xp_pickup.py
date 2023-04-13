from .player import Player
from engine.pickup import Pickup

class XpPickup(Pickup):
    def __init__(self, value, position = None):
        image_name = "green_bean.png"
        if value >= 5:
            image_name = "red_bean.png"
        Pickup.__init__(self, image_name)
        self.value = value
        if position is not None:
            self.position = position
        
    def on_pickup(self, other):
        if isinstance(other, Player):
            other.add_xp(self.value)
        self.kill()