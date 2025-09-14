from langchain.chat_models import init_chat_model
from src.configs.settings import Settings



class LLMConfig:
    """
    A class to interact with the LLM.
    """
    def __init__(self):

        settings = Settings()
        self.api_key = settings.GROQ_API_KEY
        self.model_name = settings.model_name
        self.temp = settings.TEMP


    def get_llm(self):
        """
        A function to chat with the LLM models.
        """
        llm = init_chat_model(model=self.model_name, model_provider="groq", temperature=self.temp)
        return llm
