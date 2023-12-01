from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    class Config:
        env_file = './.env'


settings = Settings()


"""
Despite having the option to create the environment variables outside of Python and read them with the os.getenv() method, we’ll use Pydantic’s BaseSettings utility class to load the environment variables and provide type validation for the variables.

To load the environment variables into the app, we created a sub-class from the BaseSettings class and declared class attributes with type annotations on the sub-class.

The setting env_file on the Config class will tell Pydantic to load the environment variables from the provided path.

Now let’s write the code required to connect the app to the MongoDB instance. So, create a app/database.py file and add the code below.

"""