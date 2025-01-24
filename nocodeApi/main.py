from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable, Dict

import json

app = FastAPI(
    title="My Custom API",
    description="This is a custom API built with FastAPI.",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# 설정 파일 읽기
with open('config.json') as f:
    config = json.load(f)

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


# python -m uvicorn main:app --port 5580 --reload --host 0.0.0.0 