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

    def to_dict(self):
        """JSON에 저장할 수 있는 dict 형태로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """dict를 다시 Quiz 객체로 되돌린다."""
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", ""))
