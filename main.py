from Server import Server
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict

app = FastAPI()
server = Server()

@app.post("/users/{user}")
async def register_user(user: str):
    server.register_user(user)

@app.get("/users/{user}/appointments")
async def get_appointments(user: str):
    return server.get_appointments(user)

@app.post("/appointments/{appointment_name}")
async def register_appointment(user: str, appointment_name: str, date: float, guests: Dict[str, bool], alerts: Dict[str, float]):
    server.register_appointment(user, appointment_name, date, guests, alerts)

@app.put("/appointments/{appointment_name}")
async def join_appointment(user: str, owner: str, appointment_name: str):
    pass

@app.delete("/appointments/{appointment_name}")
async def cancel_appointment(user: str, appointment_name: str):
    server.cancel_appointment(user, appointment_name)

@app.post("/alerts/{appointment_name}")
async def register_alert(user: str, owner: str, appointment_name: str):
    pass

@app.delete("/alerts/{appointment_name}")
async def cancel_alert(user: str, appointment_name: str):
    server.cancel_alert(user, appointment_name)


@app.get("/")
async def root():
    return RedirectResponse("index.html")

app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    print('Please run with: "uvicorn main:app"')