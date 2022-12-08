import boto3
from pathlib import Path
from . import compress

def s3_upload():
    compress.compressor() #encrypted_logs파일을 통해 압축된 로그 파일 생성하고 시작

    #s3 client 생성
    s3 = boto3.client('s3')

    currentpath = str(Path.cwd()) #/Users/orangehour/projects/ETL_pipeline
    bucket_name = 'team-etl-bucket'
    file_name = 'compressed_log.gz'
    file_path = currentpath+'/logs/'+file_name
    
    #변수: 순서대로 로컬 파일명, s3의 버킷명, s3에 저장되는 파일명
    s3.upload_file(file_path, bucket_name, file_name)