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

# 설정 파일에 따라 엔드포인트 추가
for path, datas in config["projectProgram"].items():
    method = datas["method"].lower()


# python -X utf8 -m uvicorn main:app --port 5580 --reload --host 0.0.0.0 