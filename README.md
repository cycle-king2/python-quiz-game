cd ~/projects/python-quiz-game && cat << 'EOF' > README.md
# Python Console Quiz Game

모듈화 구조와 입력 검증, 상태 저장/복구(`state.json`) 기능을 적용한 콘솔 기반 퀴즈 게임입니다.

---

## 1. 프로젝트 개요 및 퀴즈 주제 선정 이유

- **주제 선정 이유:** 김다미 배우를 좋아해 팬들이 좋아할 주제로 4지선다 퀴즈 출제·등록·점수 관리와 JSON 파일 저장/복구 흐름을 직접 구현하고 검증하기 위해 선정했습니다.

- **주요 기능:**
  - 퀴즈 풀기 : 저장된 퀴즈를 순차 출제하고 '정답/오답' 판정 및 점수 집계, 최종 결과를 출력함
  - 퀴즈 추가 : 새 퀴즈를 등록하고 검증한 뒤 저장하며, 기본 퀴즈(`default_quizzes.py`)와 연동
  - 퀴즈 목록 : 저장된 전체 퀴즈 목록을 확인하며, 등록된 퀴즈가 없는 경우도 처리
  - 점수 확인 : 현재 최고 점수를 조회하고, 풀이 결과에 따라 최고 점수를 비교·갱신하여 저장합니다.
  - 입력 검증 및 상태 저장/복구: 사용자 입력 검증(`input_utils.py`)과 진행/기록 상태 저장·복구(`state.json`)를 지원하며, 잘못된 입력이나 입력 중단(`EOF`) 시 안내 및 안전 종료/재입력 흐름을 제공합니다.

---

## 2. 프로젝트 구조 및 모듈 역할

**코드파일 구조:**
- `main.py`: 프로그램 진입점 및 메뉴 실행 흐름 제어(잘못된 메뉴 입력 안내 및 `KeyboardInterrupt` 및 입력 스트림 종료/`EOFError` 시 안내 후 안전 종료 처리)
- `quiz.py`: 개별 퀴즈 데이터 모델 및 문제 출력/정답 검증 로직 캡슐화
- `quiz_game.py`: 게임 진행 루프, 점수 집계, `state.json` 상태 저장 및 불러오기/복구 로직
- `default_quizzes.py`: 기본 제공 퀴즈 데이터 목록(출연작·필모그래피 등 주제 문항 포함)
- `input_utils.py`: 콘솔 사용자 입력 검증 유틸리티(메뉴 번호 범위, 빈 문자열/공백 입력, 선택지 및 정답 번호 범위/형식 검증)

**입력 검증(`input_utils.py`)과 데이터 IO(`quiz_game.py`) 책임 경계:**
- **입력 검증(`input_utils.py`):** 콘솔에서 들어오는 메뉴 선택(1~4 등), 보기 입력, 정답 번호(1~4) 등의 형식과 범위를 사전에 검증해 잘못된 입력이 게임 로직이나 파일 저장 단계로 넘어가지 않도록 막습니다.
- **데이터 IO(`quiz_game.py`):** 검증을 통과한 퀴즈와 점수 상태를 `state.json`에 직렬화해 기록하고, 불러올 때 파일 누락이나 파싱 오류를 처리합니다.
- **상태 처리 흐름 요약:** `읽기(파일 로드) → 검증(구조·타입·필드 확인) → 복구(오류/누락 시 기본값 대체) → 쓰기(변경 상태 저장)` 순서로 동작합니다.

**객체지향(클래스) 선택 이유 및 함수 기반 대비 장점:**
- 퀴즈 항목(`Quiz`)과 전체 게임 상태/흐름(`QuizGame`)을 클래스 단위로 묶으면 퀴즈 데이터·정답 판정과 퀴즈 목록·최고 점수·파일 입출력 상태를 한 객체 안에서 일관되게 관리할 수 있습니다.
- 전역 변수나 여러 딕셔너리/함수를 일일이 넘기는 함수 기반 구조보다 상태 변경 지점이 명확해지고, 기능 확장이나 단위별 수정 시 부작용을 줄이기 쉽습니다.

