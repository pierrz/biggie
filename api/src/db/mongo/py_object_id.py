from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

# DISCARDED (lacks the advanced features and consistency guarantees that the class-based approach)
# Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
# from pydantic import BeforeValidator
# from typing_extensions import Annotated
# PyObjectId = Annotated[str, BeforeValidator(str)]


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return ObjectId(value)

    @classmethod
    def __modify_json_schema__(cls, json_schema: JsonSchemaValue) -> JsonSchemaValue:
        json_schema.update(type="string")
        return json_schema
