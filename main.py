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
        if choice == 5:
            print("게임을 종료합니다.")
            break
        elif choice == 3:
            for i, q in enumerate(default_quizzes(), 1):
                q.display(i)
        else:
            print("준비 중입니다")


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
