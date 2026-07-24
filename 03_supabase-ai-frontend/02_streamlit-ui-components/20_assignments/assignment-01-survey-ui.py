# 로그인 화면
# 로그인 시아래 다양한 컴포넌트를 이용한 설문지 작성 후 
# 설문 화면이 없어지고 결과를 화면에 출력
# # st.number_input
# st.text_input
# st.text_area
# st.selectbox
# st.multiselect
# st.checkbox
# st.slider
# 로그인 비정상시다시 로그인 화면으로 진행
# 과정-------------------------------------------------
#1. 로그인 화면
#2. 로그인 성공 설문조사 화면
#3. 설문조사 완료 결과지만 출력
#4. 설문조사 빈칸, 설문을 해주세요. 입력

#선언-------------------------------------------------
import streamlit as st
from streamlit_local_storage import LocalStorage

#선언-------------------------------------------------
storage = LocalStorage()
loginout = storage.getItem("loginout")

if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""

#화면-------------------------------------------------
if loginout == "logout" or loginout is None:
    st.title("LOGIN")
    with st.form("login_form"):
        input_id = st.text_input("ID 입력", key="input_login_id")
        input_pwd = st.text_input("PWD 입력", type="password", key="input_login_pwd")

        submit_area , reset_area = st.columns(2)
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")
        with reset_area:
            reset_submit = st.form_submit_button("RESET", on_click=reset)

        if login_submit:
            if input_id == "id01" and input_pwd == "pwd01":
               storage.setItem("loginout", "login")
            #    st.rerun()
            else:
                st.toast("로그인 실패")

else:
    st.toast("로그인을 했습니다.")
# ----------------------설문------------------------
    st.title("오늘 하루는 어땠나요?")  # Streamlit 화면의 가장 큰 제목을 표시합니다.

    with st.form("survey_form"):  # form 영역 안의 입력값은 제출 버튼을 눌렀을 때 한 번에 처리됩니다.
        name = st.selectbox("오늘의 날씨는 어땠나요?", ["맑은날", "흐린날", "비 오는날", "눈이 오는날"])  # 사용자가 입력한 이름을 문자열로 저장합니다.
        topic = st.selectbox("오늘 하루의 기분", ["우울한", "쏘쏘", "행복"])  # 목록 중 하나를 선택해 topic 변수에 저장합니다.
        satisfaction = st.slider("오늘의 컨디션은 어떤가요?", min_value=1, max_value=5, value=3)  # 1부터 5 사이의 만족도 점수를 숫자로 저장합니다.
        comment = st.text_area("오늘 하루 고생한 당신에게 한마디!")  # 여러 줄 입력창에 작성한 의견을 문자열로 저장합니다.
        submitted = st.form_submit_button("설문 제출")  # 제출 버튼을 누르면 submitted 값이 True가 됩니다.

# --------------------------------------------------------------------------------------------------------------

    if submitted:  # 제출 버튼을 누른 뒤에만 설문 결과를 화면에 표시합니다.
        st.subheader("오늘의 일지")  # 결과 영역의 제목을 표시합니다.
        st.write(f"오늘은 {name if name else '미입력'} 입니다!")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
        st.write(f"오늘 나의 기분은: {topic}한 날 이였습니다.")  # 선택한 주제를 화면에 출력합니다.
        st.write(f"오늘의 컨디션은: {satisfaction}점 입니다!")  # 슬라이더로 선택한 만족도 점수를 화면에 출력합니다.
        if comment:  # 추가 의견이 입력된 경우에만 의견 내용을 표시합니다.
            st.subheader("고생한 당신에게 한마디")
            st.caption(comment)  # 보조 설명 형태로 추가 의견을 표시합니다.
    else:  # 아직 제출 버튼을 누르지 않은 상태라면 안내 메시지를 표시합니다.
        st.info("설문 내용을 입력한 뒤 '설문 제출' 버튼을 눌러 주세요.")
# ------------------------설문 끝----------------------
    logout = st.button("LOGOUT")
    if logout:
        storage.setItem("loginout", "logout")
        st.rerun()
#코드-------------------------------------------------
