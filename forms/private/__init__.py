from flask import Response, render_template, session, redirect
from database.private import PrivateCareDB
from utilities import generated_id, image_to_binary


class PrivateCare:
    def __init__(self):
        self.__private_care_db: PrivateCareDB = PrivateCareDB()

    @staticmethod
    def __platform_introduction(private_name: str) -> dict:
        return {
            "image": image_to_binary("static/images/logo.png"),
            "title": "Golden Years Garden",
            "message": f"Welcome to the family {private_name}\n"
                       f"You can interact with your clients through "
                       f"our dashboard. We provide features that will "
                       f"make your experience in providing your clients "
                       f"with care.\nWe will notify you of any changes "
                       f"and inform you of any clients requests."
        }

    def room_booking_request_notification(self, private_id: str, client: dict, message: str) -> None:
        self.push_notification(
            private_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            "A new client has made a request to meet you, go to requests to view details"
        )
        if message != "":
            self.push_notification(
                private_id,
                client["photo"],
                f"{client['first_name']} {client['last_name']}",
                message
            )

    def client_joined_notification(self, private_id: str, client_name: str) -> None:
        self.push_notification(
            private_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"{client_name} your client has agreed to receive your care giving service. "
            f"You can start setting schedules. Go to the appointment page and start providing "
            f"your service."
        )

    def client_removed_notification(self, private_id: str, client_name: str) -> None:
        self.push_notification(
            private_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            f"{client_name} your client has decided that they no longer require your services. "
            f"We work hard to make the client experience better including allowing them to decided "
            f"which caregiver is best for them. Make sure to do your best to also provide the best "
            f"experience to your clients."
        )

    def registration(self, content: dict) -> str | Response:
        if content["private_name"] == "":
            content["warning"] = "Please enter your name"
            return render_template("private/register.html", context=content)
        elif content["private_email"] == "":
            content["warning"] = "Please enter your email"
            return render_template("private/register.html", context=content)
        elif content["private_phone"] == "":
            content["warning"] = "Please enter your phone number"
            return render_template("private/register.html", context=content)
        elif content["private_facebook"] == "":
            content["warning"] = "Please enter your facebook account"
            return render_template("private/register.html", context=content)
        elif content["private_instagram"] == "":
            content["warning"] = "Please enter your instagram account"
            return render_template("private/register.html", context=content)
        elif content["private_details"] == "":
            content["warning"] = "Please enter details about your service"
            return render_template("private/register.html", context=content)
        elif content["private_password"] == "":
            content["warning"] = "Please enter your login password"
            return render_template("private/register.html", context=content)
        elif content["private_image"] == "":
            content["warning"] = "Please enter a photo you would like to share"
            return render_template("private/register.html", context=content)
        private_id: str = generated_id()
        self.__private_care_db.save({
            "_id": private_id,
            "image": image_to_binary(f"static/images/{content['private_image']}"),
            "name": content["private_name"],
            "email": content["private_email"],
            "phone": content["private_phone"],
            "facebook": content["private_facebook"],
            "instagram": content["private_instagram"],
            "details": content["private_details"],
            "password": content["private_password"],
            "notifications": [self.__platform_introduction(content["private_name"])]
        })
        session["private_id"] = private_id
        return redirect("/private/dashboard")

    def update_details(self, private_id: str, content: dict) -> str | Response:
        if content["private_name"] == "":
            content["warning"] = "Please enter your name"
            return render_template("private/register.html", context=content)
        elif content["private_email"] == "":
            content["warning"] = "Please enter your email"
            return render_template("private/register.html", context=content)
        elif content["private_phone"] == "":
            content["warning"] = "Please enter your phone number"
            return render_template("private/register.html", context=content)
        elif content["private_facebook"] == "":
            content["warning"] = "Please enter your facebook account"
            return render_template("private/register.html", context=content)
        elif content["private_instagram"] == "":
            content["warning"] = "Please enter your instagram account"
            return render_template("private/register.html", context=content)
        elif content["private_details"] == "":
            content["warning"] = "Please enter details about your service"
            return render_template("private/register.html", context=content)
        elif content["private_password"] == "":
            content["warning"] = "Please enter your login password"
            return render_template("private/register.html", context=content)
        elif content["private_image"] == "":
            content["warning"] = "Please enter a photo you would like to share"
            return render_template("private/register.html", context=content)
        self.__private_care_db.update(private_id, {
            "_id": private_id,
            "image": content['private_image'],
            "name": content["private_name"],
            "email": content["private_email"],
            "phone": content["private_phone"],
            "facebook": content["private_facebook"],
            "instagram": content["private_instagram"],
            "details": content["private_details"],
            "password": content["private_password"]
        })
        session["private_id"] = private_id
        return redirect("/private/dashboard")

    def login(self, content: dict) -> str | Response:
        if content["login_email"] == "":
            content["warning"] = "Please enter your email"
            return render_template("private/login.html", context=content)
        elif content["login_password"] == "":
            content["warning"] = "Please enter your login password"
            return render_template("private/login.html", context=content)
        care_giver: dict = self.caregiver_by_email(content["login_email"])
        if care_giver:
            if care_giver["password"] != content["login_password"]:
                content["warning"] = "Wrong password"
                return render_template("private/login.html", context=content)
        else:
            content["warning"] = "Email does not exist"
            return render_template("private/login.html", context=content)
        session["private_id"] = care_giver["_id"]
        return redirect("/private/dashboard")

    @property
    def caregivers(self) -> list[dict]:
        return self.__private_care_db.retrieve()

    def caregiver(self, private_id: str) -> dict | None:
        return self.__private_care_db.retrieve_by(private_id)

    def caregiver_by_email(self, email: str) -> dict:
        return self.__private_care_db.retrieve_by_email(email)

    def notifications(self, private_id: str) -> list[dict]:
        care_giver: dict = self.caregiver(private_id)
        care_notifications: list[dict] = care_giver["notifications"]
        care_notifications.reverse()
        return care_notifications

    def push_notification(self, private_id: str, image: str, title: str, message: str) -> None:
        self.__private_care_db.push_notifications(private_id, {
            "image": image,
            "title": title,
            "message": message
        })
