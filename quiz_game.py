import json
from pathlib import Path
from default_quizzes import get_default_quizzes
from input_utils import input_int_in_range, input_non_empty
from quiz import Quiz


class QuizGame:
    def __init__(self, state_file: str = "state.json") -> None:
        self.state_path = Path(state_file)
        self.backup_path = Path(f"{state_file}.bak")
        self.quizzes: list[Quiz] = []
        self.score: int = 0
        self.load_state()

    def _parse_payload(self, data: object) -> tuple[list[Quiz], int]:
        if not isinstance(data, dict):
            raise ValueError("상태 데이터 형식이 올바르지 않습니다.")

        raw_quizzes = data.get("quizzes", [])
        if not isinstance(raw_quizzes, list) or not raw_quizzes:
            raise ValueError("퀴즈 목록이 비어 있거나 형식이 잘못되었습니다.")

        loaded_quizzes: list[Quiz] = []
        for item in raw_quizzes:
            if not isinstance(item, dict):
                raise ValueError("퀴즈 항목 형식이 올바르지 않습니다.")
            question = item["question"]
            choices = item["choices"]
            answer = item["answer"]
            if not isinstance(question, str) or not question.strip():
                raise ValueError("문제 내용이 올바르지 않습니다.")
            if (
                not isinstance(choices, list)
                or len(choices) != 4
                or not all(isinstance(c, str) and c.strip() for c in choices)
            ):
                raise ValueError("보기 목록 형식이 올바르지 않습니다.")
            if isinstance(answer, bool) or not isinstance(answer, int) or not (1 <= answer <= 4):
                raise ValueError("정답 번호가 올바르지 않습니다.")

            loaded_quizzes.append(
                Quiz(
                    question=question,
                    choices=choices,
                    answer=answer,
                )
            )

        raw_score = data.get("score", 0)
        if isinstance(raw_score, bool) or not isinstance(raw_score, int):
            score = int(raw_score)
        else:
            score = raw_score

        return loaded_quizzes, score

    def restore_from_backup(self) -> bool:
        """백업 파일(state.json.bak)에서 퀴즈와 점수를 복구합니다."""
        if not self.backup_path.exists():
            return False

        try:
            data = json.loads(self.backup_path.read_text(encoding="utf-8"))
            restored_quizzes, restored_score = self._parse_payload(data)
            self.quizzes = restored_quizzes
            self.score = restored_score
            self.state_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return True
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            return False

    def load_state(self) -> None:
        if not self.state_path.exists():
            if self.restore_from_backup():
                print("state.json이 없어 백업 파일(state.json.bak)에서 복구했습니다.")
                return
            self.quizzes = get_default_quizzes()
            self.score = 0
            self.save_state()
            return

        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            self.quizzes, self.score = self._parse_payload(data)
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            if self.restore_from_backup():
                print("손상된 state.json 대신 백업 파일(state.json.bak)에서 복구했습니다.")
            else:
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
        serialized = json.dumps(payload, ensure_ascii=False, indent=2)

        if self.state_path.exists():
            try:
                self.backup_path.write_text(
                    self.state_path.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            except OSError:
                pass

        self.state_path.write_text(serialized, encoding="utf-8")

        try:
            self.backup_path.write_text(serialized, encoding="utf-8")
        except OSError:
            pass

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