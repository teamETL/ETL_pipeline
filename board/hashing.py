import hashlib
import os

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

# #log file을 json 라이브러리를 이용하여 받아오기
# import json
# from pathlib import Path

# mod_path = Path(__file__).parent
# absolute_logfile_path = (mod_path /"../logs/board_logging.log").resolve() #resolve: 절대 경로 반환


# # 로그 파일 읽어오기
# data_list = []

# with open(absolute_logfile_path, 'r') as file:
#     while True:
#         # Get next line from file
#         line = file.readline()
#         line = json.loads(line)
#         data_list.append(line)
#         # if line is empty
#         # end of file is reached
#         if not line:
#             break

# # print(data_list)
# first_dict = data_list[0]
# print(first_dict)

# # 데이터 수정
# data["Olivia"]["age"] = 26
# data["Olivia"]["hobby"].append("take a picture")
# data["Tyler"]["age"] = 29
# data["Tyler"]["hobby"].append("travel")

# # 기존 json 파일 덮어쓰기
# with open(file_path, 'w', encoding='utf-8') as file:
#     json.dump(data, file, indent="\t")
