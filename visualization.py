import streamlit as st
import pandas as pd
from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)
db = client['news-organization']
collection = db['NewsAnalysis']

data = list(collection.find())

sentiments = []
for item in data:
    sentiments.extend(item['sentiments'])

df = pd.DataFrame(sentiments)

df['seendate'] = pd.to_datetime(df['seendate'])
print(df)

# title
st.title("기엽별 날짜에 따르 감성 지수 변화")

# 기업 선택
organization = st.selectbox("기업을 선택하세요.", ['Microsoft', 'Apple'])

# 선택한 기업의 데이터 필터링
selected_df = df.loc[df['organization'] == organization].set_index('seendate')

# 감성지수 차트
st.line_chart(selected_df[['positive', 'negative', 'neutral']])