# 04_json.py
# https://jsonplaceholder.typicode.com/
# posts 정보를 가지고 와서 출력 한다.
# 출력 항목: userId, title, body

import httpx  # FastAPI 같은 백엔드 API에 HTTP 요청을 보내기 위해 httpx 클라이언트를 가져옵니다.

# API_URL = "https://jsonplaceholder.typicode.com/posts"  # 호출할 백엔드 health check API 주소입니다.
API_URL = "http://192.100.200.198:8000/health"  # 호출할 백엔드 health check API 주소입니다.

response = httpx.get(API_URL, timeout=5.0)  # GET 요청을 보내고 응답 객체를 response 변수에 저장합니다.
# [{}, {}]
if response.status_code == 200:
    result = response.json()
    for data in result:
        print(f"{data["userId"]} {data["title"]}")