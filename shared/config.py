import os

# Configuration constants
GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"

def setup_environment():
    """Set up the environment variables."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
