# Deleting a post

**Method**: DELETE

## URL format

```/api/news/details/<slug>```

```slug``` - slug of the post

## Example

```python
import requests
import json

URL = "https://diary56.ru/api/"

# Authorization
r = requests.post(URL + 'auth/', {"username": "example@mail.com", "password": "qwerty1234"})
token = json.loads(r.content.decode())['token']
headers = {"Authorization": "Token " + token}

# Delete a post
r = requests.delete(URL + 'news/details/list-of-summer-literature', headers=headers)
```
