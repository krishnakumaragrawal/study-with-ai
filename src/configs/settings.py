import os
from dotenv import load_dotenv
from .logger import setup_logger

logger = setup_logger(__name__)

# Load the env variables
load_dotenv()

class Settings:
    """
    Class to load the environment variables from .env.
    """
    def __init__(self):

        try:
            self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
            self.model_name = os.getenv("MODEL_NAME")
            self.TEMP = os.getenv("TEMPERATURE")
            self.MAX_RETRIES = os.getenv("MAX_RETRIES")
        except Exception as e:
            logger.error(f"Error loading variables from .env: {e}")
            raise ValueError("Error laoding variables from the .env.")

        logger.info("Settings intialised successfully.")


# settings = Settings()
