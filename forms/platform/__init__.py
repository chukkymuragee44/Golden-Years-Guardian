from datetime import datetime
from flask import Response, redirect
from utilities import generated_id
from database.platform import ClientRequestsToCaregiversDB, PrivateClientsDB, PlatformContactsDB


class PlatformCaregiverRequests:
    def __init__(self):
        self.__caregiver_requests_db: ClientRequestsToCaregiversDB = ClientRequestsToCaregiversDB()

    def save_private_request(self, client_id: str, private_id: str) -> Response:
        self.__caregiver_requests_db.save({
            "_id": generated_id(),
            "client": client_id,
            "caregiver": private_id,
            "category": "private"
        })
        return redirect(f"/client/booking/private/{private_id}/success")

    def save_home_request(self, client_id: str, home_id: str) -> Response:
        self.__caregiver_requests_db.save({
            "_id": generated_id(),
            "client": client_id,
            "caregiver": home_id,
            "category": "home"
        })
        return redirect(f"/client/booking/home/{home_id}/success")

    def remove_caregiver_request(self, client_id: str, private_id: str) -> None:
        self.__caregiver_requests_db.remove(client_id, private_id)

    @property
    def requests(self) -> list[dict]:
        return self.__caregiver_requests_db.retrieve()

    def single_request(self, client_id: str) -> dict:
        return self.__caregiver_requests_db.retrieve_by(client_id)

    def filtered_request(self, client_id: str) -> list[dict]:
        return self.__caregiver_requests_db.retrieve_all_by(client_id)


class PlatformPrivateClients:
    def __init__(self, private_id: str):
        self.__caregiver_requests_db: ClientRequestsToCaregiversDB = ClientRequestsToCaregiversDB()
        self.__caregiver_clients_db: PrivateClientsDB = PrivateClientsDB(private_id)

    @staticmethod
    def potential_clients_with_status(
            potential_clients: list[dict], all_clients: list[dict], private_id: str) -> list[dict]:
        my_clients: list[dict] = []
        for my_client in potential_clients:
            for other_client in all_clients:
                if my_client["_id"] == other_client["_id"]:
                    potential_client: dict = other_client
                    if my_client["active"]:
                        if other_client["caregiver"] == private_id:
                            potential_client["status"] = "active"
                        else:
                            potential_client["status"] = "unavailable"
                    else:
                        potential_client["status"] = "pending"
                    my_clients.append(potential_client)
                    break
        return my_clients

    def save_private_client(self, client_id: str, private_id: str) -> Response:
        self.__caregiver_clients_db.save({
            "_id": client_id,
            "active": False,
            "appointments": {}
        })
        self.__caregiver_requests_db.remove(client_id, private_id)
        return redirect(f"/private/clients")

    def activate_private_client(self, client_id: str) -> None:
        self.__caregiver_clients_db.update(client_id, {"active": True})

    def appointments_today(self, client_id: str) -> list[str]:
        today: datetime = datetime.now()
        year: str = today.strftime("%Y")
        month: str = today.strftime("%B").lower()
        date: str = today.strftime("%d")
        return self.__caregiver_clients_db.get_event(client_id, year, month, date)

    @property
    def clients(self) -> list[dict]:
        return self.__caregiver_clients_db.retrieve()

    def client(self, client_id: str) -> dict:
        return self.__caregiver_clients_db.retrieve_by(client_id)

    def remove_client_from_caregiver(self, client_id: str) -> None:
        self.__caregiver_clients_db.remove_client(client_id)

    def add_schedule(self, client_id: str, schedule: dict) -> None:
        self.__caregiver_clients_db.add_schedule(client_id, schedule)

    def update_schedule(self, client_id: str, event: str, year: str, month: str, date: str) -> None:
        self.__caregiver_clients_db.update_schedule(client_id, event, year, month, date)

    def remove_schedule(self, client_id: str, event: str, year: str, month: str, date: str) -> None:
        self.__caregiver_clients_db.remove_schedule(client_id, event, year, month, date)

    def clients_by(self, client_id: str) -> list[dict]:
        return self.__caregiver_clients_db.retrieve_all_by(client_id)


class PlatformContacts:
    def __init__(self):
        self.__contacts_db: PlatformContactsDB = PlatformContactsDB()

    def __add_message(self, content: dict) -> None:
        self.__contacts_db.save({
            "_id": generated_id(),
            "first_name": content["first_name"],
            "last_name": content["last_name"],
            "email": content["email"],
            "phone": content["phone"],
            "message": content["message"]
        })

    def contact_form(self, content: dict) -> bool:
        if content["first_name"] == "":
            content["warning"] = "Please enter your first name"
            return False
        elif content["last_name"] == "":
            content["warning"] = "Please enter your last name"
            return False
        elif content["email"] == "":
            content["warning"] = "Please enter your email"
            return False
        elif content["phone"] == "":
            content["warning"] = "Please enter your phone number"
            return False
        elif content["message"] == "":
            content["warning"] = "Please enter your message"
            return False
        self.__add_message(content)
        return True
