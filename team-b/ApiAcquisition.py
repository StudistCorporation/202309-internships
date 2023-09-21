


import openai
import json
import subprocess
import os

# API Keyの設定
APIKey = ""
try:
    json_file = open('APIKey.json', 'r')
    apikey = json.load(json_file)
    APIKey = apikey["APIKey"]
except Exception:
    print("APIKeyの取得に失敗しました。")

# Transcribeのデータの取得
try:
    json_file = open('data/transcribe-s3.json', 'r')
    # json_file = open('../team-a/front/data/tamagokake.json', 'r')
    transcribe_data = json.load(json_file)
except Exception:
    print("ファイルの取得に失敗しました。")

openai.api_key = APIKey

items_array = []

# Transcribeのデータを整形
for item in transcribe_data['results']['items']:
    if item['type'] == 'pronunciation':
        items_array.append({
            'startTime': item['start_time'],
            'endTime': item['end_time'],
            'content': item['alternatives'][0]['content']
        })
    else:
        items_array.append({
            'content': item['alternatives'][0]['content']
        })

# print("items_array")
# print(items_array)

# manuscript = transcribe_data['results']['transcripts'][0]['transcript']

# # GPT-3.5-turboでの問い合わせ
# res = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": "これらの文章はとあるマニュアルの説明動画の原稿です。その説明動画を各ステップごとにカットするため適切な長さのステップになるように分割してください。細かすぎる区切りは避けてください。分割した文章は元の文章から1言1句変更しないでください。返答はjson形式で返してください。その際Keyは数字にしてください。"
#         },
#         {
#             "role": "user",
#             "content": manuscript
#         },
#     ],
# )
# # GPT-3.5-turboから返ってきたステップごとの文章
# steps = json.loads(res["choices"][0]["message"]["content"])

# 綺麗にステップごとに分割されたことを仮定したステップごとの文章
steps = {
    "1": "はい。じゃあそれではえ？今回はえ？マイクソフトHの言語設定を英語文に切り替えるとメッセージをやっていきます。",
    "2": "まず手順をアクセスすると、日本語表記で表示されっていうのが分かりますと。",
    "3": "で、今回はこれを英語表記に切り替えていきます。",
    "4": "で、まずえー、右上にあるこの三点リーダーですね。",
    "5": "これをクリックしていただいて、え、この中から設定ですね。",
    "6": "これを開きます。そうすると設定画面が表示されました。",
    "7": "で表示された設定画面から、左のサイドバーにある言語というのをクリックして、言語画面が開きます。",
    "8": "で、この言語の中から今回英語に切り替えたいので、この英語の右にあるえ三点二台からマイクロソフトエッチをこのゲームの表示というのがあるので、えこちらをクリックします。",
    "9": "そうすると再起動という選択肢が出てくるんでこれ再起動します。",
    "10": "そうすると、えーとエッジが再起動されるので、再生された後にえ？T再アクセスすると英語表記に切り替わっていることが確認できると思います。"
}

# segments_info = [
#     {"start_time": "0", "end_time": "20"},
#     {"start_time": "25", "end_time": "35"},
# ]
segments_info = []
step_times = []
prev_end_time = 0.0  # 前回のendTimeを保持するための変数
last_index = 0
for step_key, step_content in steps.items():  # 各ステップの数だけループ
    start_time = 0.0
    end_time = 0.0
    count = 0

    for num in range(last_index, len(items_array)):  # 各アイテムの数だけループ
        if count >= len(step_content):  # ステップの文章の文字数を超えたら
            last_index = num
            break
        if items_array[num]['content'] in step_content: # ステップの文章にアイテムの文章が含まれているか
            # print(item)
            print(">>>"+step_content)
            count += len(items_array[num]['content'])
            if 'startTime' in items_array[num] and 'endTime' in items_array[num]:
                start_time = items_array[num]['startTime']  # ステップの開始時間を取得
                end_time = items_array[num]['endTime']
                print("------------------")
                print(items_array[num]['content'])
                print(start_time)
                print(end_time)
                print(len(step_content))
                print("|")
                print(count)
                print("------------------")
                if start_time and end_time:
                    step_times.append({
                        'step': step_key,
                        'startTime': start_time,
                        'endTime': end_time
                    })
            else:
                start_time = float(start_time) + 0.1  # 前回のendTimeから0.1秒後を開始時間とする
                end_time = float(end_time) + 0.1   # 開始時間から0.1秒後を終了時間とする
                print("------------------")
                print(items_array[num]['content'])
                print(start_time)
                print(end_time)
                print(len(step_content))
                print("|")
                print(count)
                print("------------------")
                if start_time and end_time:
                    step_times.append({
                        'step': step_key,
                        'startTime': start_time,
                        'endTime': end_time
                    })
    # ステップのstartTimeとendTimeをリストに追加
    segments_info.append({
                        'startTime': step_times[0]['startTime'],
                        'endTime': step_times[-1]['endTime']
                    })
    step_times = []  # ステップのstartTimeとendTimeをリセット
    # break
        

        



for el in segments_info:
    print(el)

