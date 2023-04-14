import pygame
from .event_handler import EventHandler


class Timer(EventHandler):
    def __init__(self, duration, position=(0, 0), font=None):
        EventHandler.__init__(self)
        self.position = position
        self.duration = duration
        self.paused = False
        self.running = False
        self.time = duration
        if font is None:
            self.font = pygame.font.SysFont("Arial", 16)
        else:
            self.font = font
        self.total_seconds = self.duration // 1000
        self.total_minutes = self.total_seconds // 60
        self.last_second = 1
        self.last_minute = 1

    def start(self):
        self.running = True
        self.total_seconds = self.duration // 1000
        self.total_minutes = self.total_seconds // 60
        self.last_second = 1
        self.last_minute = 1
        self.emit("start")

    def pause(self):
        self.paused = True
        self.emit("pause")

    def resume(self):
        self.paused = False
        self.emit("resume")

    def reset(self):
        self.time = self.duration
        self.start()

    def on_timer_complete(self):
        self.running = False
        self.time = 0
        self.emit("complete")

    def update(self, dt):
        if self.running and not self.paused:
            self.time -= dt
            # emit an event every second
            remaining_seconds = self.time // 1000
            remaining_minutes = remaining_seconds // 60
            second = self.total_seconds - remaining_seconds
            minute = self.total_minutes - remaining_minutes
            if second > self.last_second:
                self.emit("second", second)
                self.last_second = second
            if minute > self.last_minute:
                self.emit("minute", minute)
                self.last_minute = minute
            if self.time <= 0:
                self.on_timer_complete()

    def draw(self, surface):
        minutes = self.time // 1000 // 60
        seconds = self.time // 1000 % 60
        timer_text = self.font.render(
            "{:02d}:{:02d}".format(minutes, seconds), True, "white")
        position = (self.position[0] - timer_text.get_width() //
                    2, self.position[1] - timer_text.get_height() // 2)
        surface.blit(timer_text, position)
