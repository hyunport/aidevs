# 03_pizza.py
import streamlit as st

def init_state():
    if "pizza" not in st.session_state:
        st.session_state.pizza = ""
    if "dough" not in st.session_state:
        st.session_state.dough = ""
    if "cheeze" not in st.session_state:
        st.session_state.cheeze = ""
    if "toping" not in st.session_state:
        st.session_state.toping = ""
    if "count" not in st.session_state:
        st.session_state.count = 0
init_state()

def add():
    st.session_state.count = st.session_state.count + 1

def dec():
    if st.session_state.count == 0:
        return
    st.session_state.count = st.session_state.count - 1


def clear_state():
    st.session_state.dough = ""
    st.session_state.cheeze = ""
    st.session_state.toping = ""
    st.session_state.pizza = ""
    st.session_state.count = 0

def make_p1():
    st.toast("p1 피자를 만듭니다.")
    st.session_state.pizza = "pizza1"
    st.session_state["dough"] = "씬"
    st.session_state["cheeze"] = "파마산"
    st.session_state["toping"] = "페퍼로니"

def make_p2():
    st.toast("p2 피자를 만듭니다.")
    st.session_state.pizza = "pizza2"
    st.session_state["dough"] = "두꺼운"
    st.session_state["cheeze"] = "체다"
    st.session_state["toping"] = "불고기"

def make_p3():
    st.toast("p3 피자를 만듭니다.")
    st.session_state.pizza = "pizza3"
    st.session_state["dough"] = "화덕"
    st.session_state["cheeze"] = "비싼"
    st.session_state["toping"] = "포테이토"

#------------------------------------------------------------------------------------
st.title("pizza")
if st.session_state.pizza != "":
    st.info(f"당신이 선택한 피자는: {st.session_state.pizza} 입니다.")
    st.info(f"피자 갯수: {st.session_state.count}")
    left, right = st.columns(2)
    with left:
        st.button("추가", on_click=add, use_container_width= True)
    with right:
        st.button("감소", on_click=dec, use_container_width= True)

p1, p2, p3 = st.columns(3)
with p1:
    p1_clicked = st.button("p1", on_click = make_p1)

with p2:
    p2_clicked = st.button("p2", on_click = make_p2)

with p3:
    p3_clicked = st.button("p3", on_click = make_p3)

submit, reset = st.columns(2)

with st.form("pizza_form"):
    dough = st.text_input("도우 선택", key= "dough")
    cheeze = st.text_input("치즈 선택", key= "cheeze")
    toping = st.text_input("토핑 선택", key= "toping")
    submit, reset = st.columns(2)
    submit = st.form_submit_button("제출")
    reset = st.form_submit_button("초기화", on_click=clear_state)

#--------------------------------------------------------------------

if submit:  # 제출 버튼을 누른 뒤에만 설문 결과를 화면에 표시합니다.
    st.subheader("주문 내역")  # 결과 영역의 제목을 표시합니다.
    st.subheader(f"주무하신 피자는: {st.session_state.pizza}")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
    st.subheader(f"주무하신 피자 갯수는: {st.session_state.count}")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
    st.write(f"도우: {dough if dough else '도우를 고르지 않으셨습니다'} ")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
    st.write(f"치즈: {cheeze if cheeze else '치즈를 고르지 않으셨습니다.'}")  # 이름이 비어 있으면 '미입력'으로 표시합니다.
    st.write(f"토핑: {toping if toping else '토핑을 고르지 않으셨습니다.'}")  # 이름이 비어 있으면 '미입력'으로 표시합니다.

    
else:  # 아직 제출 버튼을 누르지 않은 상태라면 안내 메시지를 표시합니다.
    st.info("주문을 해주세요.")
