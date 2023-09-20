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

manuscript = "はい。じゃあそれではえ？今回はえ？マイクソフトHの言語設定を英語文に切り替えるとメッセージをやっていきます。まず手順をアクセスすると、日本語表記で表示されっていうのが分かりますと。で、今回はこれを英語表記に切り替えていきます。で、まずえー、右上にあるこの三点リーダーですね。これをクリックしていただいて、え、この中から設定ですね。これを開きます。そうすると設定画面が表示されました。で表示された設定画面から、左のサイドバーにある言語というのをクリックして、言語画面が開きます。で、この言語の中から今回英語に切り替えたいので、この英語の右にあるえ三点二台からマイクロソフトエッチをこのゲームの表示というのがあるので、えこちらをクリックします。そうすると再起動という選択肢が出てくるんでこれ再起動します。そうすると、えーとエッジが再起動されるので、再生された後にえ？T再アクセスすると英語表記に切り替わっていることが確認できると思います。"


res = openai.ChatCompletion.create(
     model="gpt-3.5-turbo",
          messages=[
         {
             "role": "system",
             "content": "これらはとあるマニュアルの説明動画の原稿です。これらの文章を適切なステップごとに分割してください。その際原稿の文章の意味が変わらないようにしてください。なお、返答は日本語でお願いします。返答はjson形式で返してください。"
         },
         {
             "role": "user",
             "content": manuscript
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
