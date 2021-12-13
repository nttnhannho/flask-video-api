import requests


BASE = "http://127.0.0.1:5000/"

data = [{"title": "Video 1", "views": 1111, "likes": 10},
        {"title": "Video 2", "views": 2222, "likes": 20},
        {"title": "Video 3", "views": 3333, "likes": 30}]

for i, element in enumerate(data, start=1):
    response = requests.put(BASE + "video/" + str(i), element)
    print(response.json())

input()
response = requests.get(BASE + "video/1")
print(response.json())
response = requests.get(BASE + "video/2")
print(response.json())
response = requests.get(BASE + "video/3")
print(response.json())
response = requests.get(BASE + "video/100")
print(response.json())

input()
response = requests.patch(BASE + "video/1", {"views": 9999, "likes": 8888})
print(response.json())

input()
response = requests.delete(BASE + "video/1")
print(response)