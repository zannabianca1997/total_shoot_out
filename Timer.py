class Timer(object):
    """A timer class"""

    def __init__(self, start_time : int = 0):
        self.time = start_time
        self.time_passed = 0
        self._on_frame = [] # [event, priority] priority is crescent
        self._timed_events = [] # [event, time_fire, repeat] repeat 0=non ripetere, altro ripeti ogni tot millisec

    def Frame(self, time_passed : int):
        self.time += time_passed
        self.time_passed = time_passed
        for  subscribed in self._on_frame:
            subscribed[0](time_passed)
        for event in self._timed_events:
            if self.time > event[1]:
                event[0](self.time)
                if event[2]: #se e' da ripetere
                    event[1] += event[2] #avanza l'evento
                else:
                    self._timed_events.remove(event)

    def subscribe(self, func : "the called function", priority : int = 0):
        "set a function you want to call every frame"
        i = 0
        while i <= len(self._on_frame):
            if i == len(self._on_frame) or self._on_frame[i][1] > priority:
                self._on_frame.insert(i,[func, priority])
                break
            i +=1

    def unsubscribe(self, func : "the called function"):
        "unset a function you wanted to call every frame"
        i = 0
        for subscribed in self._on_frame:
            if func == subscribed[0]:
                self._on_frame.remove(subscribed)
                break

    def set_event(self, event : "the called function", time_out : int, repeat_every : int = 0):
        "set a function you want to call after a certain time"
        self._timed_events.append([event, self.time + time_out, repeat_every])

    def unset_event(self, event : "the called function"):
        "unset a function you wanted to call after a certain time"
        for set_event in self._timed_events:
            if event == set_event[0]:
                self._timed_events.remove(set_event)
                break