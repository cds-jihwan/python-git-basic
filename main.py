from quiz import Quiz
import json
import random

STATE_FILE = "state.json"


def show_menu():
    """메뉴를 화면에 출력한다."""
    print("""
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 퀴즈 삭제
6. 종료
========================================""")


def ask_number(prompt, min_value, max_value):
    """올바른 숫자가 들어올 때까지 반복해서 입력받는다."""
    while True:
        choice = input(prompt).strip()
        if choice == "":
            print("입력이 비어 있습니다. 다시 입력해주세요.")
            continue
        elif not choice.isdigit():
            print("숫자를 입력해주세요.")
            continue
        elif int(choice) < min_value or int(choice) > max_value:
            print(f"{min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue
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


def add_quiz(quizzes):
    """새 퀴즈를 입력받아 목록에 추가한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.\n")

    question = ask_text("문제를 입력하세요: ")
    choices = []
    for number in range(1, 5):
        choices.append(ask_text(f"선택지 {number}: "))
    answer = ask_number("정답 번호 (1-4): ", 1, 4)
    hint = input("힌트 (없으면 Enter): ").strip()

    quizzes.append(Quiz(question, choices, answer, hint))
    print("\n✅ 퀴즈가 추가되었습니다!")


def list_quizzes(quizzes):
    """등록된 퀴즈 목록을 번호와 함께 출력한다."""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)\n")
    print("-" * 40)
    for index, quiz in enumerate(quizzes, 1):
        print(f"[{index}] {quiz.question}")
    print("-" * 40)


def delete_quiz(quizzes):
    """번호를 입력받아 해당 퀴즈를 삭제한다."""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return False

    list_quizzes(quizzes)
    number = ask_number(f"\n삭제할 퀴즈 번호 (0: 취소, 1-{len(quizzes)}): ", 0, len(quizzes))
    if number == 0:
        print("삭제를 취소했습니다.")
        return False

    removed = quizzes.pop(number - 1)
    print(f"\n🗑️ 삭제되었습니다: {removed.question}")
    return True


def play_quiz(quizzes):
    """퀴즈를 출제하고 맞힌 개수를 반환한다."""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요.")
        return None, 0, 0

    print(f"\n현재 {len(quizzes)}문제가 등록되어 있습니다.")
    count = ask_number(f"몇 문제를 풀까요? (1-{len(quizzes)}): ", 1, len(quizzes))

    selected = random.sample(quizzes, count)
    print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")

    correct_count = 0
    hint_count = 0
    for index, quiz in enumerate(selected, 1):
        print("\n" + "-" * 40)
        quiz.display(index)
        if quiz.hint:
            print("\n(0을 입력하면 힌트를 볼 수 있습니다. 점수는 절반만 인정됩니다)")

        used_hint = False
        while True:
            user_answer = ask_number("\n정답 입력: ", 0, len(quiz.choices))
            if user_answer != 0:
                break
            if not quiz.hint:
                print("💡 이 문제에는 힌트가 없습니다.")
            elif used_hint:
                print("💡 이미 힌트를 확인했습니다.")
            else:
                used_hint = True
                hint_count += 1
                print(f"💡 힌트: {quiz.hint}")

        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            correct_count += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

    return correct_count, count, hint_count


def show_result(correct_count, total, hint_count, best_score):
    """퀴즈 결과를 출력하고 갱신된 최고 점수를 반환한다."""
    score = max(0, round((correct_count - hint_count * 0.5) / total * 100))
    print("\n" + "=" * 40)
    print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
    if hint_count:
        print(f"💡 힌트 {hint_count}회 사용으로 점수가 차감되었습니다.")
    if score > best_score:
        print("🎉 새로운 최고 점수입니다!")
        best_score = score
    print("=" * 40)
    return best_score


def show_score(best_score):
    """최고 점수를 출력한다."""
    if best_score == 0:
        print("\n아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀고 점수를 기록해보세요!")
        return
    print(f"\n🏆 최고 점수: {best_score}점")


def main():
    quizzes, best_score = load_state()
    while True:
        show_menu()
        choice = ask_number("선택: ", 1, 6)
        if choice == 6:
            save_state(quizzes, best_score)
            print("게임을 종료합니다.")
            break
        elif choice == 1:
            correct_count, total, hint_count = play_quiz(quizzes)
            if correct_count is not None:
                best_score = show_result(correct_count, total, hint_count, best_score)
                save_state(quizzes, best_score)
        elif choice == 2:
            add_quiz(quizzes)
            save_state(quizzes, best_score)
        elif choice == 3:
            list_quizzes(quizzes)
        elif choice == 4:
            show_score(best_score)
        elif choice == 5:
            if delete_quiz(quizzes):
                save_state(quizzes, best_score)


def save_state(quizzes, best_score):
    """퀴즈 목록과 최고 점수를 state.json에 저장한다."""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score,
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        print("⚠️ 데이터를 저장하지 못했습니다.")


def load_state():
    """state.json을 읽어 (퀴즈 목록, 최고 점수)를 반환한다."""
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
        best_score = data.get("best_score", 0)
    except FileNotFoundError:
        print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        return default_quizzes(), 0
    except (json.JSONDecodeError, KeyError, TypeError, OSError):
        print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
        return default_quizzes(), 0

    print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)")
    return quizzes, best_score


def default_quizzes():
    return [
        Quiz(
            "스택(Stack)의 데이터 처리 방식은?",
            ["FIFO", "LIFO", "우선순위", "무작위"],
            2,
            "나중에 넣은 것이 먼저 나옵니다",
        ),
        Quiz(
            "배열에서 인덱스로 원소에 접근하는 시간복잡도는?",
            ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            1,
            "위치를 바로 계산할 수 있습니다",
        ),
        Quiz(
            "HTTP 상태 코드 404의 의미는?",
            ["서버 내부 오류", "권한 없음", "찾을 수 없음", "요청 성공"],
            3,
            "주소를 잘못 입력했을 때 자주 봅니다",
        ),
        Quiz(
            "10진수 10을 2진수로 나타내면?",
            ["1000", "1010", "1100", "1110"],
            2,
            "8 + 2 로 나눠서 생각해 보세요",
        ),
        Quiz(
            "같은 메모리 공간을 공유하는 것은?",
            ["프로세스", "스레드", "둘 다 공유함", "둘 다 공유 안 함"],
            2,
            "하나의 프로세스 안에서 여러 개가 동작합니다",
        ),
        Quiz(
            "SQL에서 데이터를 조회하는 명령어는?",
            ["SELECT", "INSERT", "UPDATE", "DELETE"],
            1,
            "영어로 '선택하다' 라는 뜻입니다",
        ),
        Quiz(
            "변경사항을 스테이징 영역에 올리는 Git 명령어는?",
            ["git init", "git add", "git commit", "git push"],
            2,
            "commit 바로 직전에 하는 작업입니다",
        ),
    ]


# 프로그램 시작

try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\n\n프로그램을 종료합니다.")
