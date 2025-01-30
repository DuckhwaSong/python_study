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

def sqlProcess(obj,context):
    return context


# print(config)
'''
# 설정 파일에 따라 엔드포인트 추가
for path, datas in config["projectProgram"].items():
    method = datas["method"].lower()  
    #process = datas["process"].lists()
    #print(process)

    # 프로세스 반복문
    for process in datas["process"]:
        for var_name,processData in process.items():
            try:type = processData["type"]
            except TypeError:type = "sql"
            print(var_name + ">>" + type)

            if type == "sql":
                locals()[var_name] = sqlQuery(connection,processData["sql"],[1])
                print(locals()[var_name])
    print(path)
    print(method)
'''

# 람다 함수를 위한 선언
func_dict = {"param": "x,y","expression": "(x+y) * 2"}

# param과 expression을 사용하여 문자열로 함수 코드 생성
func_code = f"lambda {func_dict['param']}: {func_dict['expression']}"

# eval()을 사용하여 문자열을 lambda 함수로 변환
func = eval(func_code)

print(func(5,1))  # 12


# 함수를 위한 선언
func_dict = {"name": "custom_function","param": "x,y","expression": "(x+y) * 2"}

# 함수 코드 생성
func_code = f"""
def {func_dict['name']}({func_dict['param']}):
    return {func_dict['expression']}
"""

# exec()로 함수 동적 생성
exec(func_code, globals())  # globals()를 사용하면 전역에서 사용 가능

# 생성된 함수 호출
print(custom_function(5,1))  # 10


# 함수 코드 생성
func_code2 = f"""
def read_root():
    return {{'Hello': 'World'}}
"""

# exec()로 함수 동적 생성
exec(func_code2, globals())

# 생성된 함수 호출
print(read_root())  # 실제 함수 실행 결과 출력



def funcMaker(func_name, param, expression):
    # 함수 코드 생성
    func_code = f"""
def {func_name}({param}):
    return {expression}
"""
    # exec()로 함수 동적 생성 (globals()에 함수가 제대로 등록됨)
    exec(func_code, globals())

funcMaker("plusfunc", "x,y", "(x + y) * 2")

# 생성된 함수 호출
print(plusfunc(5, 1))  # 실제 함수 실행 결과 출력


#> python -X utf8 test.py