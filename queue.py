class QueueEvent:
    def __init__(self, delay, event_name, event_object):
        self.delay = delay
        self.event_name = event_name
        self.event_object = event_object
        self.done = False


class Queue:
    def __init__(self):
        self.events = []

    def tick(self):
        for event in self.events:
            # To do: remove event when done
            if event.done:
                continue

            event.delay -= 1
            if event.delay <= 0:
                self.execute_event(event)
                event.done = True

    def add(self, delay, event_name, event_object=None):
        event = QueueEvent(delay, event_name, event_object)
        self.events.append(event)

    def execute_event(self, event):
        if event.event_name == 'retire_car':
            event.event_object.retire()


queue = Queue()
