import hashlib
import os
from cryptography.fernet import Fernet
from pathlib import Path
import datetime
import json

def get_hash(integer):
    salt = os.urandom(32) #binary 값 생성
    #ex)\xa9\x84\x01\x96\xa4\t\xadP\x1e\xf3:\x94[\xb7\x9c=\xfebI\x03\xa2\x05\xd5\x9a\x19\x9b\xabhO\x13\xb8\x83

    #Salted-Hash = SHA256(유저가 입력한 password + salt)

    """
    hashlib.pbkdf2_hmac():
    Returns a binary digest for the PBKDF2 hash algorithm of `data`
    with the given `salt`. It iterates `iterations` times and produces a
    key of `keylen` bytes. By default, SHA-256 is used as hash function;
    a different hashlib `hashfunc` can be provided.

    :param data: the data to derive.
    :param salt: the salt for the derivation.
    :param iterations: the number of iterations.
    :param keylen: the length of the resulting key.  If not provided
                    the digest size will be used.
    :param hashfunc: the hash function to use.  This can either be the
                        string name of a known hash function or a function
                        from the hashlib module.  Defaults to sha256.
    """
    plainstring = str(integer)
    plaintext = plainstring.encode() #encode하고 싶은 문자열을 binary 문자열로 인코딩
    digest = hashlib.pbkdf2_hmac('sha256', plaintext, salt, 10000) #digest 객체는 생성된 해시값을 갖고 있다
    hex_hash = digest.hex()
    return hex_hash #바이트 문자열을 16진수로 변환한 문자열(hex)을 반환


def encrypt(plaintext):
    """
    양방향 암호화를 사용하여 key를 생성 및 별도 파일에 저장하며, 암호화된 데이터를 반환하는 함수
    plaintext: 암호화하려는 데이터(json 형태)
    """
    #logkey.key 파일에서 key값 불러오기
    mod_path = Path(__file__).parent
    absolute_keyfile_path = (mod_path /"./logkey.key").resolve() #resolve: 절대 경로 반환

    my_file = Path(absolute_keyfile_path)
    if my_file.is_file():
        # 'logkey.key' 파일이 존재
        with open(absolute_keyfile_path,'rb') as file:
            key = file.read()
    else:
        #키 생성, 'logkey.key' 파일 생성 및 키값 저장
        key = Fernet.generate_key()
        with open('logkey.key','wb') as file:
            file.write(key)
    
    fernet = Fernet(key)
    json_log = plaintext
    encrypt_str = fernet.encrypt(f"{json_log}".encode('ascii'))
    # decrypt_str = fernet.decrypt(encrypt_str)
    return encrypt_str

def update_file():
    """
    로그 파일에 로그가 추가될 때마다 해당 내용을 가져와서 암호화된 내용을 별도 파일에 저장하는 함수
    """
    #로그 파일 읽어오기
    mod_path = Path(__file__).parent
    absolute_logfile_path = (mod_path /"../logs/board_logging.log").resolve()

    #로그 파일의 마지막 줄 읽어오기
    with open(absolute_logfile_path, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()

    #데이터 생성하기
    data = encrypt(last_line).decode('utf8')
    current_time = datetime.datetime.now()
    timestamp_now = current_time.timestamp()

    encrypted = {}
    encrypted["data"] = data
    encrypted["current_time"] = timestamp_now

    json_val = json.dumps(encrypted)
    newLogfile_path = Path(absolute_logfile_path).parent
    newLogfile_path = (newLogfile_path /"encrypted_log.json").resolve() #logs 폴더에 저장

    #this writes your new, encrypted data into a new JSON file
    with open(newLogfile_path, 'a') as file:
        file.write(json_val)

update_file()