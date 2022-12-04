# ETL_pipeline

참여자 : 민경도, 홍석원

작업 기록 : [ETL pipeline Design project : MinGyeongdo](https://obvious-rock-3e1.notion.site/4ea3e327799245ddb5eed70a928384a9?v=d8678130ea7e45bba84ace509e8f2d6a)

# Django Rest Framework(DRF)를 활용한 ETL 파이프라인 구축

## 로그 암호화 기능 동작 방식

기본 전제: hashing.py의 get_hash() 함수는 로그에 포함된 user_id 값의 해싱을 진행하며, encrypt()와 update_file()은 개별 로그 전체의 암호화를 진행한다. 

개별 로그 예시:
```
{"user_id": "f6fe460b82be7a3affa50936c6fe22a1b081c826ed38e80305ccf88a437a01cc", "board_id": 5, "message": "DELETE content success", "method": "DELETE", "url": "/blog/5/", "levelname": "INFO", "filename": "views.py", "pathname": "/Users/orangehour/projects/ETL_pipeline/board/views.py", "environment": "DjangoRestFramework", "time": "2022-12-04T15:50:52.40Z"}
```

1. views.py에서 logger가 동작하면 (create, put, delete 시에) 개별 로그 값이 생성되며, 이때 board_logging.log에 user_id값이 해싱된 채로 저장된다.
    * user_id 값의 암호화에는 SHA256 방식을 적용했으며, salt를 임의로 생성하여 중복 해시 값의 생성을 방지하였다.
2. views.py에서 update_file()함수가 호출되면 board_logging.log에 있는 마지막 줄을 불러와 암호화를 진행한다.
    * 대칭키 암호화 방식을 이용하였으며, logkey.key 파일이 없으면 새로 생성하여 복호화에 필요한 key값을 저장한다. 이미 존재한다면 logkey.key 파일의 key값을 불러와서 생성하며, board_logging.log의 개별 로그값에 대해서는 모두 같은 key값으로 암호화를 진행한다.
3. 암호화가 완료된 값에 대해서는 encrypted_log.json 파일에 저장한다.
    * recordId 값은 UUID를 이용하여 랜덤하지만 중복되지 않는 값으로 생성된다.
    * ArrivalTimestamp의 경우 board_logging.log의 기록된 개별 로그의 생성 시간을 epoch time으로 변환한 값이다.

암호화 완료된 로그 예시:
```
{
    "recordId": 209706300351001085499519293317723511376,
    "ArrivalTimestamp": 1670169052.4,
    "data": "gAAAAABjjENM6bGvjK-nbcVlTGhKB91-myJIyOkzicCthC-HrlPfygaRPWAA_4x-Di7aHMiJCi-OXHBQ7oXuxHqIPK7ONQ5cL-xnrEQSjbuwCL5oWFOueNnzbsPGnJU7ZfbHlEexv9kE9a0SThhMzwtjwqLA1Km-M9JVGDofm9EG_rUv4abAcbPu-o8isvJY2oi3ONcMB2jspsQw_Vo4HXSgc38lkPuwSM2WpyToXKIfuhr7zVA3Tx1RRFwBoH_iAFsMpLLV6G-qjI_6pdGfktk_y4MvzFyxkjjAMEgLN1LYhxG-xCnGwTLtNnmuKXYl8wqEaxkvU6RNcovA8MX7j_GjixJ-E98O4Cdqg5sEQ_7rWlIgDdEYyQgIsXzCvp9UhVPwgZ2PR5u1iqeVF5FJSQrClkH1-4p9GALJ_DwdXOWoOYwiG68eZ5is_ghhCRc_atDRjjfReHQceJXgT_rUqzRAYO7IZ2HgVvhVSpVgzxFo8OUZ1lXQvWTLFOkFJiUHceIaLGhAnNeV0WEyTNqSidhRngBOphGE3jyzUxXPppH3pUPZtJRcgq8="
},
```