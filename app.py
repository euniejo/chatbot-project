import streamlit as st
from query import query_ai, AIRequest
from questions import question_list

class StateMachine:
    def __init__(self):
        self.state = "CC_CHAT"
        self.user_id = 123
        self.chapter = 1
        self.question = 1
        self.question_list = question_list
        self.count = 0

    def greet(self):
        st.title("Welcome to the DTA App")
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ''

        user_input = st.text_input(
            "Hello! Would you like to start studying? \n (Type 'yes' to start, 'bye' to return to CC_CHAT state, 'end' to terminate)",
            key="greet_input"
        ).strip().lower()

        if user_input:
            st.session_state.user_input = user_input

        if st.session_state.user_input == "yes":
            self.start()
        elif st.session_state.user_input == "bye":
            self.state = "CC_CHAT"
            st.warning("Returning to CC_CHAT state")
        elif st.session_state.user_input == "end":
            self.state = "END"
            st.stop()
        elif st.session_state.user_input:
            st.error("Invalid input. Please type 'yes', 'bye', or 'end'.")

    def start(self):
        if self.state == "CC_CHAT":
            self.state = "DTA"
            st.info("Start studying!")
            self.run_lesson()
        else:
            st.warning("Cannot start in the current state!")

    def provide_hint(self, question, correct_answer, user_answer, user_previous_answers):
        """Generate a hint using AI when the answer is incorrect."""
        request = AIRequest(
            question=question,
            expected_answer=correct_answer,
            user_answer=user_answer,
            use_evaluation=False,
            user_previous_answers=user_previous_answers,
            attempt=self.count
        )
        hint = query_ai(request)
        if self.count >= 5:
            return f"*Hint*: {hint}"
        else:
            return f"Hint: {hint}"

    def run_lesson(self):
        if 'chapter' not in st.session_state:
            st.session_state.chapter = 1
        if 'question' not in st.session_state:
            st.session_state.question = 1
        if 'count' not in st.session_state:
            st.session_state.count = 0
        if 'hint' not in st.session_state:
            st.session_state.hint = ""
        if 'user_answer' not in st.session_state:
            st.session_state.user_answer = ""

        chapter = st.session_state.chapter
        question = st.session_state.question

        if chapter > len(self.question_list):
            st.success("Congratulations! You have completed all the questions.")
            self.state = "CC_CHAT"
            return

        question_text, correct_answer = self.question_list[chapter][question - 1]
        st.write(f"**Chapter {chapter}, Question {question}**")
        st.write(f"Question: {question_text}")

        with st.form(key="answer_form"):
            user_answer = st.text_area("Enter your answer:", placeholder=f"Enter your answer for Chapter {chapter}", value=st.session_state.user_answer, height=None).strip()
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if user_answer.lower() == "bye":
                    self.state = "CC_CHAT"
                    st.session_state.chapter = 1
                    st.session_state.question = 1
                    st.session_state.show_greeting = True
                    st.info("State changed: Returning to CC_CHAT state")
                    return
                elif user_answer.lower() == "end":
                    self.state = "END"
                    st.session_state.chapter = 1
                    st.session_state.question = 1
                    st.info("State changed: END. Exiting the program.")
                    st.stop()

                if self.check_answer(question_text, correct_answer, user_answer):
                    st.session_state.count = 0
                    st.session_state.question += 1
                    st.session_state.hint = "Correct"

                    # Move to next chapter if all questions are completed
                    if st.session_state.question > len(self.question_list[chapter]):
                        st.session_state.chapter += 1
                        st.session_state.question = 1
                    
                    # Force UI refresh to display the next question
                    st.success("Correct answer! Proceeding to the next question.")
           
                    st.rerun()   
                else:
                    st.session_state.count += 1
                    st.session_state.hint = self.provide_hint(question_text, correct_answer, user_answer, "")

        if st.session_state.hint:
            if "Correct" in st.session_state.hint:
                st.success("Previous step completed successfully! Proceed to the next step.") 
            else:
                st.error("Incorrect. Please try again.")
                st.error(st.session_state.hint)

    def check_answer(self, question, correct_answer, user_answer):
        """Validate the user's answer using AI."""
        request = AIRequest(question=question, expected_answer=correct_answer, user_answer=user_answer, use_evaluation=True)
        response = query_ai(request)
        return "true" in response.lower()

if __name__ == "__main__":
    sm = StateMachine()
    sm.greet()