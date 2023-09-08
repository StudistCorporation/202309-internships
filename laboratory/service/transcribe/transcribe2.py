import json
import urllib.parse
import boto3
import datetime
import time
import logging

logger = logging.getLogger()
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

job_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_Transcription'

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName= job_name,
            LanguageCode='ja-JP',
            Media={
                'MediaFileUri': 'https://s3.ap-northeast-1.amazonaws.com/' + bucket + '/' + key
            },
            OutputBucketName=bucket,
            
        )
        s3.get_object(Bucket=bucket, Key=key)
        s3.upload_file('output.mp4', outputbucket, 'output.json')
    except Exception as e:
        logger.error(e)
        logger.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    # Transcribeジョブの進行状況を監視
    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = job['TranscriptionJob']['TranscriptionJobStatus']
        
        if status in ['COMPLETED', 'FAILED']:
            break
        
        logger.info(f"Transcription job is in progress. Status: {status}")
        time.sleep(30)  # 30秒ごとにジョブの状態を確認

    # Transcribeジョブが完了した場合、結果を取得
    if status == 'COMPLETED':
        result_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribe_result = transcribe.get_object(Bucket=bucket, Key=result_uri.split('/')[-1])
        
    
        logger.info("Transcription Result:")
        logger.info(transcribe_result['Body'].read().decode('utf-8'))
    else:
        logger.error("Transcription job failed.")
        
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from Lambda!',
            'result_uri': result_uri
        })
    }