# 01_login.py
import streamlit as st

#선언-------------------------------------------------
loginout = st.query_params.get("loginout", "logout")

if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""
# if "login" not in st.session_state:
#     st.session_state.login = False
# login_submit = None


#화면-------------------------------------------------
if loginout == "logout":
    st.title("LOGIN")
    with st.form("login_form"):
        input_id = st.text_input("ID 입력")
        input_pwd = st.text_input("PWD 입력", type="password")

        submit_area , reset_area = st.columns(2)
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")
        with reset_area:
            reset_submit = st.form_submit_button("RESET", on_click=reset)

        if login_submit:
            if input_id == "id01" and input_pwd == "pwd01":
               st.query_params["loginout"] = "login"
               st.rerun()
            else:
                st.toast("로그인 실패")
        # login_submit, reset = st.columns(2)
        # login_submit, reset = st.form_submit_button("LOGIN")
        # if login_submit:
        #     if input_id == "id01" and input_pwd == "pwd01":
        #         st.query_params["loginout"] = "login"
        #     else:
        #         st.toast("로그인 실패")
else:
    st.info("로그인을 했습니다.")
    logout = st.button("LOGOUT")
    if logout:
        st.query_params["loginout"] = "logout"
        st.rerun()
#코드-------------------------------------------------
# if login_submit:
#     if input_id == "id01" and input_pwd == "pwd01":
#         ""
#     else:
#         ""