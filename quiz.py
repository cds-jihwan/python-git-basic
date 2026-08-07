class Quiz:
    """퀴즈 한 문제를 표현한다."""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, index):
        """문제 번호와 선택지를 화면에 출력한다."""
        print(f"\n[문제 {index}]")
        print(self.question)
        print()
        for number, choice in enumerate(self.choices, 1):
            print(f"{number}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 반환한다."""
        return user_answer == self.answer
