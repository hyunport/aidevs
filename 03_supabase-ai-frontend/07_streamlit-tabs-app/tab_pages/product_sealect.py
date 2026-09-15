"""데이터베이스조회 탭입니다."""
import httpx
import streamlit as st
import pandas as pd

API_BASE_URL = "https://zero2-mini-porject.onrender.com"  # 프론트엔드가 호출할 백엔드 서버의 기본 주소를 한 곳에서 관리합니다.

@st.dialog("삭제")
def show_del(p:dict) -> None:
    st.info("Delete")
    st.write(f"{p['name']}삭제 하시겠습니까")
    if st.button("삭제 요청"):
            with st.spinner("데이터 요청"):
                response = httpx.get(f"{API_BASE_URL}/product/delete/{p['id']}", timeout=10.0)
            if response.status_code == 200:
                st.rerun()

@st.dialog("수정")
def show_up(p:dict) -> None:
    st.info(f"{p['id']}를 수정 하겠습니다.")
    with st.form(f"form_{p['id']}"):
        product_name = st.text_input("이름:", value=p["name"])
        product_price = st.number_input("가격:", value=int(p["price"]))
        if st.form_submit_button("수정"):
            payload = {"name:": product_name, "price": product_price}
            with st.spinner("데이터 요청"):
                response = httpx.put(f"{API_BASE_URL}/product/update/{p['id']}",json=payload, timeout=10.0)
            if response.status_code == 200:
                st.rerun()



def product_sealect() -> None:
    """데이터를 확인합니다."""

    st.subheader("Product 조회")
    st.caption("Product 테이블을 선택하고 데이터를 확인합니다.")

    with st.spinner("데이터 요청"):
        response = httpx.get(f"{API_BASE_URL}/product/getall", timeout=10.0)

        if response.status_code == 200:
            st.info("ok")
            result = response.json()
            # st.info(result)

            # df = pd.DataFrame(result)
            # # st.table(df)
            # st.dataframe(df)

            if not result:
                st.info("product가 없습니다.")
            for p in result:
                with st.container(border=True):
                    product_col, button_col= st.columns([3,1])
                    with product_col:
                        st.write(p["id"])
                        st.write(p["name"])     
                        st.write(f"{p["price"]}원")
                                           
                    with button_col:
                        if st.button("삭제", key=f"de_{p['id']}"):
                            show_del(p)
                        if st.button("수정", key=f"up_{p['id']}"):
                            show_up(p)
        else:
            st.warning("Fail")