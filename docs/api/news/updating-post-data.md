# Updating post data

**Method**: PUT

## URL format

```/api/news/<slug>```

```slug``` - slug of the post

## Data format

```json
{
    "title": "Список литературы на лето",
    "author": "Admin",
    "content": "Очееень длинный список...",
    "slug": "list-of-summer-literature",
    "image": "https://diary56.ru/media/news/book-shielf.png"
}
```

## Fields

```title``` - *string* - title of the post  
```author``` - *string* - author of the post  
```content``` - *string* - content of the post (in markdown)  
```slug``` - *string* - slug of the post  
```image``` - *string* - link to an image of the post

## Example

```python
import requests
import json

URL = "https://diary56.ru/api/"

# Authorization
r = requests.post(URL + 'auth/', {"username": "example@mail.com", "password": "qwerty1234"})
token = json.loads(r.content.decode())['token']
headers = {"Authorization": "Token " + token}

# Getting news
r = requests.put(URL + 'news/details/list-of-summer-literature', headers=headers, data={
    "title": "Post title but changed",
    "author": "Happy API User",
    "content": "Interesting text",
    "slug": "list-of-summer-literature",
})
```