**데이터 파일(`state.json`) 설명 및 설계 이유:**
- **저장 경로:** 프로젝트 루트(`~/projects/python-quiz-game/state.json`)
- **JSON 선택 이유:** 사람이 직접 열어 보거나 수정하기 쉬운 **가독성**과 리스트·객체 계층을 자연스럽게 표현하는 **구조화** 장점이 있어 콘솔 게임 상태 저장에 적합합니다.
- **역할:** 퀴즈 데이터와 최고 점수를 저장·불러오기하며, 파일이 없거나 손상/오류 발생 시 예외 처리를 거쳐 기본 퀴즈 데이터로 안전하게 동작합니다.

  - **필드 구조:**
    ```json
    {
      "quizzes": [
        {
          "question": "문제 내용",
          "options": ["선택지1", "선택지2", "선택지3", "선택지4"],
          "answer": 1
        }
      ],
      "best_score": 0
    }
    ```

**필드 및 중첩 구조 선택 이유:**
- `quizzes`: 여러 퀴즈 항목을 순서대로 보관하고, 출제/추가/목록 조회하기 위해 리스트(배열) 형태로 구성함
- `각 퀴즈 객체(question, options, answer)`: 문제 문장, 4지선다 보기 목록, 정답 번호를 한 단위로 묶어 데이터 무결성과 직렬화/역직렬화 가독성을 높이기 위해 중첩 객체 구조를 채택함
- `best_score`: 퀴즈 목록과 별도로 누적 최고 점수를 단일 정수 값으로 빠르게 조회/비교/갱신하기 위해 최상위 필드로 분리

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


![퀴즈 추가 실행 결과](docs/screenshots/%ED%80%B4%EC%A6%88(%EB%AC%B8%EC%A0%9C)%20%EC%B6%94%EA%B0%80%20%EC%9D%B4%EB%AF%B8%EC%A7%80.png)


## 5. Git 브랜치 전략 및 커밋 이력
- **브랜치 전략 및 --no-ff 선택 이유:** `main` 브랜치의 안전성을 유지하면서 기능 개선을 독립적으로 진행하기 위해 feat/play-polish 브랜치를 분리함. 병합시 `--no-ff` 옵션을 사용해 기능 단위 병합 커밋을 남겨 변경 이력을 명확히 추적할 수 있도록 함 
- `feat/play-polish` 기능 브랜치에서 작업한 뒤 `--no-ff` 옵션으로 병합했습니다.
- **커밋 단위 및 메시지 규칙:** 기능·수정·문서 작업 단위로 커밋을 나누고, Feat:, Fix:, Docs: 같은 접두사(유형)와 변경 내용을 한눈에 알 수 있는 요약 메시지를 작성하는 관습을 따랐습니다.
- **원격 저장소 동기화:** 원격 저장소`cycle-king2/python-quiz-game`와 `clone` / `pull` / `push`로 동기화 진행


**실행-커밋 이력 및 병합 로그**
kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git log --oneline --graph --all
* ee138c4 (HEAD -> main, origin/main, origin/HEAD) README.md 내용 수정 최종본
* 01bdbe6 Feat: 기본 퀴즈 내용 수정 및 state.json 무시 처리
* 6e489a2 Docs: 프로젝트 설명 및 실행 방법 README 작성
* ed7219b Feat: 콘솔 메뉴 실행 진입점 main.py 추가
* 4b9e5cd Feat: QuizGame 클래스 및 state.json 저장 복구 추가
* f263624 Feat: 입력 검증 유틸리티 추가
* e2d8a54 Feat: 기본 퀴즈 5개 추가
* 2d987bc Feat: 입력 검증 유틸리티 함수 추가
* 58527d6 Feat: Quiz 클래스 구현
* dc3e8df Feat: Quiz 클래스 구현
* 978e3a0 Feat: 파이썬용 .gitignore 파일 추가
* d9586b2 Initial commit

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git checkout -b feat/play-polish
Switched to a new branch 'feat/play-polish'

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ echo "">> README.md && echo "## 퀴즈 주제 선정 이유" >> README.md && echo "-관심 주제를 바탕으로 4지선다 콘ㅌ솔 퀴즈와 상태 저장 흐름을 직접 구현해 보기 위해 선정했습니." >> README.md

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git add README.md
kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git commit -m "Docs: README에 퀴즈 주제 선정 이유 추가"
[feat/play-polish 9122ea7] Docs: README에 퀴즈 주제 선정 이유 추가
 1 file changed, 3 insertions(+), 1 deletion(-)

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git merge --no-ff feat/play-polish -m "Merge branch 'feat/play-polish' into main"
Merge made by the 'ort' strategy.
 README.md | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git push origin main
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 4 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 575 bytes | 575.00 KiB/s, done.
Total 4 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 2 local objects.
To https://github.com/cycle-king2/python-quiz-game.git
   ee138c4..74ae5b1  main -> main

