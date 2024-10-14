from flask import Response, render_template, redirect
from database.home import HomeCareDB
from utilities import generated_id, image_to_binary


class HomeCare:
    def __init__(self):
        self.__home_db: HomeCareDB = HomeCareDB()

    def room_booking_request_notification(self, private_id: str, client: dict, message: str) -> None:
        self.push_notification(
            private_id,
            image_to_binary("static/images/logo.png"),
            "Golden Years Garden",
            "A new client has made a request to meet you. Contact them at anytime "
            "to get more details"
        )
        if message != "":
            self.push_notification(
                private_id,
                client["photo"],
                f"{client['first_name']} {client['last_name']}",
                message
            )

    def registration(self, content: dict) -> str | Response:
        if content["agency_name"] == "":
            content["warning"] = "Please enter the agency name"
            return render_template("home/register.html", context=content)
        elif content["agency_email"] == "":
            content["warning"] = "Please enter the agency email"
            return render_template("home/register.html", context=content)
        elif content["agency_phone"] == "":
            content["warning"] = "Please enter the agency phone"
            return render_template("home/register.html", context=content)
        elif content["agency_website"] == "":
            content["warning"] = "Please enter the agency website"
            return render_template("home/register.html", context=content)
        elif content["agency_region"] == "":
            content["warning"] = "Please enter the region the agency is located"
            return render_template("home/register.html", context=content)
        elif content["agency_county"] == "":
            content["warning"] = "Please enter the county the agency is located"
            return render_template("home/register.html", context=content)
        elif content["agency_details"] == "":
            content["warning"] = "Please enter the details that describe your agency"
            return render_template("home/register.html", context=content)
        elif content["agency_image"] == "":
            content["warning"] = "Please enter the agency logo or banner"
            return render_template("home/register.html", context=content)
        home_id: str = generated_id()
        self.__home_db.save({
            "_id": home_id,
            "image": image_to_binary(f"static/images/{content['agency_image']}"),
            "name": content["agency_name"],
            "phone": content["agency_phone"],
            "email": content["agency_email"],
            "website": content["agency_website"],
            "region": content["agency_region"],
            "county": content["agency_county"],
            "details": content["agency_details"],
            "notifications": [{
                "image": image_to_binary("static/images/logo.png"),
                "title": "Golden Years Garden",
                "message": "Welcome to the Golden Years Garden Family\n"
                           "You have successfully registered with us as an agency "
                           "we are going to notify you of any requests from clients "
                           "to join your agency through the email you have provided "
                           "If you would like to change your details or you have any questions "
                           "about our platform, you can contact us through the website.\n"
                           "We are a platform that connects you to those who may need your "
                           "services, beyond that you are responsible on communicating "
                           "and scheduling when to meet and to provide the service."
            }]
        })
        return redirect("/home/success")

    @property
    def homes(self) -> list[dict]:
        return self.__home_db.retrieve()

    def home(self, home_id: str) -> dict:
        return self.__home_db.retrieve_by(home_id)

    def push_notification(self, home_id: str, image: str, title: str, message: str) -> None:
        self.__home_db.push_notifications(home_id, {
            "image": image,
            "title": title,
            "message": message
        })
