from typing import Any, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from bson import ObjectId


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, data: dict[str, Any]):
        data["user_id"] = ObjectId(user_id)
        insert_result = self.database["shanyraks"].insert_one(data)
        return insert_result.inserted_id

    def get_shanyrak(self, shanyrak_id: str):
        return self.database["shanyraks"].find_one({"_id": ObjectId(shanyrak_id)})

    def update_shanyrak(self, shanyrak_id: str, user_id: str, data: dict[str, Any]) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )

    def add_comment(self, shanyrak_id: str, comment: dict[str, str]):
        comment_id = str(ObjectId())
        comment["_id"] = comment_id
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$push": {"comments": comment}},
        )

    def update_comment(self, shanyrak_id: str, comments: List[dict[str, Any]]):
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(shanyrak_id)},
            {"$set": {"comments": comments}},
        )


