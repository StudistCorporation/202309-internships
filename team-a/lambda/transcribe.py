import urllib.parse
import boto3
print('Loading function')

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')

# 候補のファイル名： datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_Transcription' + '_teamA' 
job_name = 'output-transcript4' # HACK:名前が一意な必要があるのでどうするか

output_bucket = 'team-a-test-fetch'

# S3のフォーマット：https://team-a-test-bucket.s3.ap-northeast-1.amazonaws.com/sample-movie.mp4

def lambda_handler(event, context):
    # イベントからバケット名とファイル名を取得
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # logs
    print("bucket naem is: " + bucket)
    print("key is :" + key)
    
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode='ja-JP',
            Media={
                'MediaFileUri':'https://' + bucket + '.s3.ap-northeast-1.amazonaws.com/' + key
            },
            OutputBucketName=output_bucket
        )
        # NOTE: ↓ 動画＋Transcribeの出力を同じS3から取得したいというフロントエンド側の要望に応えるためのコード
        s3.copy_object(
            CopySource={
                'Bucket': bucket,
                'Key': key
            },
            Bucket=output_bucket,
            Key="output-movie2.mp4" # HACK: ここも名前が一意な必要があるのでどうするか
        )
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e