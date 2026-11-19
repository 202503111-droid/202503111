from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

HERE = Path(__file__).parent
df = pd.read_csv(HERE / "data.csv")

st.title("지점별 월간 매출")

branches = st.multiselect("지점 선택", df["branch"].unique(), default=list(df["branch"].unique()))

if not branches:
    st.info("지점을 하나 이상 선택하세요.")
else:
    view = df[df["branch"].isin(branches)]
    st.metric("매출 합계", f"{view['sales'].sum():,}")
    st.plotly_chart(px.line(view, x="month", y="sales", color="branch", markers=True))
    st.dataframe(view)
