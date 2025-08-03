import os

def setup_environment():
    """Set up the environment variables."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
