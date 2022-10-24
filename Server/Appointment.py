from datetime import datetime


class Appointment():
    def __init__(self, owner: str, date: datetime, guests: list[str] = {}, alerts: dict[str, datetime] = {}):
        self.owner: str = owner
        self.date: datetime = date
        self.guests: dict[str, True] = guests
        self.alerts: dict[str, datetime] = alerts
