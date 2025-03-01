import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from prompt import prompt_hint, prompt_evaluation  # Import prompt module
from pydantic import BaseModel

class AIRequest(BaseModel):
    question: str
    expected_answer: str
    user_answer: str = None  # Add user_answers for evaluation
    use_evaluation: bool = True  # T: evaluation prompt, F: hint prompt
    user_previous_answers: str = "None"  # Add user_previous_answers for hint
    attempt: int = 1  # Add attempt number for hint

# Load environment variables
load_dotenv()

groq_api_key = os.environ.get("GROQ_API_KEY", "your_dummy_key")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768", max_tokens=1024, temperature=0.2)

def query_ai(request: AIRequest) -> str:
    """Input a single question into the AI model and return the response."""
    if request.use_evaluation:
        prompt = prompt_evaluation(request.question, request.expected_answer, request.user_answer)
    else:
        prompt = prompt_hint(request.question, request.expected_answer, request.user_answer, request.user_previous_answers, request.attempt)
    
    try:
        response = llm.invoke(prompt)
        response_text = getattr(response, "content", "").strip().lower()

        # print(f"#######response_text: {response_text}")

        if not response_text:
            raise ValueError("No response received from AI.")
        
        return response_text
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    question = input("Enter your question: ")
    expected_answer = input("Enter the expected answer: ")
    user_answer = input("Enter the user's answer: ")
    use_evaluation = input("Use evaluation prompt? (yes/no): ").strip().lower() == 'yes'
    request = AIRequest(question=question, expected_answer=expected_answer, user_answer=user_answer, use_evaluation=use_evaluation)
    answer = query_ai(request)
    print(f"AI Response: {answer}")