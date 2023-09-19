class event:
    def __init__(self, id, event_time, event_type, arrival_time, service_time, interarrival_time):
        self.id = id
        self.event_time = event_time
        self.event_type = event_type
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.interarrival_time = interarrival_time
    def __lt__(self, other):
        return self.event_time < other.event_time

    def __repr__(self):
        return (f"ID: {self.id}, Time: {self.event_time}, Type: {self.event_type}, ST: {self.service_time}, AT: {self.arrival_time}, IA: {self.interarrival_time}\n")
