from query import query_ai, AIRequest
from questions import question_list  # 올바른 모듈 이름으로 수정

class StateMachine:
    def __init__(self):
        self.state = "CC_CHAT"  # Initial state cc chat operation
        self.user_id = 123  # Placeholder for user ID
        self.chapter = 1  # Save the current chapter in the DB with the user ID
        self.question = 1  # Save the current question in the DB with the user ID
        self.question_list = question_list  # Initialize questions
        self.count = 0

    def greet(self):
        while True:
            print("Hello! Would you like to start studying? (Type 'yes' to start, 'bye' to return to CC_CHAT state, 'end' to terminate)")
            user_input = input().strip().lower()
            if user_input == "yes":
                self.start()
            elif user_input == "bye":
                self.state = "CC_CHAT"
                print("[INFO] State changed: Returning to CC_CHAT state")
            elif user_input == "end":
                self.state = "END"
                print("[INFO] State changed: END. Exiting the program.")
                exit()
            else:
                print("[ERROR] Invalid input. Please type 'yes', 'bye', or 'end'.")

    def start(self):
        if self.state == "CC_CHAT":
            self.state = "DTA"
            print("[INFO] State changed: CC_CHAT → ## DTA ##")
            self.run_lesson()
        else:
            print("[WARNING] Cannot start in the current state!")

    def check_answer(self, question, correct_answer, user_answer):
        """ Function to evaluate subjective answers """
        request = AIRequest(question=question, expected_answer=correct_answer, user_answer=user_answer, use_evaluation=True)
        response = query_ai(request)
        return "true" in response.lower()

    def provide_hint(self, question, correct_answer, user_answer, user_previous_answers):
        """ Function to provide hints using AI """
        request = AIRequest(question=question, expected_answer=correct_answer, user_answer=user_answer, use_evaluation=False, user_previous_answers=user_previous_answers, attempt=self.count)
        hint = query_ai(request)
        if self.count >= 5:
            return f"*Hint*: {hint}"
        else:
            return f"Hint: {hint}"

    def run_lesson(self):
        while self.chapter <= len(self.question_list):
            while self.question <= len(self.question_list[self.chapter]):
                question_text, correct_answer = self.question_list[self.chapter][self.question - 1]
                print(f"Question: {question_text}")
                user_answer = input("Enter your answer: ").strip()
                user_previous_answers = user_answer
                if user_answer.lower() == "bye":
                    self.state = "CC_CHAT"
                    self.chapter = 1
                    print("[INFO] State changed: Returning to ## CC_CHAT ## state")
                    return
                elif user_answer.lower() == "end":
                    self.state = "END"
                    self.chapter = 1
                    print("[INFO] State changed: ## END ##. Exiting the program.")
                    exit()
                elif self.check_answer(question_text, correct_answer, user_answer):
                    print("[INFO] Correct answer!")
                    self.count = 0
                    self.question += 1
                else:
                    self.count += 1
                    print("[ERROR] Incorrect. Please try again.")
                    print(self.provide_hint(question_text, correct_answer, user_answer, user_previous_answers))

            self.chapter += 1
            self.question = 1
            if self.chapter <= len(self.question_list):
                print(f"Moving to chapter {self.chapter}.")

        print("Congratulations! You have completed all the questions.")
        self.state = "CC_CHAT"

    def stop(self):
        if self.state == "DTA":
            self.state = "CC_CHAT"
            print("[INFO] State changed: DTA → ## CC_CHAT ##")
        else:
            print("[WARNING] Cannot stop in the current state!")

if __name__ == "__main__":
    sm = StateMachine()
    sm.greet()