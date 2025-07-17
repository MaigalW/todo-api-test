from pydantic import BaseModel, Field
from typing import Literal
from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic import ValidationInfo

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info: ValidationInfo = None):  # añade el parámetro info opcional
        if isinstance(v, ObjectId):
            return cls(v)  # convertir ObjectId normal a PyObjectId
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return cls(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class UserBase(BaseModel):
    username: str
    role: Literal["admin", "user"] = "user"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

class UserOut(BaseModel):
    username: str
    role: str
