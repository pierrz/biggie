from pydantic import BeforeValidator
from typing_extensions import Annotated

# Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


# INVESTIGATE
# from bson import ObjectId

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")

# class User(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     # ... other fields ...

#     class Config:
#         json_encoders = {ObjectId: str}
