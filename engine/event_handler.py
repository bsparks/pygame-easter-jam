class EventHandler:
    def __init__(self):
        self.events = {}

    def add_listener(self, event_name, callback):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        if event_name in self.events:
            self.events[event_name].remove(callback)

    def emit(self, event_name, *args):
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(*args)
