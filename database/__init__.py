from pymongo import MongoClient
from pymongo.database import Database


class MongoDB:
    __route: str = "mongodb://localhost:27017"

    @property
    def _db(self) -> Database:
        cluster_path: str = "elder_care"
        client: MongoClient = MongoClient(self.__route)
        return client[cluster_path]

    def save(self, content: dict) -> None:
        pass

    def retrieve(self) -> list[dict]:
        pass

    def retrieve_by(self, item_id: str) -> dict:
        pass

    def update(self, item_id: str, content: dict) -> None:
        pass

    def push_notifications(self, item_id: str, notification: dict) -> None:
        pass
