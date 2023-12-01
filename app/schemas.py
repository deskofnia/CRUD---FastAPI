from datetime import datetime
from typing import List
from pydantic import BaseModel
from bson.objectid import ObjectId

"""
In this section, you’ll create a Pydantic model to represent how data is stored in the MongoDB database and schemas that will be used by FastAPI to validate incoming and outgoing data.

Create a app/schemas.py file and add the following Pydantic schemas. The NoteBaseSchema represents the structure of the documents that will be stored in the MongoDB collection.

"""

class NoteBaseSchema(BaseModel):
    id: str | None = None
    title: str
    content: str
    category: str = ""
    published: bool = False
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateNoteSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    published: bool | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NoteResponse(BaseModel):
    status: str
    note: NoteBaseSchema

class ListNoteResponse(BaseModel):
    status: str
    results: int
    notes: List[NoteBaseSchema]

