# Getting post details

**Method**: GET

## URL format

```/api/news/<slug>```

```slug``` - slug of the post

## JSON format

```json
{
    "date": "2020-06-02T16:33:55.631140+03:00",
    "title": "Список литературы на лето",
    "author": "Admin",
    "content": "Очееень длинный список...",
    "slug": "list-of-summer-literature",
    "image": "https://diary56.ru/media/news/book-shielf.png"
}
```

## Fields

```date``` - *string* - date and time of post creation, in ISO 8601 format (*YYYY-MM-DDThh:mm:ss.ssssssTZD*)  
```title``` - *string* - title of the post  
```author``` - *string* - author of the post  
```content``` - *string* - content of the post (in markdown)  
```slug``` - *string* - slug of the post  
```image``` - *string* - link to an image of the post

## Example

```python
import requests
import json
import pprint

URL = "https://diary56.ru/api/"

# Authorization
r = requests.post(URL + 'auth/', {"username": "example@mail.com", "password": "qwerty1234"})
token = json.loads(r.content.decode())['token']
headers = {"Authorization": "Token " + token}

# Getting news
r = requests.get(URL + 'news/list-of-summer-literature', headers=headers)
pprint.pprint(json.loads(r.content.decode()), indent=4)
```
