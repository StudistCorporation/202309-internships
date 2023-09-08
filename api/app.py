from flask import Flask, request, jsonify
from boto3 import client

aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'

app = Flask(__name__)

@app.route('/manuals', methods=['GET'])
def get_manuals():
    """Get all manuals in the bucket"""
    # NOTE: マニュアル動画と文字起こしスクリプトを格納するS3を用意できた場合のエンドポイント
    
    bucket_name = 'manuals-bucket' # 仮置き
    
    s3 = client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key) 
    
    response = s3.list_objects_v2(Bucket=bucket_name)
    manuals = []
    
    for manual in response['Contents']:
        manuals.append(manual['Key'])
        print(manual['Key'])
    
    return jsonify({'manuals_keys': manuals})

@app.route('/upload', methods=['POST'])
def upload_manual():
    """Upload a manual to the bucket"""
    # NOTE: ユーザが撮影した動画格納するためのS3を用意できた場合のエンドポイント 
    
    bucket_name = 'upload-bucket' # 仮置き
    
    s3 = client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    file = request.files['file']
    
    s3.upload_fileobj(file, bucket_name, file.filename)
    
    return jsonify({'message': 'success to upload'})
