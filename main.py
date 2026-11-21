from input_utils import input_int_in_range
from quiz_game import QuizGame


def print_menu() -> None:
    print("\n==============================")
    print("       콘솔 퀴즈 게임")
    print("==============================")
    print("1. 퀴즈 풀기")
    print("2. 새 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("4. 현재 점수 보기")
    print("5. 종료")
    print("==============================")


def main() -> None:
    game = QuizGame()

    while True:
        print_menu()
        choice = input_int_in_range("메뉴 번호를 선택하세요 (1~5): ", 1, 5)

        if choice == 1:
            game.play_quiz()
        elif choice == 2:
            game.add_quiz()
        elif choice == 3:
            game.list_quizzes()
        elif choice == 4:
            game.show_score()
        elif choice == 5:
            game.save_state()
            print("상태를 저장하고 게임을 종료합니다. 수고하셨습니다!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n입력이 중단되어 프로그램을 종료합니다.")