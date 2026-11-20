class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self) -> None:
        print(f"\n{self.question}")
        for idx, choice in enumerate(self.choices, start=1):
            print(f"  {idx}. {choice}")

    def check_answer(self, user_choice: int) -> bool:
        return user_choice == self.answer
