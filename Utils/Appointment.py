from datetime import datetime


class Appointment():
    def __init__(self, owner: str, name: str, date: datetime, guests: dict[str, True] = {}, alerts: dict[str, datetime] = {}):
        self.owner: str = owner
        self.name: str = name
        self.date: datetime = date
        self.guests: dict[str, True] = guests
        self.alerts: dict[str, datetime] = alerts

    def to_dict(self):
        return {
            'owner': self.owner,
            'name': self.name,
            'date': self.date,
            'guests': self.guests,
            'alerts': self.alerts
        }

    def __lt__(self, other):
        return self.date < other.date
