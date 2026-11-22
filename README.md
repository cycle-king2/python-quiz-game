cd ~/projects/python-quiz-game && cat << 'EOF' > README.md
# Python Console Quiz Game

모듈화 구조와 입력 검증, 상태 저장/복구(`state.json`) 기능을 적용한 콘솔 기반 퀴즈 게임입니다.

---

## 1. 프로젝트 개요 및 퀴즈 주제 선정 이유
- **주제 선정 이유:** 감자 테마를 주제로 4지선다 퀴즈 출제·등록·점수 관리와 JSON 파일 저장/복구 흐름을 직접 구현하고 검증하기 위해 선정했습니다.
- **주요 기능:**
  - 퀴즈 문제 출제 및 정답/오답 판정, 점수 집계
  - 새 퀴즈 등록 및 기본 퀴즈(`default_quizzes.py`) 연동
  - 사용자 입력 검증(`input_utils.py`) 및 진행/기록 상태 저장·복구(`state.json`)

---

## 2. 프로젝트 구조 및 모듈 역할
- `main.py`: 프로그램 진입점 및 메뉴 실행 흐름 제어
- `quiz.py`: 개별 퀴즈 데이터 및 문제/정답 처리 로직
- `quiz_game.py`: 게임 루프, 점수 관리, 상태 저장 및 불러오기 로직
- `default_quizzes.py`: 기본 제공 퀴즈 데이터 목록
- `input_utils.py`: 콘솔 사용자 입력 검증 유틸리티

---

## 3. 개발 환경 설정
WSL Ubuntu 환경과 Python, VS Code, Git 기반으로 개발 환경을 구성했습니다.

![개발환경 설정 스크린샷](docs/screenshots/개발환경%20설정%20스크린샷.png)

---

## 4. 실행 방법 및 실행 결과
터미널에서 프로젝트 루트(`python-quiz-game`)로 이동한 뒤 아래 명령어로 실행합니다.

`python3 main.py`

![프로그램 실행결과 스크린샷](docs/screenshots/프로그램%20실행결과%20스크린샷.png)

---

## 5. Git 브랜치 전략 및 커밋 이력
- `feat/play-polish` 기능 브랜치에서 작업한 뒤 `--no-ff` 옵션으로 병합했습니다.
- 원격 저장소(`cycle-king2/python-quiz-game`)와 동기화(`clone` / `pull` / `push`)를 진행했습니다.

![브랜치 병합과 커밋 이력](docs/screenshots/브랜치%20병합과%20커밋%20이력.png)

![git log 스크린샷 결과](docs/screenshots/git%20log%20스크린샷%20결과.png)

---

## 6. 회고 및 개선점
- 콘솔 입출력 흐름과 모듈 간 책임을 분리하면서 코드 가독성과 유지보수성을 높일 수 있었습니다.
- Git 브랜치 병합 및 원격 동기화 과정을 거치며 버전 관리 기본기를 점검했습니다.