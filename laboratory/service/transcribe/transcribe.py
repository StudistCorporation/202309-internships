# import boto3
# import time

# aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
# aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'

# transcribe = boto3.client('transcribe', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-1')


# target_bucket_name = 'your-bucket-name'
# audio_file_key = 'path/to/your/audio/file.mp3'

# job_name = 'transcribe-job-name' # 任意だが一意(NOTE: 時間とか使おう)

# # Transcribeジョブを作成
# response = transcribe.start_transcription_job(
#     TranscriptionJobName=job_name,
#     LanguageCode='ja-JP',  # 音声の言語コードを指定
#     MediaFormat='mp3',     # 音声ファイルのフォーマットを指定
#     Media={
#         'MediaFileUri': f's3://{target_bucket_name}/{audio_file_key}'  # 音声ファイルのS3 URIを指定
#     }
# )

import urllib.parse
import boto3
import datetime
import time

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

job_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_Transcription'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName= job_name,
            LanguageCode='ja-JP',
            Media={
                'MediaFileUri': 'https://s3.ap-northeast-1.amazonaws.com/' + bucket + '/' + key
            },
            OutputBucketName='naata-ouput'
        )
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    # Transcribeジョブの進行状況を監視
    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = job['TranscriptionJob']['TranscriptionJobStatus']
        
        if status in ['COMPLETED', 'FAILED']:
            break
        
        print(f"Transcription job is in progress. Status: {status}")
        time.sleep(30)  # 30秒ごとにジョブの状態を確認

    # Transcribeジョブが完了した場合、結果を取得
    if status == 'COMPLETED':
        result_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribe_result = transcribe.get_object(Bucket=bucket, Key=result_uri.split('/')[-1])
        
        print("Transcription Result:")
        print(transcribe_result['Body'].read().decode('utf-8'))
    else:
        print("Transcription job failed.")
