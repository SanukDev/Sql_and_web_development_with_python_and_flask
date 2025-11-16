import requests

url = f"http://127.0.0.1:5000/random"
response = requests.get(url)
datas = response.json()

print(datas)