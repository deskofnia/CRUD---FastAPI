from app import note
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(note.router, tags=['Notes'], prefix='/api/notes')


# @app.get("/api/healthchecker")
# def root():
#     return {"message": "Welcome to FastAPI with Pymongo"}



# @router.get('/')
# def get_notes():
#     return "return a list of note items"


# @router.post('/', status_code=status.HTTP_201_CREATED)
# def create_note():
#     return "create note item"


# @router.patch('/{noteId}')
# def update_note(noteId: str):
#     return f"update note item with id {noteId}"


# @router.get('/{noteId}')
# def get_note(noteId: str):
#     return f"get note item with id {noteId}"


# @router.delete('/{noteId}')
# def delete_note(noteId: str):
#     return f"delete note item with id {noteId}"

"""
First, we imported the FastAPI modules at the top level of the file.
Then, we created instances of the FastAPI and APIRouter classes.
After that, we created the CRUD path operation functions and added them to the router middleware pipeline.
Lastly, we evoked the include_router() method available on the app instance to register the router in the app.

With the above explanation, open your terminal and run this command to start the FastAPI HTTP server.

uvicorn app.main:app --host localhost --port 8000 --reload


We imported the CORSMiddleware class to help us configure the FastAPI application with CORS.
Then, we created a list of the allowed origins and added the CORS configurations to the FastAPI middleware stack.
Setting allow_credentials=True will tell the FastAPI app to accept credentials like Authorization headers, Cookies, etc from the cross-origin domain.

"""