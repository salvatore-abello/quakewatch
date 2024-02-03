LOGGING_FMT = "%(asctime)s | %(levelname)8s | %(message)s"
LOGGER_NAME = "main"
DEFAULT_JWT_SECRET_KEY = "keytest"
EARTHQUAKE_API_ENDPOINT = "http://webservices.ingv.it/fdsnws/event/1/query"
LIMITS = {
    "basic": "10000/month",
    "standard": "500000/month",
    "professional": "1000000/month"
}
