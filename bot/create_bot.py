import requests
from datetime import datetime 
import random
# 원하는 만큼의 봇계정 생성
def create_bot(num):

    # 봇 생성 숫자 조절

    for i in range(4,num+1):
        bot_form = {
            "email": f"bot{i}@bot.com",
            "nickname" : f"bot{i}",
            "gender" : random.choice(['M','F']),
            "password" : "iambot4084",
            "password2" : "iambot4084", 
            "name" : f"bot{i}",
            "birth_date" : datetime.today().strftime("%Y-%m-%d"),
        }
        response = requests.post("http://127.0.0.1:8000/user/signup/", json=bot_form)


    return  f"{num}개의 bot accounts 생성 complete"









if __name__ == '__main__':
    # 원하는 bot 개수 입력
    create_bot(10)