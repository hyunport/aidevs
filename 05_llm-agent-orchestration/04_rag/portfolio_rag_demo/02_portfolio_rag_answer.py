"""pgvector 검색 Context를 사용해 포트폴리오 질문에 답합니다."""

import sys

from _portfolio_rag import answer_question


DEFAULT_QUESTION = (
    "태웅님의 현재 포트폴리오를 분석하고, 균형형 포트폴리오로 변경하려면 "
    "얼마씩 조정해야 하는지 알려줘."
)


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]).strip() or DEFAULT_QUESTION
    result = answer_question(question)
    print("질문:", question)
    print("\n답변:\n", result["answer"])
    print("\n검색 출처:", result["sources"])

