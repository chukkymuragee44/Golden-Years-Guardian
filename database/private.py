from database import MongoDB
from pymongo.collection import Collection


class PrivateCareDB(MongoDB):
    def __init__(self):
        self.__caregiver_db: Collection = self._db["private_caregivers"]

    def save(self, content: dict) -> None:
        self.__caregiver_db.insert_one(content)

    def retrieve(self) -> list[dict]:
        return list(self.__caregiver_db.find())

    def retrieve_by(self, item_id: str) -> dict:
        content: dict | None = self.__caregiver_db.find_one({"_id": item_id})
        if content:
            return dict(content)

    def retrieve_by_email(self, email: str) -> dict | None:
        content: dict | None = self.__caregiver_db.find_one({"email": email})
        if content:
            return dict(content)

    def update(self, item_id: str, content: dict) -> None:
        if "_id" in content:
            del content["_id"]
        self.__caregiver_db.update_one({"_id": item_id}, {"$set": content})

    def push_notifications(self, item_id: str, notification: dict) -> None:
        self.__caregiver_db.update_one({"_id": item_id}, {"$push": {"notifications": notification}})
