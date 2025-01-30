from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable, Dict
import logging
import json

# 설정 파일 읽기
with open('config.json') as f:
    config = json.load(f)

app = FastAPI(
    title=config["projectDescript"]["title"],
    description=config["projectDescript"]["description"],
    version=config["projectDescript"]["version"],
    terms_of_service=config["projectDescript"]["terms_of_service"],
    contact=config["projectDescript"]["contact"],
    license_info=config["projectDescript"]["license_info"],
)

# 핸들러 함수 정의
async def read_root():
    return {"message": "Hello World"}

async def read_item(item_id: int):
    return {"item_id": item_id}

# 핸들러 맵
handler_map: Dict[str, Callable] = {
    "read_root": read_root,
    "read_item": lambda item_id: {"item_id": item_id}
}

'''
# 설정 파일에 따라 엔드포인트 추가
for endpoint in config["endpoints"]:
    path = endpoint["path"]
    method = endpoint["method"].lower()
    handler_name = endpoint["handler"]
    handler = handler_map.get(handler_name)
    params = endpoint["params"]
    
    if handler:
        if method == "get":
            app.get(path)(handler)
        elif method == "post":
            app.post(path)(handler)
        elif method == "put":
            app.put(path)(handler)
        elif method == "delete":
            app.delete(path)(handler)
        # 필요한 경우 다른 HTTP 메서드도 추가 가능
    else:
        raise ValueError(f"Handler '{handler_name}' not found")
'''
'''
# 설정 파일에 따라 엔드포인트 추가
valid_methods = {"get", "post", "put", "delete", "patch", "options", "head", "trace"}   # FastAPI 에서 지원하는 메소드
for path, datas in config["projectProgram"].items():
    method = datas["method"].lower()
    #app.get(path)(handler)
    
    if method in valid_methods:getattr(app, method)(path)(handler)
    else:raise ValueError(f"Invalid HTTP method: invalid_method")    

'''

@app.get("/",summary="모든 아이템 조회",description="이 API는 데이터베이스에서 모든 아이템을 가져옵니다.")
def read_root():
    return {"Hello": "World"}

#handler = handler_map.get("read_item")
#handler = lambda item_id: {"item_id": item_id}
handler = lambda item_id,item_name,item_ea: {"item_id": item_id,"item_name": item_name,"item_ea": item_ea}
print(handler)
method="get"
getattr(app, method)("/aaa")(handler)


func_dict = {
    "name": "_bbb_ccc",
    "param": "x,y",
    "expression": "(x+y) * 2"
}

# 함수 코드 생성
func_code = f"""
def {func_dict['name']}({func_dict['param']}):
    return {func_dict['expression']}
"""

# exec()로 함수 동적 생성
exec(func_code, globals())  # globals()를 사용하면 전역에서 사용 가능

# 생성된 함수 호출
#print(custom_function(5,1))  # 10

getattr(app, method)("/bbb")(_bbb_ccc)



# python -X utf8 -m uvicorn main:app --port 5580 --reload --host 0.0.0.0 