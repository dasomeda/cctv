import streamlit as st
import pandas as pd

st.title("나의 집 근처 데이터 서비스")
st.image('image.jpg')

try:
    data = pd.read_csv("members.csv", encoding='cp949')  # 다른 가능한 인코딩: 'euc-kr', 'ISO-8859-1'
except UnicodeDecodeError:
    st.error("CSV 파일 인코딩 문제로 파일을 읽을 수 없습니다. 올바른 인코딩을 사용하고 있는지 확인하세요.")
    data = pd.DataFrame()  # 빈 DataFrame으로 대체

data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    elif not data.empty:
        # 사용자 확인
        user = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}님 환영합니다!")
            st.session_state["ID"] = ID
            
            progress_text = "로그인 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
            
            # 페이지 전환에 대한 처리가 필요
            # st.switch_page("pages/cctv.py")  # 실제 존재하는 유효한 페이지 확인 필요
            
        else:
            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")