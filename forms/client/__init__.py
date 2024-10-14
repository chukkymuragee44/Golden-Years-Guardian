from flask import Response, render_template, session, redirect

from database.client import ClientDB
from utilities import generated_id, image_to_binary


class Client:
    def __init__(self):
        self.__client_db: ClientDB = ClientDB()

    @staticmethod
    def __platform_introduction(client_name: str) -> dict:
        return {
            "image": image_to_binary("static/images/logo.png"),
            "title": "Golden Years Garden",
            "message": f"Welcome to the family {client_name}\n"
                       f"You can now start exploring home and "
                       f"private caregivers you would like to meet "
                       f"We provide the best experience in helping "
                       f"you find your caregiver."
        }

    def room_booking_notification(self, client_id: str, private_name: str) -> None:
        self.push_notification(
            client_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"Your request to meet {private_name} was sent, we will "
            f"notify you when the caregiver responds to your request"
        )

    def request_accepted_notification(self, client_id: str, caregiver: dict, message: str) -> None:
        self.push_notification(
            client_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"{caregiver['name']} the caregiver you requested has accepted your request and added you as a client, "
            f"Go to your appointment dashboard to confirm the request and avail yourself for your orientation. "
            f"Congratulations, I hope your stay with us will be productive"
        )
        if message != "":
            self.push_notification(
                client_id,
                caregiver["image"],
                caregiver["name"],
                message
            )

    def joined_caregiver_notification(self, client_id: str, private_name: str) -> None:
        self.push_notification(
            client_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"You have accepted {private_name} to be your caregiver. "
            f"Your care giver will be setting schedules on when they are going "
            f"to be available. You will find a calendar on the appointment page that "
            f"will update you on the schedules. I hope your stay with us will be productive."
        )

    def left_caregiver_notification(self, client_id: str, caregiver: dict, message: str) -> None:
        self.push_notification(
            client_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"You have decided to leave your caregiver {caregiver['name']}, we are sad to here that "
            f"I hope you can still find a caregiver that is ideal for you."
        )
        if message != "":
            if message != "":
                self.push_notification(
                    client_id,
                    caregiver["image"],
                    caregiver["name"],
                    message
                )

    def signup(self, content: dict) -> str | Response:
        if content["client_first_name"] == "":
            content["warning"] = "Please enter your first name"
            return render_template("client/signup.html", context=content)
        elif content["client_last_name"] == "":
            content["warning"] = "Please enter your last name"
            return render_template("client/signup.html", context=content)
        elif content["client_username"] == "":
            content["warning"] = "Please enter your username"
            return render_template("client/signup.html", context=content)
        elif content["client_age"] == "":
            content["warning"] = "Please enter your age"
            return render_template("client/signup.html", context=content)
        elif content["client_phone"] == "":
            content["warning"] = "Please enter your phone"
            return render_template("client/signup.html", context=content)
        elif content["client_email"] == "":
            content["warning"] = "Please enter your email"
            return render_template("client/signup.html", context=content)
        elif content["client_region"] == "":
            content["warning"] = "Please tell us the region you live"
            return render_template("client/signup.html", context=content)
        elif content["client_county"] == "":
            content["warning"] = "Please tell us the county you live"
            return render_template("client/signup.html", context=content)
        elif content["client_emergency_name"] == "":
            content["warning"] = "Please enter your emergency contact's name"
            return render_template("client/signup.html", context=content)
        elif content["client_emergency_contact"] == "":
            content["warning"] = "Please enter your emergency contact's phone number"
            return render_template("client/signup.html", context=content)
        elif content["client_children_number"] == "":
            content["warning"] = "Please tell us how many children you have"
            return render_template("client/signup.html", context=content)
        elif content["client_image"] == "":
            content["warning"] = "Please upload a phot of yourself"
            return render_template("client/signup.html", context=content)
        elif content["client_password"] == "":
            content["warning"] = "Please enter your login password"
            return render_template("client/signup.html", context=content)
        if content["client_age"] != "":
            age: int = int(content["client_age"])
            if age < 60:
                content["warning"] = "Your are too young to need elderly care"
                return render_template("client/signup.html", context=content)
        client_id: str = generated_id()
        self.__client_db.save({
            "_id": client_id,
            "photo": image_to_binary(f"static/images/{content['client_image']}"),
            "first_name": content["client_first_name"],
            "last_name": content["client_last_name"],
            "username": content["client_username"],
            "age": content["client_age"],
            "phone": content["client_phone"],
            "email": content["client_email"],
            "region": content["client_region"],
            "county": content["client_county"],
            "emergency_name": content["client_emergency_name"],
            "emergency_contact": content["client_emergency_contact"],
            "marital_status": content["client_marital_status"],
            "children_number": content["client_children_number"],
            "password": content["client_password"],
            "notifications": [self.__platform_introduction(content["client_first_name"])],
            "acceptance": [],
            "caregiver": ""
        })
        session["client_id"] = client_id
        return redirect("/client/dashboard")

    def update_details(self, client_id: str, content: dict) -> str | Response:
        if content["first_name"] == "":
            return redirect("/client/profile")
        elif content["last_name"] == "":
            return redirect("/client/profile")
        elif content["username"] == "":
            return redirect("/client/profile")
        elif content["age"] == "":
            return redirect("/client/profile")
        elif content["phone"] == "":
            return redirect("/client/profile")
        elif content["email"] == "":
            return redirect("/client/profile")
        elif content["region"] == "":
            return redirect("/client/profile")
        elif content["county"] == "":
            return redirect("/client/profile")
        elif content["emergency_name"] == "":
            return redirect("/client/profile")
        elif content["emergency_contact"] == "":
            return redirect("/client/profile")
        elif content["children"] == "":
            return redirect("/client/profile")
        elif content["password"] == "":
            return redirect("/client/profile")
        if content["age"] != "":
            age: int = int(content["age"])
            if age < 60:
                return redirect("/client/profile")
        self.__client_db.update(client_id, {
            "_id": client_id,
            "photo": content["profile_image"],
            "first_name": content["first_name"],
            "last_name": content["last_name"],
            "username": content["username"],
            "age": content["age"],
            "phone": content["phone"],
            "email": content["email"],
            "region": content["region"],
            "county": content["county"],
            "emergency_name": content["emergency_name"],
            "emergency_contact": content["emergency_contact"],
            "marital_status": content["marital_status"],
            "children_number": content["children"],
            "password": content["password"]
        })
        return redirect("/client/profile")

    def login(self, content: dict) -> str | Response:
        if content["client_username"] == "":
            content["warning"] = "Please enter your login username"
            return render_template("client/login.html", context=content)
        elif content["client_password"] == "":
            content["warning"] = "Please enter your login password"
            return render_template("client/login.html", context=content)
        client: dict | None = self.__client_db.retrieve_by_username(content["client_username"])
        if client:
            if client["username"] != content["client_username"]:
                content["warning"] = "Wrong password"
                return render_template("client/login.html", context=content)
        else:
            content["warning"] = "Username does not exist"
            return render_template("client/login.html", context=content)
        session["client_id"] = client["_id"]
        return redirect("/client/dashboard")

    @property
    def clients(self) -> list[dict]:
        return self.__client_db.retrieve()

    def details(self, client_id: str) -> dict:
        return self.__client_db.retrieve_by(client_id)

    @staticmethod
    def validate_caregiver_active(client: dict) -> None:
        if client["caregiver"] != "":
            client["status"] = "active"

    def add_private_acceptance(self, client_id: str, private_id: str) -> None:
        self.__client_db.add_private_acceptance(client_id, private_id)

    def set_caregiver(self, client_id: str, private_id: str) -> None:
        self.__client_db.update(client_id, {"caregiver": private_id})

    def remove_caregiver(self, client_id: str) -> None:
        self.__client_db.remove_caregiver(client_id)

    def remove_caregiver_acceptance(self, client_id: str, private_id: str) -> None:
        self.__client_db.remove_caregiver_acceptance(client_id, private_id)

    def push_notification(self, client_id: str, image: str, title: str, message: str) -> None:
        self.__client_db.push_notifications(client_id, {
            "image": image,
            "title": title,
            "message": message
        })

    def notifications(self, client_id: str) -> list[dict]:
        client: dict = self.details(client_id)
        client_notifications: list[dict] = client["notifications"]
        client_notifications.reverse()
        return client_notifications

    @staticmethod
    def validate_booked_rooms(caregivers: list[dict], rooms: list[dict], category: str, status: str) -> None:
        for client in rooms:
            for caregiver in caregivers:
                if client["caregiver"] == caregiver["_id"] and client["category"] == category:
                    caregiver["status"] = status
                    break

    @staticmethod
    def validate_accepted_rooms(caregivers: list[dict], client: dict, status: str) -> None:
        rooms: list[str] = client["acceptance"]
        for room in rooms:
            for caregiver in caregivers:
                if room == caregiver["_id"]:
                    if client["caregiver"] == "":
                        caregiver["status"] = status
                    else:
                        caregiver["status"] = "active"
                    break
