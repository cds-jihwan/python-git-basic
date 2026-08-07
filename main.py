from quiz import Quiz

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
5. 종료
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


def main():
    while True:
        show_menu()
        choice = ask_number("선택: ", 1, 5)
        if choice == 1:
            print("준비 중입니다")
            break
        if choice == 2:
            print("준비 중입니다")
            break
        if choice == 3:
            print("준비 중입니다")
            break
        if choice == 4:
            print("준비 중입니다")
            break
        if choice == 5:
            print("게임을 종료합니다.")
            break

def default_quizzes():
    return [
        Quiz("스택(Stack)의 데이터 처리 방식은?",
             ["FIFO", "LIFO", "우선순위", "무작위"],
             2,
             "나중에 넣은 것이 먼저 나옵니다"),
        # TODO: 6개 더
    ]


# 프로그램 시작

try:
    main()
except (KeyboardInterrupt, EOFError):
    print("\n\n프로그램을 종료합니다.")