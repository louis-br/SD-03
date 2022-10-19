from Pyro5.server import expose

class Server(object):
    def __init__(self):
        pass

    @expose
    def register_user(self):
        print("register_user")

    @expose
    def register_appointment(self):
        print("register_appointment")

    @expose
    def cancel_appointment(self):
        print("cancel_appointment")

    @expose
    def cancel_alert(self):
        print("cancel_alert")

    @expose
    def get_appointments(self):
        print("get_appointments")