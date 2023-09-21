import openai
import json

APIKey = ""
try:
    json_file = open('APIKey.json', 'r')
    apikey = json.load(json_file)
    APIKey = apikey["APIKey"]
except Exception:
    print("APIKeyの取得に失敗しました。")

openai.api_key = APIKey

with open('./data/transcribe-s3.json', 'r', encoding='utf-8') as file:
    manuscript_data = json.load(file)

manuscript = manuscript_data["results"]["transcripts"][0]["transcript"]
# items = manuscript_data["results"]["items"]

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": "あなたは動画の字幕作成者です。"
        },
        {
            "role": "user",
            "content": manuscript
        },
        {
            "role": "system",
            "content": "これはマニュアル説明動画の音声を文字起こしした文章です。この文章を句読点に注目して適切なステップごとに分割してください。。"
        },
        {
            "role": "system",
            "content": "[{'step': 1, 'description': 'XXX'}, ...]といったフォーマットのjson形式で返答してください。言語は日本語を使用してください。",
        },
    ],
)

# print(res)
c=0
# for each in res["choices"]["message"]:
#     print(each["content"])
#     print(""+str(c)+"\n")
#     c+=1
print(res["choices"][0]["message"]["content"])
