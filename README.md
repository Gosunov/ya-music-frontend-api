# Ya-music-frontend-api

Python wrapper for Yandex.Music frontend api for manipulating history

To use this, you need to obtain your `Session_id` cookie from [Yandex.Music](https://music.yandex.ru).

## Example
```py
from ya_music import Client

session_id = 'secret'
client = Client(session_id)

client.get_history()
client.clear_history()
client.add_to_history('2269771:225060')
```

