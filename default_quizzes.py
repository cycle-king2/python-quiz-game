from quiz import Quiz


def get_default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            question="김다미 배우가 출연하지 않은 영화는?",
            choices=["도깨비 1", "마녀 2", "대홍수 3", "소울메이트 4"],
            answer=1,
        ),
        Quiz(
            question="김다미 배우가 출연하지 않은 드라마는?",
            choices=["그해우리는 1", "작은아씨들 2", "이태원클라쓰 3", "백번의 추억 4"],
            answer=2,
        ),
        Quiz(
            question="김다미 배우의 MBTI는?",
            choices=["INTJ 1", "ENFP 2", "ISFP 3", "INFP 4"],
            answer=3,
        ),
        Quiz(
            question="김다미 배우가 졸업한 대학은?",
            choices=["한양대 1", "연세대 2", "동국대 3", "인천대 4"],
            answer=4,
        ),
        Quiz(
            question="김다미 배우의 키는?",
            choices=["160cm 1", "170cm 2", "172cm 3", "175cm 4"],
            answer=2,
        ),
    ]
