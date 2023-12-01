from pymongo import mongo_client, ASCENDING
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('🚀 Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
Note = db.notes
Note.create_index([("title", ASCENDING)], unique=True)


"""
mongo_client – A tool for connecting to MongoDB
ASCENDING – Ascending sort order
settings – For accessing the environment variables

We evoked the .MongoClient() method with the database connection URL in the above code to create a connection pool to the MongoDB database. Calling the .MongoClient() method returns a client object with a bunch of methods that we can use to access and manage the MongoDB instance.

Next, we created the database with client["enter_database_name"] , added a collection with the name notes and created a unique index on the title field. The unique index will ensure that no two documents in the collection end up with the same title.

"""