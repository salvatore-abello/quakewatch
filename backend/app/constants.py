LOGGING_FMT = "%(asctime)s | %(levelname)8s | %(message)s"
LOGGER_NAME = "main"
DEFAULT_JWT_SECRET_KEY = "keytest"
EARTHQUAKE_API_ENDPOINT = "http://webservices.ingv.it/fdsnws/event/1/query"
LIMITS = {
    "basic": "10000/month",
    "standard": "500000/month",
    "professional": "1000000/month"
}

OPENAPI_TAGS = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "keys",
        "description": "Manage keys.",
    },
    {
        "name": "auth",
        "description": "Operations with authentication. **Login**, **register** **logout** are here.",
    },
    {
        "name": "query",
        "description": "Operations with querying. **Earthquake** queries are here.",
        "externalDocs": {
            "description": "Add invgov API docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "files",
        "description": "Download of free/paid plan files",
    },
]