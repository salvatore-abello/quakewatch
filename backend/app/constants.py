import os

REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
HCAPTCHA_SECRET = os.environ.get("HCAPTCHA_SECRET", "secretsecret")

LOGGING_FMT = "%(asctime)s | %(levelname)8s | %(message)s"
LOGGER_NAME = "main"
DEFAULT_JWT_SECRET_KEY = "keytest"
EARTHQUAKE_API_ENDPOINT = "http://webservices.ingv.it/fdsnws/event/1/query"
HCAPTCHA_URL = "https://api.hcaptcha.com/siteverify"
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