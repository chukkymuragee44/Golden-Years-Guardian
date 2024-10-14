from pymongo.collection import Collection
from database import MongoDB


class ClientRequestsToCaregiversDB(MongoDB):
    def __init__(self):
        self.__requests: Collection = self._db["requests"]

    def save(self, content: dict) -> None:
        self.__requests.insert_one(content)

    def retrieve(self) -> list[dict]:
        return list(self.__requests.find())

    def retrieve_by(self, item_id: str) -> dict:
        content: dict | None = self.__requests.find_one({"client": item_id})
        if content:
            return dict(content)

    def retrieve_by_two(self, client_id: str, caregiver_id: str) -> dict | None:
        content: dict | None = self.__requests.find_one({
            "client": client_id,
            "caregiver": caregiver_id
        })
        if content:
            return dict(content)

    def retrieve_all_by(self, item_id: str) -> list[dict]:
        return list(self.__requests.find({"client": item_id}))

    def update(self, item_id: str, content: dict) -> None:
        del content["_id"]
        self.__requests.update_one({"_id": item_id}, {"$set": content})

    def remove(self, client_id: str, caregiver_id: str) -> None:
        self.__requests.delete_one({
            "client": client_id,
            "caregiver": caregiver_id
        })


class PrivateClientsDB(MongoDB):
    def __init__(self, private_id: str):
        self.__clients: Collection = self._db[f"private_clients_{private_id}"]

    def save(self, content: dict) -> None:
        self.__clients.insert_one(content)

    def retrieve(self) -> list[dict]:
        return list(self.__clients.find())

    def retrieve_by(self, item_id: str) -> dict:
        content: dict | None = self.__clients.find_one({"_id": item_id})
        if content:
            return dict(content)

    def retrieve_all_by(self, item_id: str) -> list[dict]:
        return list(self.__clients.find({"client": item_id}))

    def add_schedule(self, client_id: str, schedule: dict) -> None:
        self.__clients.update_one({"_id": client_id}, {"$set": {"appointments": schedule}})

    def update_schedule(self, client_id: str, event: str, year: str, month: str, date: str) -> None:
        self.__clients.update_one({"_id": client_id}, {"$push": {
            f"appointments.{year}.{month}.{date}": event
        }})

    def remove_schedule(self, client_id: str, event: str, year: str, month: str, date: str) -> None:
        self.__clients.update_one({"_id": client_id}, {"$pull": {
            f"appointments.{year}.{month}.{date}": event
        }})

    def remove_client(self, client_id: str) -> None:
        self.__clients.delete_one({"_id": client_id})

    def get_event(self, client_id: str, year: str, month: str, date: str) -> list[str]:
        appointment: dict = self.__clients.find_one({"_id": client_id})
        if appointment and len(appointment["appointments"]) > 0 and year in appointment["appointments"]:
            if month in appointment["appointments"][year]:
                day_index: str = str(int(date) + 1)
                if day_index in appointment["appointments"][year][month]:
                    return appointment["appointments"][year][month][day_index]
        return []

    def update(self, item_id: str, content: dict) -> None:
        if "_id" in content:
            del content["_id"]
        self.__clients.update_one({"_id": item_id}, {"$set": content})


class PlatformContactsDB(MongoDB):
    def __init__(self):
        self.__contacts: Collection = self._db["contacts"]

    def save(self, contact: dict) -> None:
        self.__contacts.insert_one(contact)
