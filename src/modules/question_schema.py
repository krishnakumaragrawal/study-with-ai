from pydantic import BaseModel, Field, field_validator
from typing import List


class MCQQuestion(BaseModel):
    """
    A pydantic model to represent a Multiple Choice Questions.
    """
    question: str = Field(description="The question text (string only)")
    options: List[str] = Field(description="list of options (usually 4 choices)")
    correct_answer: str = Field(description="The correct answer (must be one of the options)")

    @field_validator("question", mode="before")
    def clean_questions(cls, v):
        """
        Ensure 'question' is always stored a string.
        If provided as a dict, extract 'description'.
        """
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)
    

    @field_validator("correct_answer")
    def check_correct_answer_in_options(cls, v, values):
        """
        Ensure the correct answer is one of the options.
        """
        options = values.data.get("options", {})
        if v not in options:
            raise ValueError(f"Correct answer '{v}' must be one of {options}")
        return v


class FillBlankQuestion(BaseModel):
    """
    A pydantic model to represent a Fill-in-the-Blanks Question.
    """
    question: str = Field(description="The question text with '__' for the blank.")
    answer: str = Field(description="The correct word or phrase for the blank.")

    @field_validator("question", mode="before")
    def clean_questions(cls, v):
        """
        Ensure 'question' is always stored as a string.
        If provided as a dict, extract 'description'.
        """
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)
