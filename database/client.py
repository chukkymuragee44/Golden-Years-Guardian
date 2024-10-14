from database import MongoDB
from pymongo.collection import Collection


class ClientDB(MongoDB):
    def __init__(self):
        self.__client: Collection = self._db["client"]

    def save(self, content: dict) -> None:
        self.__client.insert_one(content)

    def retrieve(self) -> list[dict]:
        return list(self.__client.find())

    def retrieve_by(self, item_id: str) -> dict | None:
        client: dict | None = self.__client.find_one({"_id": item_id})
        if client:
            return dict(client)

    def retrieve_by_username(self, username: str) -> dict | None:
        client: dict | None = self.__client.find_one({"username": username})
        if client:
            return dict(client)

    def update(self, item_id: str, content: dict) -> None:
        if "_id" in content:
            del content["_id"]
        self.__client.update_one({"_id": item_id}, {"$set": content})

    def push_notifications(self, item_id: str, notification: dict) -> None:
        self.__client.update_one({"_id": item_id}, {"$push": {"notifications": notification}})

    def add_private_acceptance(self, client_id: str, private_id: str) -> None:
        self.__client.update_one({"_id": client_id}, {"$push": {"acceptance": private_id}})

    def remove_caregiver(self, client_id: str) -> None:
        self.__client.update_one({"_id": client_id}, {"$set": {"caregiver": ""}})

    def remove_caregiver_acceptance(self, client_id: str, private_id: str) -> None:
        self.__client.update_one({"_id": client_id}, {"$pull": {"acceptance": private_id}})
