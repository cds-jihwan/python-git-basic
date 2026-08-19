# 나만의 퀴즈 게임

코디세이 AI 올인원 2기 2주차 과제 '컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기'

터미널에서 동작하는 CS 기초 지식 퀴즈 게임입니다.

## 프로젝트 개요

터미널에서 4지선다 CS 퀴즈를 풀 수 있는 콘솔 프로그램입니다.
퀴즈를 직접 등록하고 목록을 확인할 수 있으며, 푼 결과는 점수로 계산됩니다.

퀴즈 데이터와 최고 점수는 `state.json`에 저장되어 프로그램을 종료했다가
다시 실행해도 그대로 유지됩니다.

Python 기본 문법으로 입력과 출력의 흐름을 만들고, `Quiz`와 `QuizGame`
두 개의 클래스로 역할을 나눠 구조화하는 것을 목표로 했습니다.

## 퀴즈 주제와 선정 이유

**주제: CS 기초 지식**

개발자라면 CS 지식이 필수라고 생각해서 이 과제를 학습 기회로 삼았습니다.
자료구조, 시간복잡도, 네트워크, 운영체제, 데이터베이스, Git 등 기본 개념을
4지선다로 만들었습니다. 정답이 명확해 선택지로 만들기 좋고, 선택지가 짧아
터미널 화면에서도 읽기 편합니다.

## 실행 방법

```bash
git clone https://github.com/cds-jihwan/python-git-basic.git
cd python-git-basic
python3 main.py
```

- Python 3.10 이상 필요
- 외부 라이브러리 설치 불필요 (표준 라이브러리 `json`만 사용)

## 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 순서대로 출제합니다. 정답/오답을 즉시 안내하고 마지막에 점수를 계산합니다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 등록하고 바로 저장합니다. |
| 3 | 퀴즈 목록 | 등록된 퀴즈를 번호와 함께 출력합니다. |
| 4 | 점수 확인 | 최고 점수와 그때의 정답 수를 보여줍니다. |
| 5 | 종료 | 데이터를 저장하고 종료합니다. |

### 입력 처리

- 입력 앞뒤 공백을 제거합니다. (`" 1 "` → `1`)
- 숫자가 아니거나(`abc`), 허용 범위 밖이거나(`9`), 빈 입력이면
  안내 메시지를 출력하고 다시 입력받습니다.
- `Ctrl+C`(KeyboardInterrupt), `Ctrl+D`(EOFError)를 눌러도 비정상 종료되지 않고
  안내 메시지 출력 후 **데이터를 저장하고** 종료합니다.

## 파일 구조

```
python-git-basic/
├── main.py         # 진입점. QuizGame을 실행하고 종료 처리를 담당
├── quiz.py         # Quiz 클래스 — 퀴즈 한 문제 (출제, 정답 확인, dict 변환)
├── quiz_game.py    # QuizGame 클래스 — 메뉴, 게임 진행, 파일 저장/불러오기
├── state.json      # 데이터 파일 (첫 실행 시 자동 생성, Git 추적 제외)
├── README.md
└── .gitignore
```

### 클래스 구조

**`Quiz`** — 퀴즈 한 문제를 표현합니다.

| 구분 | 이름 | 역할 |
|---|---|---|
| 속성 | `question`, `choices`, `answer` | 문제, 선택지 4개, 정답 번호(1~4) |
| 메서드 | `display(index)` | 문제 번호와 선택지를 화면에 출력 |
| 메서드 | `is_correct(user_answer)` | 입력한 번호가 정답인지 판단 |
| 메서드 | `to_dict()` / `from_dict(data)` | JSON 저장을 위한 dict 변환 / 복원 |

**`QuizGame`** — 게임 전체를 관리합니다.

| 구분 | 이름 | 역할 |
|---|---|---|
| 속성 | `quizzes`, `best_score` | 퀴즈 목록, 최고 점수 |
| 메서드 | `run()`, `show_menu()` | 메뉴 표시와 반복 진행 |
| 메서드 | `play()`, `show_result()` | 퀴즈 출제와 결과·점수 계산 |
| 메서드 | `add_quiz()`, `list_quizzes()`, `show_score()` | 각 메뉴 기능 |
| 메서드 | `load()`, `save()`, `default_quizzes()` | 파일 입출력과 기본 데이터 |

## 데이터 파일 설명

**경로**: 프로젝트 루트의 `state.json`
**인코딩**: UTF-8 (`ensure_ascii=False`로 한글을 그대로 저장)
**역할**: 퀴즈 목록과 최고 점수를 저장해 프로그램을 껐다 켜도
데이터가 유지되도록 합니다.

```json
{
  "quizzes": [
    {
      "question": "스택(Stack)의 데이터 처리 방식은?",
      "choices": ["FIFO", "LIFO", "우선순위", "무작위"],
      "answer": 2
    }
  ],
  "best_score": 86,
  "best_correct": 6,
  "best_total": 7
}
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int | 최고 점수 (0~100) |
| `best_correct` / `best_total` | int | 최고 점수를 낸 게임의 정답 수 / 전체 문제 수 |

### 예외 처리

| 상황 | 동작 |
|---|---|
| 파일이 없음 (첫 실행) | 안내 후 기본 퀴즈 7문항으로 시작 |
| 파일이 손상됨 (JSON 파싱 실패, 필수 키 없음) | 안내 후 기본 데이터로 복구 |
| 읽기/쓰기 오류 (`OSError`) | 안내 메시지 출력 후 계속 진행 |

`state.json`은 실행할 때마다 내용이 바뀌므로 `.gitignore`로 제외했습니다.
저장소를 clone한 직후에는 파일이 없으므로 기본 퀴즈 7문항으로 시작합니다.

## 점수 계산

```
점수 = 맞힌 문제 수 ÷ 전체 문제 수 × 100
```

## 실행 화면


![메뉴](screenshots/menu.png)
![퀴즈 풀기](screenshots/play.png)
![퀴즈 추가](screenshots/add_quiz.png)
![점수 확인](screenshots/score.png)

## 개발 환경

- macOS / VSCode
- Python 3.13
- Git 2.50
