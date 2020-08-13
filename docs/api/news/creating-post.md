# Creating a post

**Method**: POST

## URL format

```/api/news/create/```

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

# Create a post
r = requests.post(URL + 'news/create/', headers=headers, data={
    "title": "A new post",
    "author": "Happy API User",
    "content": "Interesting text",
    "slug": "a-new-post",
})
```
