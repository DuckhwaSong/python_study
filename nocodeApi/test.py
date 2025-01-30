import json
import pymysql
import datetime

# MySQL 연결 설정
connection = pymysql.connect(
    host="localhost",
    user="db_user",
    password="db_user_pass",
    database="app_db",
    port=3366,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 반환
)


# 설정 파일 읽기
with open("config.json", "r") as configFile:
    config = json.load(configFile)

# 쿼리 함수 정의
def sqlQuery(connection,sql,bind):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, bind)  # 쿼리 실행, 매개변수는 튜플로 전달
            result = cursor.fetchall()  # 결과 가져오기
    except TypeError:return {}
    idx=0
    for data in result:
        for key, val in data.items():
            # datetime 자료형을 Y-m-d H:i:s 형태로 변환
            if isinstance(val, datetime.datetime):result[idx][key]=val.strftime("%Y-%m-%d %H:%M:%S")
        idx+=1
    return result

# print(config)

# 설정 파일에 따라 엔드포인트 추가
for path, datas in config["projectProgram"].items():
    method = datas["method"].lower()  
    #process = datas["process"].lists()
    #print(process)
    # 프로세스 반복문
    for process in datas["process"]:
        for variable,processData in process.items():
            try:type = processData["type"]
            except TypeError:type = "sql"
            print(variable + ">>" + type)

            if type == "sql":
                result = sqlQuery(connection,processData["sql"],[1])
                print(result)
    print(path)
    print(method)

#> python -X utf8 test.py