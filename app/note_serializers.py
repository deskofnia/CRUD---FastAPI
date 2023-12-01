"""
Before getting into the API implementation, let’s create serializer functions that we’ll use to parse the data returned from MongoDB into Python dictionaries.

"""

def noteEntity(note) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "category": note["category"],
        "content": note["content"],
        "published": note["published"],
        "createdAt": note["createdAt"],
        "updatedAt": note["updatedAt"]
    }


def noteListEntity(notes) -> list:
    return [noteEntity(note) for note in notes]
