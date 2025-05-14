import datetime

from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

print(client.list_database_names())

db = client['news_db']
collection = db['NewsText']

# item = {
#     "title": "삼성전자 주가 일시 상승.",
#     "text": "삼성전자의 주가가 일시적으로 상승했다. 장중 최고치는...",
#     "date": datetime.datetime.now()
# }
#
# insert_id = collection.insert_one(item).inserted_id

print(collection.find_one())