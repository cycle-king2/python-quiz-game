import json
from pathlib import Path
from default_quizzes import get_default_quizzes
from input_utils import input_int_in_range, input_non_empty
from quiz import Quiz


class QuizGame:
    def __init__(self, state_file: str = "state.json") -> None:
        self.state_path = Path(state_file)
        self.quizzes: list[Quiz] = []
        self.score: int = 0
        self.load_state()

    def load_state(self) -> None:
        if not self.state_path.exists():
            self.quizzes = get_default_quizzes()
            self.score = 0
            self.save_state()
            return

        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            raw_quizzes = data.get("quizzes", [])
            loaded_quizzes: list[Quiz] = []

            for item in raw_quizzes:
                loaded_quizzes.append(
                    Quiz(
                        question=item["question"],
                        choices=item["choices"],
                        answer=item["answer"],
                    )
                )

            if not loaded_quizzes:
                raise ValueError("퀴즈 목록이 비어 있습니다.")

            self.quizzes = loaded_quizzes
            self.score = int(data.get("score", 0))
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장된 상태 파일이 없거나 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.score = 0
            self.save_state()

    def save_state(self) -> None:
        payload = {
            "score": self.score,
            "quizzes": [
                {
                    "question": q.question,
                    "choices": q.choices,
                    "answer": q.answer,
                }
                for q in self.quizzes
            ],
        }
        self.state_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def list_quizzes(self) -> None:
        print("\n=== 현재 등록된 퀴즈 목록 ===")
        for idx, q in enumerate(self.quizzes, start=1):
            print(f"{idx}. {q.question} (정답: {q.answer}번)")

    def add_quiz(self) -> None:
        print("\n=== 새 퀴즈 추가 ===")
        question = input_non_empty("문제를 입력하세요: ")
        choices = [
            input_non_empty(f"보기 {i}을 입력하세요: ") for i in range(1, 5)
        ]
        answer = input_int_in_range("정답 번호를 입력하세요 (1~4): ", 1, 4)

        self.quizzes.append(Quiz(question=question, choices=choices, answer=answer))
        self.save_state()
        print("새 퀴즈가 추가되고 state.json에 저장되었습니다.")

    def play_quiz(self) -> None:
        print("\n=== 퀴즈 풀기 시작 ===")
        for idx, q in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {idx}/{len(self.quizzes)}]")
            q.display()
            user_choice = input_int_in_range("정답 번호 (1~4): ", 1, 4)
            if q.check_answer(user_choice):
                self.score += 10
                print(f"정답입니다! (+10점, 현재 점수: {self.score}점)")
            else:
                print(f"오답입니다. 정답은 {q.answer}번입니다. (현재 점수: {self.score}점)")
        self.save_state()

    def show_score(self) -> None:
        print(f"\n현재 누적 점수: {self.score}점 (등록된 퀴즈 수: {len(self.quizzes)}개)")