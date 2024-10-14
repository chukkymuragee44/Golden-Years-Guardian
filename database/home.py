from pymongo.collection import Collection
from database import MongoDB


class HomeCareDB(MongoDB):
    def __init__(self):
        self.__home: Collection = self._db["home_caregivers"]

    def save(self, content: dict) -> None:
        self.__home.insert_one(content)

    def retrieve_by(self, item_id: str) -> dict:
        content: dict | None = self.__home.find_one({"_id": item_id})
        if content:
            return dict(content)

    def retrieve(self) -> list[dict]:
        return list(self.__home.find())

    def update(self, item_id: str, content: dict) -> None:
        self.__home.update_one({"_id": item_id}, {"$set": content})

    def push_notifications(self, item_id: str, notification: dict) -> None:
        self.__home.update_one({"_id": item_id}, {"$push": {"notifications": notification}})
