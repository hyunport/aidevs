import streamlit as st  # Python 코드로 웹 화면을 만들기 위해 Streamlit을 st라는 별칭으로 가져옵니다.

def response(prompt: str):
    return f"{prompt}"


st.title("역할별 메시지 출력")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

for message in st.session_state.messages:  # 목록이나 반복 가능한 데이터를 하나씩 꺼내 같은 작업을 반복합니다.
    with st.chat_message(message["role"]):  # 파일, 화면 영역, 로딩 상태처럼 시작과 종료가 있는 작업 범위를 만듭니다.
        st.write(message["content"])  # 문자열, 숫자, 객체를 Streamlit 화면에 출력합니다.

prompt = st.chat_input("질문을 입력하세요")  # 채팅 입력창에서 사용자가 보낸 질문 문자열을 변수에 저장합니다.
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response_text = response(prompt)
    st.session_state.messages.messages.append({"role": "assistant", "content": "prompt"})
    st.rerun()
    