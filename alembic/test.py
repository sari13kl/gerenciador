import requests
import traceback

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzY3NDU2ODI1fQ.NVLJFlwvOFmK4JvonapPpUwZEUdsIne0V5JSwdiMofQ"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
try:
    print(requisicao)
    print(requisicao.json())
except Exception:
    traceback.print_exc()
    raise