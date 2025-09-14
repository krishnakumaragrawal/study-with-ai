import streamlit as st
from src.modules.question_generator import QuestionGenerator
from src.modules.backend import QuizManager

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get("rerun_trigger", False)

def main():
    st.set_page_config(page_title="Study with AI")
    st.title("Study with AI")

    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger' not in st.session_state:
        st.session_state.rerun_trigger = False
    

    st.sidebar.header("Quiz Settings")
    question_type = st.sidebar.selectbox(
        "Select Question type",
        ["MCQ", "Fill in the Blanks"], 
        index=0
    )

    topic = st.sidebar.text_input("Enter topic", placeholder="Algebra")

    difficulty = st.sidebar.selectbox(
        "Difficulty Level", 
        ["Easy", "Medium", "Hard"], 
        index=1
    )

    num_of_questions = st.sidebar.number_input(
        "Enter number of questions", 
        min_value=1, 
        max_value=10, 
        value=4
    )

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False

        generator = QuestionGenerator()
        success = st.session_state.quiz_manager.generate_questions(
            generator, question_type, topic, difficulty, num_of_questions
        )

        st.session_state.quiz_generated = success
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:

            correct_count = results_df['is_correct'].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions)*100
            st.write(f"Score: {score_percentage}")

            for _,result in results_df.iterrows():
                question_num = result['question_number']

                if result['is_correct']:
                    st.success(f"✅ Question {question_num} : {result['question']}")
                else:
                    st.error(f"❌ Question {question_num} : {result['question']}")
                    st.write(f"Your answer: {result['user_answer']}")
                    st.write(f"Correct answer: {result['correct_answer']}")

                st.markdown("------")



if __name__ == "__main__":
    main()