kimkidong@DESKTOP-MS0C3LR:~/projects/python-quiz-game$ git log --oneline --graph --all -n 6
*   74ae5b1 (HEAD -> main, origin/main, origin/HEAD) Merge branch 'feat/play-polish' into main
|\  
| * 9122ea7 (feat/play-polish) Docs: README에 퀴즈 주제 선정 이유 추가
|/  
* ee138c4 README.md 내용 수정 최종본
* 01bdbe6 Feat: 기본 퀴즈 내용 수정 및 state.json 무시 처리
* 6e489a2 Docs: 프로젝트 설명 및 실행 방법 README 작성
* ed7219b Feat: 콘솔 메뉴 실행 진입점 main.py 추가



- 원격 저장소(`cycle-king2/python-quiz-game`)와 동기화(`clone` / `pull` / `push`)를 진행했습니다.

![브랜치 병합과 커밋 이력](docs/screenshots/브랜치%20병합과%20커밋%20이력.png)

![git log 스크린샷 결과](docs/screenshots/git%20log%20스크린샷%20결과.png)

---


## 6. 예외처리, 저장소 한계, 유지보수 및 회고..그리고 개선점

- **대표적 예외 사례 및 대응 방안:** `OSError, json.JSONDecodeError, KeyError, TypeError, ValueError`가 발생하더라도 프로그램이 중단되지 않도록 예외를 잡고, 손상/누락 시 기본 퀴즈 및 초기 점수로 안전하게 복구하도록 구성

- **JSON 저장/복구 성능 한계와 DB 비교:** 현재 방식은 파일 전체를 읽고 쓰는 구조라 소규모 콘솔 퀴즈에는 적합하지만, 데이터가 커지면 전체 파싱/직렬화 비용과 메모리 부담이 늘어나고 동시 쓰기 충돌 위험이 생겨 다중 사용자·대규모 데이터·검색/필터링이 필요해지면 SQLite나 RDBMS 같은 데이터베이스(DB)로 전환하는 것이 유리

- **백업/복구 대응 및 향후 개선점:** 현재 손상 시 기본 퀴즈로 복구하는 수준이므로, 추후 .bak 백업 파일 생성이나 수동 복구 메뉴/옵션을 추가하면 사용자 데이터 손실 방지를 더 강화할 수 있음

![백업 및 수동 복구](docs/screenshots/백업%20및%20수동복구%20스크린샷.png)

- **요구사항 변경 시 수정 대상 파일 및 테스트 목록:** 
가. 문제/선택지/정답 스키마 변경 시: `quiz.py, default_quizzes.py, quiz_game.py` 수정 → 기본 퀴즈 로딩, 퀴즈 추가/목록/풀이 및 `state.json` 저장·복구 테스트
나. 콘솔 입력 규칙/검증 조건 변경 시: `input_utils.py, main.py` 수정 → 잘못된 메뉴/보기/정답 입력 시 재입력 유도 및 정상 흐름 테스트
다. 저장 포맷/경로 변경 시: `quiz_game.py` 수정 → 파일 미존재, JSON 손상(JSONDecodeError), 타입 오류(TypeError/ValueError) 시 예외 복구 테스트

- **회고:** 콘솔 입출력 흐름과 모듈 간 책임을 분리하면서 유지보수성을 높였고, 파이썬 캐시`__pycache__/`나 가상환경/에디터 설정 등을 무시하기 위해 `.gitignore`를 설정함

---
