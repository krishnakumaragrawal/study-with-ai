from src.configs.logger import setup_logger
from src.configs.llm_config import LLMConfig
from src.utils.load_prompt import PromptTemplate
from src.modules.question_schema import MCQQuestion, FillBlankQuestion
from langchain.output_parsers import PydanticOutputParser

logger = setup_logger(__name__)

MCQ_PROMPT_PATH = "./src/prompts/mcq_prompt.txt"
FILL_BLANK_PROMPT_PATH = "./src/prompts/fill_blank_prompt.txt"

class QuestionGenerator:
    """
    A class to generate different types of questions (MCQ, Fill-in-the-Blanks) using a LLM.
    """
    def __init__(self):
        self.llm = LLMConfig().get_llm()

    def parsed_response_from_llm(self, prompt: str, parser, topic: str, difficulty: str):
        """
        Sends a formatted prompt to the LLM and parse the response into a 
        structured Pydantic object.

        Args:
            prompt (str): The base prompt template with placeholders.
            parser (PydanticOutputParser): Parser to enforce the structured output.
            **kwargs: Variables to format the prompt (e.g. Topic & Difficulty Level).

        Returns:
            Any: Parsed response as the target Pydantic object.
        """
        try:
            formatted_prompt = prompt.format(topic=topic, difficulty=difficulty)
            logger.info(f"Sending formatted prompt to the LLM: {formatted_prompt[:20]}")
            raw_response = self.llm.invoke(formatted_prompt)
            return parser.parse(raw_response.content)
        
        except Exception as e:
            logger.error(f"Error parsing the response from the LLM: {e}", exc_info=True)
            return None
        

    def generate_mcq(self, topic: str, difficulty: str = "medium") -> MCQQuestion | None:
        """
        Generates a Multiple Choice Question for a given topic and difficulty level.

        Args:
            topic (str): Subject/Topic for the MCQ.
            difficulty (str): Difficulty level (default: "medium").

        Returns:
            MCQQuestion | None: Parsed MCQQuestion object if successful, else None.
        """
        try:
            mcq_prompt_template = PromptTemplate.get_prompt_template(filename=MCQ_PROMPT_PATH)

            if not mcq_prompt_template:
                logger.error("MCQ Prompt template could be loaded.")
                return None

            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self.parsed_response_from_llm(mcq_prompt_template, parser, topic, difficulty)
            
            if len(question.options) != 4 or question.correct_answer not in question.options:
                logger.error("Invalid MCQ Question generated.")
                raise ValueError("Invalid MCQ generated.")
            
            logger.info("MCQ generated successfully.")
            return question

        except Exception as e:
            logger.error(f"Failed to generate MCQ: {e}")
            return None
        

    def generate_fill_blank(self, topic: str, difficulty: str = "medium") -> FillBlankQuestion | None:
        """
        Generates a Fill_in_the_Blanks Question for a given topic and difficulty level.

        Args:
            topic (str): Subject/Topic for generating the question.
            difficulty (str): Difficulty level (default: "medium").

        Returns:
            FillBlankQuestion | None: Parsed FillBlankQuestion object if successful otherwise None.
        """
        try:
            fill_blank_prompt_template = PromptTemplate.get_prompt_template(FILL_BLANK_PROMPT_PATH)
            
            if not fill_blank_prompt_template:
                logger.error("Fill_in_the_Blank Prompt template could be loaded.")
                return None

            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self.parsed_response_from_llm(fill_blank_prompt_template, parser, topic, difficulty)
            
            if "___" not in question.question:
                logger.error("Invalid Fill_in_the_Blank generated.")
                raise ValueError("Invalid Fill_in_the_Blank generated.")

            logger.info("Fill_in_the_Blank generated successfully.")
            return question 

        except Exception as e:
            logger.error(f"Failed to generate Fill_in_the_Blank Question: {e}")
            return None