import os
import datetime

from dotenv import load_dotenv
from openai import OpenAI
from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
from pymongo import MongoClient

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

mongoClient = MongoClient(host="localhost", port=27017)
client = OpenAI(
    api_key=openai_api_key,
    base_url="https://api.upstage.ai/v1"
)
gd = GdeltDoc()

db = mongoClient['project1']
collection = db['NewsAnalysis']

text = "삼성전자 주가는 상승한 반면에, 테슬라의 주가는 하락했습니다."
prompt = """아래 뉴스에서 S&P에 상장된 기업명을 모두 추출하고, 기업에 해당하는 감성을 분석하시오.
각 감석의 스코어링을 하시오. 각 스코어의 합은 1이 되어야 합니다. 소수점 첫번째 자리까지만 생성해주세요.
출력포맷은 리스트이며, 세부 내용은 다음과 같습니다.
반드시 출력포맷만을 생성하고, 다른 텍스트는 생성하지 마시오.
[{"organization": <기업명>, "positive": 0~1, "negative": 0~1, "neutral": 0~1}, ...]
    
텍스트: 
"""

def solar_pro_generate(query):
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": query
    }]

    response = client.chat.completions.create(
        model="solar-pro",
        messages=messages
    )

    return response.choices[0].message.content

def get_url(keyword):
    f = Filters(
        start_date="2024-05-01",
        end_date="2024-11-02",
        num_records=10,
        keyword=keyword,
        domain="nytimes.com",
        country="US",
    )

    articles = gd.article_search(f)
    return articles

def url_crawling(df):
    urls = df["url"]
    titles = df["title"]
    texts = []
    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        texts.append(article.text)

    return texts, titles


orgs = ['microsoft', 'apple']
def analysis():
    for org in orgs:
        df = get_url(org)
        texts, titles = url_crawling(df)
        for idx, text in enumerate(texts):
            news_item = {}
            answer = solar_pro_generate(prompt + text)
            try:
                answer_list = eval(answer)
                news_item["text"] = text
                news_item["title"] = titles[idx]
                news_item["sentiments"] = answer_list
                news_item["date"] = datetime.datetime.now()

                insert_id = collection.insert_one(news_item).inserted_id
                print(insert_id)
            except:
                continue


if __name__ == "__main__":
    analysis()