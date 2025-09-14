from src.modules.question_generator import QuestionGenerator
from src.configs.logger import setup_logger
import streamlit as st
import pandas as pd

logger = setup_logger(__name__)


class QuizManager:
    """
    
    """
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []

    
    def generate_questions(self, generator: QuestionGenerator, question_type: str, topic: str, difficulty: str, num_of_questions: int):
        """
        
        """
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            for _ in range(num_of_questions):
                if question_type == "MCQ":
                    logger.info(f"Generating {num_of_questions} MCQ Questions.")
                    question = generator.generate_mcq(topic, difficulty)

                    self.questions.append({
                        "type": "MCQ", 
                        'question': question.question, 
                        'options': question.options, 
                        'correct_answer': question.correct_answer
                    })

                elif question_type == "Fill in the Blanks":
                    logger.info(f"Generating {num_of_questions} Fill_in_the_Blank Questions.")
                    question = generator.generate_fill_blank(topic, difficulty)

                    self.questions.append({
                        'type': 'Fill in the Blanks', 
                        'question': question.question, 
                        'correct_answer': question.answer
                    })

                else:
                    logger.error("Wrong question_type selected.")
                    return False
        
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            return False
        
        return True
    

    def attempt_quiz(self):
        
        for i,q in enumerate(self.questions):
            st.markdown(f"**Question {i+1} : {q['question']}**")

            if q['type'] == "MCQ":
                user_answer = st.radio(
                    f"Select answer for Question {i+1}",
                    q['options'], 
                    key = f"mcq_{i}"
                )

                self.user_answers.append(user_answer)

            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {i+1}", 
                    key = f"fill_in_the_blank_{i}"
                )
                self.user_answers.append(user_answer)


    def evaluate_quiz(self):
        self.results = []

        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):

            result_dict = {
                'question_number': i+1, 
                'question': q['question'], 
                'question_type': q['type'], 
                'user_answer': user_ans, 
                'correct_answer': q['correct_answer'], 
                'is_correct': False
            }

            if q['type'] == "MCQ":
                result_dict['options'] = q['options']
                result_dict['is_correct'] = user_ans == q['correct_answer']

            else:
                result_dict['options'] = []
                result_dict['is_correct'] = user_ans.strip().lower() == q['correct_answer'].strip().lower()

            
            self.results.append(result_dict)

    
    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        
        return pd.DataFrame(self.results)
        
    