import Pyro5.api
from Pyro5.server import expose
from datetime import datetime
from threading import Lock, Timer
from Utils.Appointment import Appointment


def printcall(f):
    def new(*args, **kwargs):
        print(f'{type(args[0]).__name__}.{f.__name__}', end="(")
        print(*args[1:], sep=", ", end="")
        print(**kwargs, sep=", ", end=")\n")
        return f(*args, **kwargs)
    return new


class ScheduledAlerts():
    def __init__(self, timer: Timer = None, appointments: list[Appointment] = []):
        self.timer = timer
        self.appointments: list[Appointment] = appointments


class Server(object):
    def __init__(self):
        self.users: dict[str, str] = {}
        self.usersMutex = Lock()
        self.appointments: dict[str, list[Appointment]] = {}
        self.scheduledAlerts: dict[datetime, ScheduledAlerts] = {}
        self.appointmentsMutex = Lock()
        pass

    def get_user(self, user: str):
        with self.usersMutex:
            if user not in self.users:
                return None
            return Pyro5.api.Proxy(self.users[user])

    @expose
    @printcall
    def register_user(self, user: str, uri: str):
        with self.usersMutex:
            self.users[user] = uri
        return "key"

    def alert(self, time: datetime):
        if time not in self.scheduledAlerts:
            return
        alert = self.scheduledAlerts[time]
        for appointment in alert.appointments:
            for user in appointment.alerts.keys():
                self.alert_event(user, appointment)

    def new_alert_timer(self, time: datetime):
        print(f'New timer: {time}')
        timer = Timer((time - datetime.now()).total_seconds(), self.alert, args=(time,))
        timer.start()
        return timer

    def get_appointment_by_name(self, user: str, appointmentName: str):
        appointment = self.appointments[user] if user in self.appointments else []
        appointment = [a for a in appointment if a.name == appointmentName]
        if len(appointment) == 0:
            return None
        return appointment[0]

    def add_user_appointment(self, user: str, appointment: Appointment):
        appointment.guests[user] = True
        if user not in self.appointments:
            self.appointments[user] = []
        appointments = self.appointments[user]
        appointments.append(appointment)
        appointments.sort()
        for user, alert in appointment.alerts.items():
            self.add_user_alert(user, appointment, alert)

    def remove_user_appointment(self, user: str, appointmentName: str):
        appointment: Appointment = self.get_appointment_by_name(user, appointmentName)
        if not appointment:
            return
        appointment.guests.pop(user, None)
        appointment.alerts.pop(user, None)
        if user in self.appointments:
            self.appointments[user] = [a for a in self.appointments[user] if a.name != appointmentName]

    def add_user_alert(self, user: str, appointment: Appointment, alert: datetime):
        appointment.alerts[user] = alert
        if alert in self.scheduledAlerts:
            self.scheduledAlerts[alert].appointments.append(appointment)
        else:
            self.scheduledAlerts[alert] = ScheduledAlerts(self.new_alert_timer(alert), [appointment])

    def remove_user_alert(self, user: str, appointmentName: str):
        appointment: Appointment = self.get_appointment_by_name(user, appointmentName)
        if not appointment:
            return
        alert = appointment.alerts.pop(user, None)
        if not alert:
            return
        if len([a for a in appointment.alerts.values() if a == alert]) == 0:
            self.scheduledAlerts[alert].appointments.remove(appointment)
        if (len(self.scheduledAlerts[alert].appointments) == 0):
            self.scheduledAlerts[alert].timer.cancel()
            del self.scheduledAlerts[alert]

    def new_appointment_event(self, user: str, appointment: Appointment):
        user = self.get_user(user)
        if user:
            user.new_appointment_event(appointment.to_dict())

    def alert_event(self, user: str, appointment: Appointment):
        user = self.get_user(user)
        if user:
            user.alert_event(appointment.to_dict())

    @expose
    @printcall
    def register_appointment(self, user: str, name: str, date: float, guests: dict[str, True], alerts: dict[str, float]):
        date = datetime.fromtimestamp(date)
        alerts = {user: datetime.fromtimestamp(alert) for user, alert in alerts.items()}
        with self.appointmentsMutex:
            if name in self.appointments:
                print(f'Appointment {name} already registered')
            appointment = Appointment(user, name, date, guests, alerts)
            guests = appointment.guests
            keys = list(guests.keys())
            while len(guests) > 0:
                guest = keys.pop()
                del guests[guest]
                self.new_appointment_event(guest, appointment)
            self.add_user_appointment(user, appointment)

    @expose
    @printcall
    def cancel_appointment(self, user: str, appointmentName: str):
        with self.appointmentsMutex:
            self.remove_user_appointment(user, appointmentName)

    @expose
    @printcall
    def register_alert(self, user: str, appointmentName: str, alert: float):
        alert = datetime.fromtimestamp(alert)
        with self.appointmentsMutex:
            appointment = self.get_appointment_by_name(user, appointmentName)
            if not appointment:
                return
            self.add_user_alert(user, appointment, alert)

    @expose
    @printcall
    def cancel_alert(self, user: str, appointmentName: str):
        with self.appointmentsMutex:
            self.remove_user_alert(user, appointmentName)

    @expose
    @printcall
    def get_appointments(self, user: str):
        with self.appointmentsMutex:
            if user in self.appointments:
                return [a.to_dict() for a in self.appointments[user]]
