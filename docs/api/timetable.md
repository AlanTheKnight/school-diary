# Timetable

## Getting a timetable

### URL format

```/api/timetable/<letter>/<number>/```

```letter``` - a cyrillic letter from ```А``` to ```И```  
```number``` - a number from ```1``` to ```11```

### JSON Format

```json
[
    {
        "weekday": "Понедельник",
        "lessons": [
            {
                "number": {
                    "n": 1,
                    "start": "09:00:00",
                    "end": "09:40:00"
                },
                "subject": "Русский язык",
                "classroom": "205"
            },
        ]
    },
]
```

### Fields

```weekday``` - *string* - a weekday  
```lessons``` - *list* - a list of lessons on this weekday

**Lessons**:  
```number``` - *int* - time when the lesson starts and it's index
```subject``` - *string* - a subject of the lesson  
```classroom``` - *string* - a classroom where the lesson is held

**Number**:  
```n``` - *int* - index of the lesson  
```start``` - *string* - start of the lesson in HH:MM:SS format  
```end``` - *string* - end of the lesson in HH:MM:SS format

**Notes**:  
```weekday``` field also contains ```today``` and ```tomorrow``` values which automatically
show lessons for today & tomorrow.  
```lessons``` field is an empty list if there are no lessons for this weekday.  
```classroom``` field's type is not *int* because it may not only contain a number of
classroom but also values like ```Физкультурный зал``` or ```АЦТ```.

### Example

```python
import requests
import json
import pprint

URL = "https://diary56.ru/api/"

# Authorization
r = requests.post(URL + 'auth/', {"username": "example@mail.com", "password": "qwerty1234"})
token = json.loads(r.content.decode())['token']
headers = {"Authorization": "Token " + token}

# Getting timetable
r = requests.get(URL + 'timetable/8/З/', headers=headers)
pprint.pprint(json.loads(r.content.decode()), indent=4)
```
