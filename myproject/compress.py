import gzip
from pathlib import Path
import pathlib

def compressor():
    #압축할 로그파일 경로 생성
    logfile_path = Path.cwd()/'logs'/'encrypted_log.json'
    logfile_path = logfile_path.resolve() #절대경로 반환

    compressfile_path = Path.cwd()/'logs'/'compressed_log.gz'

    with open(logfile_path,'rb') as f_in:
        with gzip.open(compressfile_path,'wb') as f_out:
            f_out.writelines(f_in)  # ./logs/compressed_log.gz 압축 파일 생성


