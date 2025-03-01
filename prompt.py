def prompt_evaluation(question: str, expected_answer: str, user_answer: str) -> str:
    """Generate AI evaluation prompt for user questions with a forced boolean output."""
    prompt = (
        "You are a digital teaching assistant. Your only task is to determine whether the user's answer is correct.\n"
        "You must return 'true' (exactly this word) if the user's answer matches the expected answer.\n"
        "Otherwise, return 'false' (exactly this word) and provide a short explanation of why it is incorrect.\n"
        "Check for:\n"
        "- Presence of all required components (e.g., variable initialization, all necessary conditionals, expected output).\n"
        "- Structural correctness (e.g., ensuring all branches of conditionals exist, syntax is valid).\n"
        "- Exactness of output formatting and text.\n"
        "Do not generate new questions. Do not provide alternative questions or further discussion.\n\n"
    )

    prompt += f"Question: {question}\n"
    prompt += f"Expected Answer: {expected_answer}\n"
    prompt += f"User's Answer: {user_answer}\n\n"
    # print("## eveluation ##")
    return prompt


def prompt_hint(question: str, expected_answer: str, user_answer: str, user_previous_answers: str, attempt: int) -> str:
    """Generate AI hint prompt for user questions"""
    prompt = (
        "You are a digital teaching assistant.\n"
        "Your task is to guide the user by providing hints without revealing direct answers.\n"
        "The user's current answer and previous answer can be used to determine if they are getting closer to the correct answer."
        "Provide a simple yet informative hint.\n"
        "Do not reveal the direct answer.\n"
        "Encourage logical reasoning.\n"
        "Do not generate any additional questions or answers.\n\n"
    )
    if attempt >= 5:
        prompt += "Provide a slightly more specific hint to help them progress without directly giving the solution.\n\n"

    print(attempt)
    prompt += f"Question: {question}\n"
    prompt += f"Expected Answer: {expected_answer}\n"
    prompt += f"User's Answer: {user_answer}\n"
    prompt += f"User's previous Answer: {user_previous_answers}\n\n"
    # print("## hint ##")
    return prompt