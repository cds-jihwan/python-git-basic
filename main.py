"""나만의 퀴즈 게임 - 진입점

실행 방법: python3 main.py
"""

from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n프로그램을 종료합니다.")
        game.save()


if __name__ == "__main__":
    main()
