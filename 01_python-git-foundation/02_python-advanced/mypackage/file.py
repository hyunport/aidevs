

def normalize_question(question: str) -> str:
    """질문 앞뒤의 공백을 제거합니다.

    question:
        사용자가 입력한 원본 질문입니다.

    return:
        앞뒤 공백이 제거된 질문 문자열입니다.
    """

    return question.strip()


def make_mock_answer(question: str) -> str:
    """실제 AI 호출 대신 연습용 답변을 만듭니다."""

    return f"'{question}'에 대한 연습용 답변입니다."


def main() -> None:
    """프로그램 실행 시작점입니다."""

    while True:
        # user_question = "  FastAPI는 무엇인가요?  "
        user_question = input("질문을 입력하세요: ")
        if user_question == "q":
            break;

        cleaned_question = normalize_question(user_question)
        answer = make_mock_answer(cleaned_question)

        print("원본 질문:", user_question)
        print("정리된 질문:", cleaned_question)
        print("답변:", answer)


main()