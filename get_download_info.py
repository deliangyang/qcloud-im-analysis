# -*-- coding:utf-8 -*--
import requests
from config import *
import json
import gzip
import time
import pprint

from cache import FileCache


class QCloudImDownloader:
    __slots__ = ('query', 'count')

    def __init__(self, query):
        self.query = query
        self.count = 0

    def parse_url(self):
        _query = []
        for key in self.query:
            _query.append('%s=%s' % (key, self.query[key]))
        return get_history_url + '?' + '&'.join(_query)

    def get_download_urls(self, body_content):
        url = self.parse_url()
        req = requests.post(url=url, data=body_content)
        resp = req.json()
        return self.__parse(resp)

    def download(self, date, type):
        params = json.dumps({
            "ChatType": type,
            "MsgTime": date
        })
        (md5, url) = self.get_download_urls(params)
        resp = requests.get(url)
        filename = './data/%s.gz' % md5
        file_flag = FileCache(filename, 'b')
        if not file_flag.exist():
            file_flag.set(resp.content)

        with gzip.open(filename, 'rb') as fp:
            cnt = -1
            for line in fp:
                line = line.strip().rstrip(b',')
                if line == b']}':
                    break
                if cnt < 0:
                    info = json.loads(line + b']}')
                    print('info: ', info)
                else:
                    msg = json.loads(line)
                    self.raw_print(msg)
                cnt += 1

    def raw_print(self, content):

        _content = json.loads(content['MsgBody'][0]['MsgContent']['Data'])
        if _content['action'] == 'ROOM_OTHER_USER_ENTER' and content['To_Account'] == '11264921':
            print('[%s] %s=>%s:' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(content['MsgTimestamp'] + 3600 * 8)),
                content['From_Account'],
                content['To_Account'],
            ))
            pprint.pprint(content)
            self.count += 1
            pprint.pprint(_content)
        print('count: %d\n' % self.count)

    def __parse(self, data):
        try:
            if len(data['File']) > 0:
                file = data['File'].pop()
                return file['GzipMD5'], file['URL']
            return '', ''
        except Exception as e:
            print(data)
            raise e


if __name__ == '__main__':
    query = {
        'sdkappid': sdk_app_id,
        'identifier': identifier,
        'usersig': user_sig,
        'random': random,
        'apn': 1,
        'contenttype': 'json',
    }

    downloader = QCloudImDownloader(query)
    downloader.download('2019062416', 'C2C')
