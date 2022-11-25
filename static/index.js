function convertDatetimeLocal(datetime) {
    if (datetime == undefined) {
        datetime = new Date();
    }
    datetime.setMinutes(datetime.getMinutes() - datetime.getTimezoneOffset());
    return datetime.toISOString().slice(0,19);
}

function minDatetime(id) {
    element = document.getElementById(id);
    if (!id) { return; }
    datetime = new Date(Math.max(new Date(element.value).getTime(), new Date().getTime()))
    datetime = isNaN(datetime) ? new Date() : datetime;
    datetime = convertDatetimeLocal(datetime);
    element.min = datetime;
    element.value = datetime;
}

setInterval(minDatetime, 1000, "date");
setInterval(minDatetime, 1000, "alert");
setInterval(minDatetime, 1000, "joinAlert");

function register() {
    let username = document.getElementById("username").value;

    fetch(`users/${username}`, {
        method: "POST"
    });

    updateAppointments();
}

function updateAppointments() {
    let username = document.getElementById("username").value;
    let appointments = document.getElementById("appointments");

    fetch(`users/${username}/appointments`)
        .then((response) => response.json())
        .then((json) => {
            appointments.innerText = JSON.stringify(json, null, "\t");
        });
}

function newAppointment() {
    let username =  document.getElementById("username");
    let name =      document.getElementById("appointmentName");
    let dateTime =  document.getElementById("date");
    let alertTime = document.getElementById("alert");
    let guests =    document.getElementById("guests");

    username = username.value;
    name = name.value;
    dateTime = new Date(dateTime.value);
    alertTime = new Date(alertTime.value);
    guests = guests.value.split(',')

    body = {
        "guests": {},
        "alerts": {}
    }

    for (let i = 0; i < guests.length; i++) {
        body.guests[guests[i]] = true
    }

    if (document.getElementById("alertEnabled").checked) {
        body.alerts = {
            [username]: alertTime.getTime()/1000
        }
    }

    fetch(`appointments/${name}?user=${username}&date=${dateTime.getTime()/1000}`, {
        body: JSON.stringify(body),
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json"
        },
        method: "POST"
    });

    updateAppointments();
}

function joinAppointment() {

}

function cancelObject(url) {
    let username =  document.getElementById("username").value;
    let name =      document.getElementById("appointmentName").value;

    fetch(`${url}/${name}?user=${username}`, {
        method: "DELETE"
    });
    
    updateAppointments();
}

function cancel() {
    cancelObject("appointments")
}

function cancelAlert() {
    cancelObject("alerts")
}

function joinAlert() {
    
}