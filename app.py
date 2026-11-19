from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# app.py가 있는 폴더 기준으로 데이터 파일을 찾는다 (서버에서도 동작)
HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data.csv")

LABEL = {"branch": "지점", "month": "월", "visitors": "방문객(명)", "sales": "매출(천원)"}

st.set_page_config(page_title="지점별 월간 매출", layout="wide")
st.title("지점별 월간 매출 대시보드")
st.caption("연습용 가상 데이터입니다.")

# 위젯: 값이 바뀌면 이 파일이 처음부터 다시 실행된다
branches = st.sidebar.multiselect(
    "지점 선택", sorted(df["branch"].unique()), default=sorted(df["branch"].unique())
)
m_start, m_end = st.sidebar.slider("월 범위", 1, 12, (1, 12))
metric = st.sidebar.radio("지표", ["sales", "visitors"], format_func=LABEL.get)

# 선택을 모두 지웠을 때 안내
if not branches:
    st.info("왼쪽에서 지점을 하나 이상 선택하세요.")
    st.stop()

view = df[df["branch"].isin(branches) & df["month"].between(m_start, m_end)]

c1, c2, c3 = st.columns(3)
c1.metric("매출 합계(천원)", f"{view['sales'].sum():,}")
c2.metric("방문객 합계(명)", f"{view['visitors'].sum():,}")
c3.metric("방문객당 매출(천원)", f"{view['sales'].sum() / view['visitors'].sum():.1f}")

# Plotly 차트는 브라우저가 글자를 그려서 한글이 그대로 보인다
line = px.line(
    view, x="month", y=metric, color="branch", markers=True,
    labels=LABEL, title=f"월별 {LABEL[metric]}",
)
line.update_xaxes(dtick=1)
st.plotly_chart(line, use_container_width=True)

total = view.groupby("branch", as_index=False)[metric].sum()
bar = px.bar(total, x="branch", y=metric, color="branch", labels=LABEL,
             title=f"지점별 {LABEL[metric]} 합계")
st.plotly_chart(bar, use_container_width=True)

with st.expander("데이터 표 보기"):
    st.dataframe(view.rename(columns=LABEL), use_container_width=True)
