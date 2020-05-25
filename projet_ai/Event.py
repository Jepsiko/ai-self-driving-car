from weakref import WeakKeyDictionary


class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""

    def __init__(self):
        self.name = 'Generic Event'


class QuitEvent(Event):
    def __init__(self):
        super().__init__()
        self.name = 'Quit Event'


class TickEvent(Event):
    def __init__(self):
        super().__init__()
        self.name = 'Tick Event'


class ChangeModeEvent(Event):
    def __init__(self, mode):
        super().__init__()
        self.name = 'Change Mode Event'
        self.mode = mode


class ToggleDebugEvent(Event):
    def __init__(self):
        super().__init__()
        self.name = 'Toggle Debug Event'


class MapUpdatedEvent(Event):
    def __init__(self, map_):
        super().__init__()
        self.name = 'Map Updated Event'
        self.map = map_


class CarUpdatedEvent(Event):
    def __init__(self, car):
        super().__init__()
        self.name = 'Car Updated Event'
        self.car = car


class CreationEvent(Event):
    def __init__(self):
        super().__init__()
        self.name = 'Creation Event'


class RemovingEvent(Event):
    def __init__(self):
        super().__init__()
        self.name = 'Removing Event'


class MovePlayerEvent(Event):
    def __init__(self, acceleration, throttle):
        super().__init__()
        self.name = 'Move Player Event'
        self.acceleration = acceleration
        self.throttle = throttle


class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""

    def __init__(self):
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event):
        if not isinstance(event, TickEvent) and not isinstance(event, CarUpdatedEvent):
            print('Message: ' + event.name, end='')

            if isinstance(event, ChangeModeEvent):
                print(' (' + str(event.mode) + ')')
            elif isinstance(event, MovePlayerEvent):
                print(' (' + str(event.acceleration) + ', ' + str(event.throttle) + ')')
            else:
                print()

        for listener in self.listeners.keys():
            # NOTE: If the weakref has died, it will be
            # automatically removed, so we don't have
            # to worry about it.
            listener.notify(event)


class Listener:

    def __init__(self, evManager):
        self.evManager = evManager
        if self.evManager is not None:
            self.evManager.register_listener(self)

    def notify(self, event):
        pass
