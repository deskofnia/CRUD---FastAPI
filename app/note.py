"""
To reduce the complexity of the project, we’ll implement all the business logic related to the CRUD operations directly in the path operation functions. However, you can extract the business logic from the route handlers into a separate file as a challenge. This will make your code more modular and easier to test.

So, create a app/note.py file and add these imports. Also, since we want to create the path operation functions in a separate file, instantiate the APIRouter class and assign it to a router variable.

"""

from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Note
from app.note_serializers import noteEntity, noteListEntity
from bson.objectid import ObjectId

router = APIRouter()

"""
The first path operation function will be responsible for retrieving all the documents in the collection or a paginated list of the documents. When a GET request hits the /api/notes endpoint, FastAPI will delegate the request to this route handler to retrieve a selection of documents in the database.

In the above, we created a MongoDB aggregation pipeline to perform operations like:

Sorting
Filtering
Limiting
Next, we passed the aggregation pipeline to the Note.aggregate() method in order to retrieve a paginated list of the documents in the database. The noteListEntity() method will then parse the list of documents returned by MongoDB into Python dictionaries.

"""
@router.get('/', response_model=schemas.ListNoteResponse)
def get_notes(limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {'title': {'$regex': search, '$options': 'i'}}},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    notes = noteListEntity(Note.aggregate(pipeline))
    return {'status': 'success', 'results': len(notes), 'notes': notes}


"""
The second path operation function will be responsible for adding new documents to the database. FastAPI will forward any POST request that matches /api/notes to this route handler.

When this route controller is evoked, Pydantic will read the request body as JSON, validate the JSON against the provided schema and assign the payload data to the payload variable.

Next, we converted the JSON payload into a Python dictionary by evoking the .dict() method and passed the result as an argument to the Note.insert_one() method. The .insert_one() method will query the MongoDB database to add the new document to the collection and return the ObjectId of the newly-added document.

So, to retrieve the newly-created document, we had to call the Note.find_one() method with the ObjectId.

"""

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse)
def create_note(payload: schemas.NoteBaseSchema):
    payload.createdAt = datetime.utcnow()
    payload.updatedAt = payload.createdAt
    try:
        result = Note.insert_one(payload.dict(exclude_none=True))
        new_note = Note.find_one({'_id': result.inserted_id})
        return {"status": "success", "note": noteEntity(new_note)}
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Note with title: {payload.title} already exists")


"""
This path operation function will be called to edit a document in the collection whenever a /api/notes/{noteId} PATCH request hits the server. When the request is delegated to this handler, Pydantic will validate the request body against the schemas.UpdateNoteSchema and assign the resulting JSON to the payload variable.

Also, the Id of the document to be updated will be extracted from the URL parameters and assigned to the noteId variable.

Then, the ObjectId.is_valid() method will be called to check if the provided Id is a valid ObjectId before the Note.find_one_and_update() method will be evoked to update the document with the data provided in the request body.

Since PyMongo will return the document before it was updated, theReturnDocument.AFTER option will instruct PyMongo to return the document after it has been updated.

"""

@router.patch('/{noteId}', response_model=schemas.NoteResponse)
def update_note(noteId: str, payload: schemas.UpdateNoteSchema):
    if not ObjectId.is_valid(noteId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {noteId}")
    updated_note = Note.find_one_and_update(
        {'_id': ObjectId(noteId)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')
    return {"status": "success", "note": noteEntity(updated_note)}


"""
This path operation function will be called to retrieve a single document from the database when a GET request hits the /api/notes/{noteId} endpoint.

The Id of the document to be lookup for will be obtained from the URL parameter and the ObjectId.is_valid() method will be called to check if the Id is a valid MongoDB ObjectId.

After that, the Note.find_one() method will be evoked to query the database to find the document that matches the provided ObjectId.

Once the document has been retrieved from the database, the noteEntity() method will be called to parse it into a Python dictionary.

"""

@router.get('/{noteId}', response_model=schemas.NoteResponse)
def get_note(noteId: str):
    if not ObjectId.is_valid(noteId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {noteId}")

    note = Note.find_one({'_id': ObjectId(noteId)})
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No note with this id: {noteId} found")
    return {"status": "success", "note": noteEntity(note)}

"""
Now that we’ve implemented the Create, Update, and Read operations, let’s create a route handler to delete a document in the database. This path operation function will be evoked to remove a document in the collection when a /api/notes/{noteId} DELETE request is made to the API.

The Id of the document to be deleted will be extracted from the URL parameter and the ObjectId.is_valid() method will be called to check if it’s a valid ObjectId before the Note.find_one_and_delete() method will be called to remove that document from the database.

"""

@router.delete('/{noteId}')
def delete_note(noteId: str):
    if not ObjectId.is_valid(noteId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {noteId}")
    note = Note.find_one_and_delete({'_id': ObjectId(noteId)})
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {noteId} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

