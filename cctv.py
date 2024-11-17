import streamlit as st
import pandas as pd

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')
data = pd.read_csv("서울특별시 강서구 CCTV 시설물 정보_20201031.csv")

st.title('우리집 주위에 CCTV 어디있지?')


data = data.copy().fillna(0)
data.loc[:,'size'] = 5*(data['시설물 상태']+data['시설물설치일'])
data


color = {'시설물 상태':'#eb6a37',
         '시설물설치일':'#377ceb'}
data.loc[:,'color'] = data.copy().loc[:,'설치물 특징'].map(color)


st.map(data, latitude="위도",
       longitude="경도",
       size="size",
       color="color")

with st.sidebar:
    st.caption(f'{ID}님 접속중')
    
with st.form("input"):
    type = st.multiselect("시설물종류명", data['시설물종류명'].unique())
    division = st.multiselect("시설물물품구분", data['시설물물품구분'].unique())
    date = st.multiselect("시설물설치일", data['시설물설치일'].unique())
    submitted = st.form_submit_button("조회")
    
    if submitted:
        name_list = []
        result = data["시설물설치일"].drop_duplicates().sort_values().reset_index(drop=True)
        for ty in type:
            for di in division:
                for da in date:
                    name = f"{ty}_{di}_{da}"
                    name_list.append(name)
                    selected_df = data[(data['시설물종류명'] == ty) & (data['시설물물품구분'] == di)& (data['시설물설치일'] == da)]
                    selected_df = selected_df[["시설물설치일","시설물 수"]].rename(columns={"시설물 수": name})
                    result = pd.merge(result, selected_df, on='시설물설치일').sort_values('시설물설치일')
        
        st.line_chart(data=result, x='시설물설치일', y=name_list,use_container_width=True)
        