from flask import Flask, render_template, request, session, redirect, Response
from forms.platform import PlatformCaregiverRequests, PlatformPrivateClients, PlatformContacts
from forms.home import HomeCare
from forms.private import PrivateCare
from forms.client import Client

app: Flask = Flask(__name__)
app.secret_key = b'my_secret'

contact_platform: PlatformContacts = PlatformContacts()
requests_platform: PlatformCaregiverRequests = PlatformCaregiverRequests()
private_clients_platform: PlatformPrivateClients | None = None
my_client: Client = Client()
my_home_care: HomeCare = HomeCare()
my_private_care: PrivateCare = PrivateCare()


# root routes
@app.route("/", methods=["GET"])
def index() -> str:
    client: dict | None = None
    notifications: list[dict] = []
    if "client_id" in session.keys():
        client_id: str = session.get("client_id")
        client = my_client.details(client_id)
        notifications = my_client.notifications(client_id)
    return render_template(
        "index.html",
        client=client,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/about", methods=["GET"])
def about() -> str:
    client: dict | None = None
    notifications: list[dict] = []
    if "client_id" in session.keys():
        client_id: str = session.get("client_id")
        client = my_client.details(client_id)
        notifications = my_client.notifications(client_id)
    return render_template(
        "about.html",
        client=client,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts() -> str:
    client: dict | None = None
    notifications: list[dict] = []
    if "client_id" in session.keys():
        client_id: str = session.get("client_id")
        client = my_client.details(client_id)
        notifications = my_client.notifications(client_id)
    if request.method == "POST":
        content: dict = dict(request.form)
        status: bool = contact_platform.contact_form(content)
        if status:
            content["success"] = "Thank you for your message, we will get back to you"
        return render_template(
            "contacts.html",
            content=content,
            client=client,
            notifications=notifications,
            notification_count=len(notifications)
        )
    return render_template(
        "contacts.html",
        client=client,
        notifications=notifications,
        notification_count=len(notifications)
    )


# client routes
@app.route("/client/login", methods=["GET", "POST"])
def client_login() -> str | Response:
    if request.method == "GET":
        if "client_id" in session.keys():
            return redirect("/client/dashboard")
        return render_template("client/login.html")
    content: dict = dict(request.form)
    return my_client.login(content)


@app.route("/client/signup", methods=["GET", "POST"])
def client_signup() -> str | Response:
    if request.method == "GET":
        if "client_id" in session.keys():
            return redirect("/client/dashboard")
        return render_template("client/signup.html")
    content: dict = dict(request.form)
    return my_client.signup(content)


@app.route("/client/dashboard", methods=["GET"])
def client_dashboard() -> str | Response:
    global private_clients_platform
    if "client_id" not in session.keys():
        return redirect("/client/login")
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(client["caregiver"])
    homes: list[dict] = my_home_care.homes
    privates: list[dict] = my_private_care.caregivers
    notifications: list[dict] = my_client.notifications(client_id)
    schedule_today: list[str] = private_clients_platform.appointments_today(client_id)
    return render_template(
        "client/dashboard.html",
        client=my_client.details(client_id),
        homes=homes,
        home_count=len(homes),
        privates=privates,
        private_count=len(privates),
        notifications=notifications,
        notification_count=len(notifications),
        appointment_count=len(schedule_today)
    )


@app.route("/client/me", methods=["GET"])
def client_profile_me() -> dict:
    client_id: str = session.get("client_id")
    return my_client.details(client_id)


@app.route("/client/caregiver", methods=["GET"])
def client_profile_caregiver() -> dict:
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    private_id: str = client["caregiver"]
    caregiver: dict = my_private_care.caregiver(private_id)
    return caregiver


@app.route("/client/caregiver/schedule", methods=["GET"])
def client_caregiver_schedule() -> dict:
    global private_clients_platform
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    private_id: str = client["caregiver"]
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    active_client: dict = private_clients_platform.client(client_id)
    return active_client["appointments"]


@app.route("/client/profile", methods=["GET"])
def client_profile() -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    client_id: str = session.get("client_id")
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/profile.html",
        profile=my_client.details(client_id),
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/profile/update", methods=["POST"])
def client_profile_update() -> Response:
    if "client_id" in session.keys():
        content: dict = dict(request.form)
        client_id: str = session.get("client_id")
        return my_client.update_details(client_id, content)
    return redirect("/client/login")


@app.route("/client/home", methods=["GET"])
def client_home() -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    homes: list[dict] = my_home_care.homes
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    my_requests: list[dict] = requests_platform.filtered_request(client_id)
    my_client.validate_booked_rooms(homes, my_requests, "home", "pending")
    my_client.validate_accepted_rooms(homes, client, "accepted")
    notifications: list[dict] = my_client.notifications(client_id)
    if client["caregiver"] != "":
        client["status"] = "active"
    return render_template(
        "client/home.html",
        client=client,
        homes=homes,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/private", methods=["GET"])
def client_private() -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    privates: list[dict] = my_private_care.caregivers
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    my_requests: list[dict] = requests_platform.filtered_request(client_id)
    my_client.validate_booked_rooms(privates, my_requests, "private", "pending")
    my_client.validate_accepted_rooms(privates, client, "accepted")
    notifications: list[dict] = my_client.notifications(client_id)
    if client["caregiver"] != "":
        client["status"] = "active"
    return render_template(
        "client/private.html",
        client=client,
        privates=privates,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/caregiver/cancel", methods=["POST"])
def client_caregiver_cancel() -> Response:
    global private_clients_platform
    if "client_id" in session.keys():
        content: dict = dict(request.form)
        client_id: str = session.get("client_id")
        client: dict = my_client.details(client_id)
        private_id: str = client["caregiver"]
        if not private_clients_platform:
            private_clients_platform = PlatformPrivateClients(private_id)
        my_client.remove_caregiver(client_id)
        private_clients_platform.remove_client_from_caregiver(client_id)
        caregiver = my_private_care.caregiver(private_id)
        my_client.left_caregiver_notification(client_id, caregiver, content["client_message"])
        my_private_care.client_removed_notification(private_id, client["first_name"])
    return redirect("/client/private")


@app.route("/client/booking/home/<string:home_id>", methods=["GET", "POST"])
def client_booking_home(home_id: str) -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    care_giver: dict = my_home_care.home(home_id)
    if request.method == "GET":
        return render_template(
            "client/booking.html",
            home_id=home_id,
            home_name=care_giver["name"]
        )
    content: dict = dict(request.form)
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    if client["caregiver"] != "":
        return render_template(
            "client/booking.html",
            home_id=home_id,
            home_name=care_giver["name"],
            status="active"
        )
    my_client.room_booking_notification(client_id, care_giver["name"])
    my_home_care.room_booking_request_notification(home_id, client, content["client_message"])
    return requests_platform.save_home_request(client_id, home_id)


@app.route("/client/booking/home/<string:home_id>/success", methods=["GET"])
def client_booking_home_success(home_id: str) -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    caregiver: dict = my_home_care.home(home_id)
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/success.html",
        client=client,
        home_name=caregiver["name"],
        first_name=client["first_name"],
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/booking/private/<string:private_id>", methods=["GET", "POST"])
def client_booking_private(private_id: str) -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    care_giver: dict = my_private_care.caregiver(private_id)
    if request.method == "GET":
        return render_template(
            "client/booking.html",
            private_id=private_id,
            private_name=care_giver["name"]
        )
    content: dict = dict(request.form)
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    if client["caregiver"] != "":
        return render_template(
            "client/booking.html",
            private_id=private_id,
            private_name=care_giver["name"],
            status="active"
        )
    my_client.room_booking_notification(client_id, care_giver["name"])
    my_private_care.room_booking_request_notification(private_id, client, content["client_message"])
    return requests_platform.save_private_request(client_id, private_id)


@app.route("/client/booking/private/<string:private_id>/success", methods=["GET"])
def client_booking_private_success(private_id: str) -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    caregiver: dict = my_private_care.caregiver(private_id)
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/success.html",
        client=client,
        private_name=caregiver["name"],
        first_name=client["first_name"],
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/appointments", methods=["GET"])
def client_appointments() -> str | Response:
    if "client_id" not in session.keys():
        return redirect("/client/login")
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    if client["caregiver"] != "":
        return redirect(f"/client/appointments/{client['caregiver']}/client")
    privates: list[dict] = my_private_care.caregivers
    my_requests: list[dict] = requests_platform.filtered_request(client_id)
    my_client.validate_booked_rooms(privates, my_requests, "private", "pending")
    my_client.validate_accepted_rooms(privates, client, "accepted")
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/appointments.html",
        client=client,
        privates=privates,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/appointments/<string:private_id>/join", methods=["GET"])
def client_appointments_join(private_id: str) -> str | Response:
    global private_clients_platform
    if "client_id" not in session.keys():
        return redirect("/client/login")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    client_id: str = session.get("client_id")
    client: dict = my_client.details(client_id)
    if client["caregiver"] == "":
        private_clients_platform.activate_private_client(client_id)
        my_client.set_caregiver(client_id, private_id)
        my_client.remove_caregiver_acceptance(client_id, private_id)
        caregiver: dict = my_private_care.caregiver(private_id)
        my_client.joined_caregiver_notification(client_id, caregiver["name"])
        my_private_care.client_joined_notification(private_id, client["first_name"])
    return redirect(f"/client/appointments/{private_id}/client")


@app.route("/client/appointments/<string:private_id>/client", methods=["GET"])
def client_appointments_client(private_id: str) -> str | Response:
    global private_clients_platform
    if "client_id" not in session.keys():
        return redirect("/client/login")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    client_id: str = session.get("client_id")
    caregiver: dict = my_private_care.caregiver(private_id)
    client: dict = my_client.details(client_id)
    my_client.validate_caregiver_active(client)
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/appointments.html",
        client=client,
        private=caregiver,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/client/appointments/<string:private_id>/cancel", methods=["GET"])
def client_appointments_client_cancel(private_id: str) -> str | Response:
    global private_clients_platform
    if "client_id" not in session.keys():
        return redirect("/client/login")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    client_id: str = session.get("client_id")
    caregiver: dict = my_private_care.caregiver(private_id)
    client: dict = my_client.details(client_id)
    my_client.validate_caregiver_active(client)
    notifications: list[dict] = my_client.notifications(client_id)
    return render_template(
        "client/appointments.html",
        client=client,
        private=caregiver,
        notifications=notifications,
        notification_count=len(notifications),
        cancelling=True
    )


@app.route("/client/logout", methods=["GET"])
def client_logout() -> Response:
    if "client_id" in session.keys():
        del session["client_id"]
    return redirect("/client/login")


# home care routes
@app.route("/home", methods=["GET"])
def home() -> str:
    client: dict | None = None
    notifications: list[dict] = []
    homes: list[dict] = my_home_care.homes
    if "client_id" in session.keys():
        client_id: str = session.get("client_id")
        client = my_client.details(client_id)
        my_requests: list[dict] = requests_platform.filtered_request(client_id)
        my_client.validate_booked_rooms(homes, my_requests, "home", "pending")
        my_client.validate_accepted_rooms(homes, client, "accepted")
        notifications = my_client.notifications(client_id)
    return render_template(
        "home/index.html",
        homes=homes,
        client=client,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/home/register", methods=["GET", "POST"])
def home_register() -> str:
    if request.method == "GET":
        return render_template("home/register.html")
    content: dict = dict(request.form)
    return my_home_care.registration(content)


@app.route("/home/success", methods=["GET"])
def home_register_success() -> str:
    return render_template("home/success.html")


# private care routes
serving_client: dict = {}


def get_selected_private_clients(private_id: str) -> list[dict]:
    global private_clients_platform
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    potential_clients: list[dict] = private_clients_platform.clients
    all_clients: list[dict] = my_client.clients
    return private_clients_platform.potential_clients_with_status(potential_clients, all_clients, private_id)


@app.route("/private", methods=["GET"])
def private() -> str:
    client: dict | None = None
    notifications: list[dict] = []
    caregivers: list[dict] = my_private_care.caregivers
    if "client_id" in session.keys():
        client_id: str = session.get("client_id")
        client = my_client.details(client_id)
        my_requests: list[dict] = requests_platform.filtered_request(client_id)
        my_client.validate_booked_rooms(caregivers, my_requests, "private", "pending")
        my_client.validate_accepted_rooms(caregivers, client, "accepted")
        notifications = my_client.notifications(client_id)
    return render_template(
        "private/index.html",
        privates=caregivers,
        client=client,
        notifications=notifications,
        notification_count=len(notifications)
    )


@app.route("/private/client/serving", methods=["GET"])
def private_client_serving() -> dict:
    return serving_client


@app.route("/private/client/serving/schedule", methods=["GET", "POST"])
def private_client_serving_schedule() -> dict:
    global private_clients_platform
    private_id: str = session.get("private_id")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    if request.method == "GET":
        active_client: dict = private_clients_platform.client(serving_client["_id"])
        return active_client["appointments"]
    schedule: dict = request.get_json()
    private_clients_platform.add_schedule(serving_client["_id"], schedule)
    return {"res": "ok"}


@app.route(
    "/private/client/serving/schedule/remove/<string:event>/<string:year>/<string:month>/<string:date>",
    methods=["GET"]
)
def private_client_serving_schedule_remove(event: str, year: str, month: str, date: str) -> dict:
    global private_clients_platform
    private_id: str = session.get("private_id")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    private_clients_platform.remove_schedule(serving_client["_id"], event, year, month, date)
    return {"res": "ok"}


@app.route("/private/client/serving/schedule/<string:year>/<string:month>/<string:date>", methods=["POST"])
def private_client_serving_schedule_update(year: str, month: str, date: str) -> dict:
    global private_clients_platform
    private_id: str = session.get("private_id")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    schedule: dict = request.get_json()
    private_clients_platform.update_schedule(serving_client["_id"], schedule["event"], year, month, date)
    return {"res": "ok"}


@app.route("/private/register", methods=["GET", "POST"])
def private_register() -> str | Response:
    if "private_id" in session.keys():
        return redirect("/private/dashboard")
    if request.method == "GET":
        return render_template("private/register.html")
    content: dict = dict(request.form)
    return my_private_care.registration(content)


@app.route("/private/login", methods=["GET", "POST"])
def private_login() -> str | Response:
    if "private_id" in session.keys():
        return redirect("/private/dashboard")
    if request.method == "GET":
        return render_template("private/login.html")
    content: dict = dict(request.form)
    return my_private_care.login(content)


@app.route("/private/dashboard", methods=["GET"])
def private_dashboard() -> str | Response:
    global private_clients_platform
    if "private_id" in session.keys():
        private_id: str = session.get("private_id")
        if not private_clients_platform:
            private_clients_platform = PlatformPrivateClients(private_id)
        client_count: int = len(private_clients_platform.clients)
        caregiver: dict = my_private_care.caregiver(private_id)
        request_count: int = len(requests_platform.requests)
        notifications: list[dict] = my_private_care.notifications(private_id)
        return render_template(
            "private/dashboard.html",
            private=caregiver,
            request_count=request_count,
            client_count=client_count,
            notifications=notifications,
            notification_count=len(notifications)
        )
    return redirect("/private/login")


@app.route("/private/profile", methods=["GET"])
def private_profile() -> str | Response:
    if "private_id" in session.keys():
        private_id: str = session["private_id"]
        notifications: list[dict] = my_private_care.notifications(private_id)
        return render_template(
            "private/profile.html",
            private=my_private_care.caregiver(private_id),
            notifications=notifications,
            notification_count=len(notifications)
        )
    return redirect("/private/login")


@app.route("/private/profile/update", methods=["POST"])
def private_profile_update() -> Response:
    if "private_id" in session.keys():
        content: dict = dict(request.form)
        private_id: str = session.get("private_id")
        my_private_care.update_details(private_id, content)
        return redirect("/private/profile")
    return redirect("/private/login")


@app.route("/private/appointments", methods=["GET"])
def private_appointments() -> str | Response:
    if "private_id" in session.keys():
        private_id: str = session.get("private_id")
        caregiver: dict = my_private_care.caregiver(private_id)
        clients: list[dict] = get_selected_private_clients(private_id)
        notifications: list[dict] = my_private_care.notifications(private_id)
        return render_template(
            "private/appointments.html",
            private=caregiver,
            clients=clients,
            notifications=notifications,
            notification_count=len(notifications)
        )
    return redirect("/private/login")


@app.route("/private/clients", methods=["GET"])
def private_clients() -> str | Response:
    if "private_id" in session.keys():
        private_id: str = session.get("private_id")
        clients: list[dict] = get_selected_private_clients(private_id)
        notifications: list[dict] = my_private_care.notifications(private_id)
        return render_template(
            "private/clients.html",
            private=my_private_care.caregiver(private_id),
            clients=clients,
            notifications=notifications,
            notification_count=len(notifications)
        )
    return redirect("/private/login")


@app.route("/private/clients/<string:client_id>", methods=["GET"])
def private_single_client(client_id: str) -> str | Response:
    global private_clients_platform
    if "private_id" in session.keys():
        private_id: str = session.get("private_id")
        if not private_clients_platform:
            private_clients_platform = PlatformPrivateClients(private_id)
        notifications: list[dict] = my_private_care.notifications(private_id)
        client: dict = private_clients_platform.client(client_id)
        single_client: dict = my_client.details(client["_id"])
        if single_client["caregiver"] != "":
            single_client["status"] = "active"
        if client:
            return render_template(
                "private/clients.html",
                private=my_private_care.caregiver(private_id),
                notifications=notifications,
                notification_count=len(notifications),
                single_request=single_client
            )
        return redirect("/private/clients")
    return redirect("/private/login")


@app.route("/private/clients/<string:client_id>/appointments", methods=["GET"])
def private_single_client_appointments(client_id: str) -> str | Response:
    global serving_client
    if "private_id" not in session.keys():
        return redirect("/private/login")
    private_id: str = session.get("private_id")
    notifications: list[dict] = my_private_care.notifications(private_id)
    single_client: dict = my_client.details(client_id)
    if single_client["caregiver"] != "":
        single_client["status"] = "scheduling"
    serving_client = single_client
    return render_template(
        "private/appointments.html",
        private=my_private_care.caregiver(private_id),
        notifications=notifications,
        notification_count=len(notifications),
        single_request=single_client
    )


@app.route("/private/requests", methods=["GET"])
def private_requests() -> str | Response:
    if "private_id" in session.keys():
        private_id: str = session["private_id"]
        notifications: list[dict] = my_private_care.notifications(private_id)
        client_requests: list[dict] = requests_platform.requests
        clients: list[dict] = list(map(lambda client: my_client.details(client["client"]), client_requests))
        return render_template(
            "private/requests.html",
            private=my_private_care.caregiver(private_id),
            notifications=notifications,
            notification_count=len(notifications),
            clients=clients
        )
    return redirect("/private/login")


@app.route("/private/requests/<client_id>", methods=["GET"])
def private_requests_client(client_id: str) -> str | Response:
    if "private_id" in session.keys():
        private_id: str = session["private_id"]
        notifications: list[dict] = my_private_care.notifications(private_id)
        my_request: dict = requests_platform.single_request(client_id)
        if my_request:
            return render_template(
                "private/requests.html",
                private=my_private_care.caregiver(private_id),
                notifications=notifications,
                notification_count=len(notifications),
                single_request=my_client.details(my_request["client"])
            )
        return redirect("/private/requests")
    return redirect("/private/login")


@app.route("/private/requests/add_client/<client_id>", methods=["GET", "POST"])
def private_requests_add_client(client_id: str) -> str | Response:
    global private_clients_platform
    if "private_id" not in session.keys():
        return redirect("/private/login")
    private_id: str = session.get("private_id")
    if not private_clients_platform:
        private_clients_platform = PlatformPrivateClients(private_id)
    caregiver: dict = my_private_care.caregiver(private_id)
    if request.method == "GET":
        notifications: list[dict] = my_private_care.notifications(private_id)
        my_request: dict = requests_platform.single_request(client_id)
        single_request: dict = {}
        if my_request:
            single_request = my_client.details(my_request["client"])
        return render_template(
            "private/requests.html",
            private=caregiver,
            notifications=notifications,
            notification_count=len(notifications),
            single_request=single_request,
            add_client="add",
        )
    content: dict = dict(request.form)
    if content["private_message"] == "":
        content["warning"] = "Please write a message to the client"
        notifications: list[dict] = my_private_care.notifications(private_id)
        my_request: dict = requests_platform.single_request(client_id)
        return render_template(
            "private/requests.html",
            private=caregiver,
            notifications=notifications,
            notification_count=len(notifications),
            single_request=my_client.details(my_request["client"]),
            add_client="add",
            context=content
        )
    my_client.add_private_acceptance(client_id, private_id)
    my_client.request_accepted_notification(client_id, caregiver, content["private_message"])
    return private_clients_platform.save_private_client(client_id, private_id)


@app.route("/private/logout", methods=["GET"])
def private_logout() -> Response:
    if "private_id" in session.keys():
        del session["private_id"]
    return redirect("/private/login")


if __name__ == '__main__':
    # app.run(host="localhost", port=5000)
    app.run(host="localhost", port=5000, debug=True)
