"""포트폴리오 문서 검색 결과를 Context로 전달해 Ollama 답변을 생성합니다."""

import os
import re

import httpx

from _pgvector_store import OLLAMA_BASE_URL, similarity_search


COLLECTION = "portfolio_demo"
CHAT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
USER_IDS = {
    "태웅": "user_001",
    "오현": "user_002",
    "기화": "user_003",
}
ASSET_NAMES = ("국내 주식", "해외 주식", "채권", "현금")


def _parse_total_asset(content: str) -> int | None:
    match = re.search(r"총자산:\s*([\d,]+)원", content)
    return int(match.group(1).replace(",", "")) if match else None


def _parse_allocations(content: str) -> dict[str, int]:
    allocations: dict[str, int] = {}
    for asset_name in ASSET_NAMES:
        match = re.search(rf"- {re.escape(asset_name)}:\s*(\d+)%", content)
        if match:
            allocations[asset_name] = int(match.group(1))
    return allocations


def _calculation_context(question: str, results: list[dict]) -> str:
    """LLM이 산술을 추측하지 않도록 검색 문서의 정확한 계산 결과를 만듭니다."""
    target_document = next(
        (
            item
            for item in results
            if item.get("metadata", {}).get("guide_type") == "balanced_target"
        ),
        None,
    )
    target_allocations = (
        _parse_allocations(target_document["content"]) if target_document else {}
    )
    needs_rebalancing = any(
        keyword in question for keyword in ("균형형", "리밸런싱", "조정", "매수", "매도")
    )
    lines: list[str] = ["[코드에서 확정한 정확한 금액 계산]"]

    for item in results:
        metadata = item.get("metadata", {})
        if metadata.get("document_type") != "portfolio":
            continue

        total_asset = _parse_total_asset(item["content"])
        current_allocations = _parse_allocations(item["content"])
        if total_asset is None or len(current_allocations) != len(ASSET_NAMES):
            continue

        user_name = metadata.get("user_name", item["title"])
        lines.append(f"{user_name}님의 총자산은 {total_asset:,}원이며 리밸런싱 전후 동일하다.")
        for asset_name in ASSET_NAMES:
            ratio = current_allocations[asset_name]
            amount = total_asset * ratio // 100
            lines.append(f"현재 {asset_name}: {ratio}% = {amount:,}원")

        stock_ratio = current_allocations["국내 주식"] + current_allocations["해외 주식"]
        risks: list[str] = []
        if current_allocations["해외 주식"] >= 50:
            risks.append("해외시장 및 환율 변동 위험")
        if stock_ratio >= 70:
            risks.append("시장 하락 위험")
        if current_allocations["채권"] < 10:
            risks.append("방어 자산 부족")
        if current_allocations["현금"] < 10:
            risks.append("유동성 위험")
        if current_allocations["현금"] > 30:
            risks.append("낮은 기대수익 가능성")
        if max(current_allocations.values()) > 50:
            risks.append("단일 자산군 집중 위험")
        lines.append("조건을 충족한 적용 위험: " + (", ".join(risks) if risks else "없음"))

        if needs_rebalancing and len(target_allocations) == len(ASSET_NAMES):
            lines.append("균형형 목표와 조정 금액:")
            for asset_name in ASSET_NAMES:
                current_amount = total_asset * current_allocations[asset_name] // 100
                target_ratio = target_allocations[asset_name]
                target_amount = total_asset * target_ratio // 100
                difference = target_amount - current_amount
                action = "매수" if difference > 0 else "매도" if difference < 0 else "유지"
                lines.append(
                    f"{asset_name}: 목표 {target_ratio}% = {target_amount:,}원, "
                    f"{action} {abs(difference):,}원"
                )

    return "\n".join(lines)


def retrieve(question: str) -> list[dict]:
    """질문에 이름이 있으면 사용자 문서를 정확히 필터링하고 기준 문서를 함께 찾습니다."""
    results: list[dict] = []
    mentioned_user_ids = [user_id for name, user_id in USER_IDS.items() if name in question]

    if mentioned_user_ids:
        for user_id in mentioned_user_ids:
            results.extend(
                similarity_search(
                    question,
                    collection=COLLECTION,
                    top_k=1,
                    metadata_filter={"document_type": "portfolio", "user_id": user_id},
                )
            )
        guide_types = ["profile", "risk"]
        if any(
            keyword in question
            for keyword in ("균형형", "리밸런싱", "조정", "매수", "매도")
        ):
            guide_types.append("balanced_target")
        for guide_type in guide_types:
            results.extend(
                similarity_search(
                    question,
                    collection=COLLECTION,
                    top_k=1,
                    metadata_filter={"document_type": "guide", "guide_type": guide_type},
                )
            )
    else:
        results = similarity_search(question, collection=COLLECTION, top_k=5)

    unique: dict[str, dict] = {}
    for item in results:
        unique[item["id"]] = item
    return list(unique.values())


def answer_question(question: str) -> dict:
    results = retrieve(question)
    if not results:
        return {"answer": "관련 포트폴리오 문서를 찾지 못했습니다.", "sources": []}

    context = "\n\n".join(
        f"[출처: {item['source']}]\n{item['content']}" for item in results
    )
    context = f"{context}\n\n{_calculation_context(question, results)}"
    needs_rebalancing = any(
        keyword in question for keyword in ("균형형", "리밸런싱", "조정", "매수", "매도")
    )
    if needs_rebalancing:
        answer_scope = "현재 포트폴리오, 투자 성향, 적용 위험, 리밸런싱, 금액 계산"
    else:
        answer_scope = (
            "현재 포트폴리오, 투자 성향, 적용 위험만 답변한다. "
            "리밸런싱 제안과 목표 금액 계산은 절대 포함하지 않는다."
        )
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {
                    "role": "system",
                    "content": """
제공된 Context만 사용하여 한국어로 답하세요.
사용자 이름, 총자산, 자산별 비중을 정확하게 인용하세요.
금액은 총자산 × 비중으로 계산하고 원 단위 또는 만 원 단위로 명확히 표시하세요.
리밸런싱은 목표 금액 - 현재 금액으로 계산하고 매수 또는 매도를 표시하세요.
리밸런싱 전후 총자산은 바뀌지 않습니다.
Context의 '코드에서 확정한 정확한 금액 계산'이 있으면 반드시 그 숫자를 그대로 사용하고 다시 계산하지 마세요.
위험은 '조건을 충족한 적용 위험'에 적힌 항목만 안내하고 기준 문서의 모든 위험을 나열하지 마세요.
자산 이름과 한국어 표현도 계산 Context의 문구를 그대로 사용하세요.

답변은 질문에 필요한 항목만 다음 순서로 작성하세요.
1. 현재 포트폴리오
2. 투자 성향
3. 주요 위험
4. 리밸런싱 제안
5. 금액 기준 계산

Context에 없는 최신 시세나 수익률은 추측하지 마세요.
질문이 리밸런싱, 균형형 전환, 조정, 매수 또는 매도를 요구하지 않으면 리밸런싱과 목표 금액 계산을 절대 작성하지 마세요.
마지막에 교육용 예시이며 실제 투자 권유가 아니라고 안내하세요.
""".strip(),
                },
                {
                    "role": "user",
                    "content": f"답변 범위: {answer_scope}\n질문: {question}\n\nContext:\n{context}",
                },
            ],
        },
        timeout=120,
    )
    response.raise_for_status()
    return {
        "answer": response.json()["message"]["content"],
        "sources": sorted({item["source"] for item in results}),
    }
