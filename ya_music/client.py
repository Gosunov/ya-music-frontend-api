import requests
import random
from time import time, sleep

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.3',
    'Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1',
]
    
class Client():
    def __init__(self, session_id):
        self.session_id = session_id
        self.refresh_auth()


    def http_post(self, url, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()
        kwargs['headers']['User-Agent'] = random.choice(user_agents)
        resp = requests.post(url, **kwargs)
        if resp.status_code != 200:
            raise RuntimeError("Yandex music returned %d status code for POST %s" % (resp.status_code, url))
        return resp


    def http_get(self, url, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()
        kwargs['headers']['User-Agent'] = random.choice(user_agents)
        resp = requests.post(url, **kwargs)
        if resp.status_code != 200:
            raise RuntimeError("Yandex music returned %d status code for GET %s" % (resp.status_code, url))
        return resp


    def refresh_auth(self):
        url = 'https://music.yandex.ru/handlers/auth.jsx?external-domain=music.yandex&overembed=no'
        cookies = {
            'Session_id': self.session_id
        }
        resp = self.http_get(url, cookies=cookies)
        body = resp.json()

        self.login = body['user']['login']
        self.sign  = body['user']['sign']
        self.uid   = body['user']['uid']
        self.i_cookie = resp.cookies.get('i')

        if self.i_cookie is None:
            raise RuntimeError("Yandex music did not set i_cookie")


    def get_history(self):
        url = 'https://music.yandex.ru/handlers/library.jsx?owner=%s&filter=history' % self.login
        headers = {
            'Referer': 'https://music.yandex.ru/'
        }
        cookies = {
            'Session_id': self.session_id
        }
        resp = self.http_get(url, headers=headers, cookies=cookies)
        return resp.json()['trackIds']


    def clear_history(self):
        url = 'https://music.yandex.ru/handlers/history-clear.jsx'
        cookies = {
            'Session_id': self.session_id,
            'i': self.i_cookie,
        }
        data = {
            'sign': self.sign,
        }
        self.http_post(url, data=data, cookies=cookies)


    def add_to_history(self, track_id):
        def send_reason(reason):
            position = 0
            if reason == 'end':
                position = 2.063673469387755
            timestamp = int(time() * 1000)
            url = 'https://music.yandex.ru/api/v2.1/handlers/track/%s/web-album_track-album-album-main/feedback/%s?__t=%d' % (track_id, reason, timestamp)
            headers = {
                'Host': 'music.yandex.ru',
                'Referer': 'https://music.yandex.ru/',
                'X-Current-UID': self.uid,
                'X-Yandex-Music-Client': 'YandexMusicAPI',
                'X-Retpath-Y': 'https://music.yandex.ru/',
            }
            cookies = {
                'i': self.i_cookie,
                'Session_id': self.session_id,
            }
            data = {
                'timestamp': timestamp,
                'data': [
                    {
                        'sendReason': reason,
                        'timestamp':  timestamp,
                        'trackId':    track_id.split(':')[0],
                        'album':      int(track_id.split(':')[1]),
                        'restored':   False,
                        'preview':    False,
                        'yaDisk':     False,
                        # TODO?
                        'duration':   2.063673469387755,
                        'position':   position,
                        'played':     position,
                        'playId':     'a46553201b8607e26741aae6f31d2b961b11a0b21:%s:40079980362412815' % track_id.split(':')[0],
                        'context':    'album',
                        'cm':         'pt',
                    }
                ],
                'sign': self.sign,
                'external-domain': 'music.yandex.ru',
                'overembed': 'no',
            }
            resp = self.http_post(url, headers=headers, cookies=cookies, json=data)
            return resp

        send_reason('start')
        sleep(2)
        send_reason('end')
