import json

from quiz import Quiz

STATE_FILE = "state.json"


def ask_number(prompt, min_value, max_value):
    """올바른 숫자가 들어올 때까지 반복해서 입력받는다."""
    while True:
        choice = input(prompt).strip()
        if choice == "":
            print("입력이 비어 있습니다. 다시 입력해주세요.")
        elif not choice.isdigit():
            print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
        elif int(choice) < min_value or int(choice) > max_value:
            print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
        else:
            return int(choice)


def ask_text(prompt):
    """빈 값이 아닌 문자열이 들어올 때까지 반복해서 입력받는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("입력이 비어 있습니다. 다시 입력해주세요.")
            continue
        return text


class QuizGame:
    """퀴즈 게임 전체를 관리한다."""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0
        self.load()

    # ------------------------------------------------------------------
    # 파일 입출력
    # ------------------------------------------------------------------

    def load(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
            self.best_score = data.get("best_score", 0)
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)
        except FileNotFoundError:
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = self.default_quizzes()
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = 0
            self.best_correct = 0
            self.best_total = 0
        else:
            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)"
            )

    def save(self):
        """퀴즈와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️ 데이터를 저장하지 못했습니다.")

    @staticmethod
    def default_quizzes():
        """파일이 없을 때 사용할 기본 퀴즈 목록을 만든다."""
        return [
            Quiz(
                "스택(Stack)의 데이터 처리 방식은?",
                ["FIFO", "LIFO", "우선순위", "무작위"],
                2,
            ),
            Quiz(
                "배열에서 인덱스로 원소에 접근하는 시간복잡도는?",
                ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                1,
            ),
            Quiz(
                "HTTP 상태 코드 404의 의미는?",
                ["서버 내부 오류", "권한 없음", "찾을 수 없음", "요청 성공"],
                3,
            ),
            Quiz(
                "10진수 10을 2진수로 나타내면?",
                ["1000", "1010", "1100", "1110"],
                2,
            ),
            Quiz(
                "같은 메모리 공간을 공유하는 것은?",
                ["프로세스", "스레드", "둘 다 공유함", "둘 다 공유 안 함"],
                2,
            ),
            Quiz(
                "SQL에서 데이터를 조회하는 명령어는?",
                ["SELECT", "INSERT", "UPDATE", "DELETE"],
                1,
            ),
            Quiz(
                "변경사항을 스테이징 영역에 올리는 Git 명령어는?",
                ["git init", "git add", "git commit", "git push"],
                2,
            ),
        ]

    # ------------------------------------------------------------------
    # 메뉴
    # ------------------------------------------------------------------

    def show_menu(self):
        """메뉴를 화면에 출력한다."""
        print(
            """
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================"""
        )

    def run(self):
        """메뉴를 반복해서 보여주며 게임을 진행한다."""
        while True:
            self.show_menu()
            choice = ask_number("선택: ", 1, 5)
            if choice == 5:
                self.save()
                print("게임을 종료합니다.")
                break
            elif choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()

    # ------------------------------------------------------------------
    # 각 메뉴 기능
    # ------------------------------------------------------------------

    def play(self):
        """퀴즈를 출제하고 결과와 최고 점수를 갱신한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        correct_count = 0
        for index, quiz in enumerate(self.quizzes, 1):
            print("\n" + "-" * 40)
            quiz.display(index)
            user_answer = ask_number("\n정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        self.show_result(correct_count, total)
        self.save()

    def show_result(self, correct_count, total):
        """결과를 출력하고 최고 점수를 갱신한다."""
        score = round(correct_count / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total
        print("=" * 40)

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = ask_text("문제를 입력하세요: ")
        choices = [ask_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = ask_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for index, quiz in enumerate(self.quizzes, 1):
            print(f"[{index}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_total == 0:
            print("\n아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀고 점수를 기록해보세요!")
            return

        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)"
        )
