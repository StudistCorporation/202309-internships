import json

# JSONファイルを読み込む
with open('./data/transcribe-s3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

transcript_text = data['results']['transcripts'][0]['transcript']

items_array = []

for item in data['results']['items']:
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

print("Transcript:")
print(transcript_text)
print("\nItems:")
for item in items_array:
    print(item)
