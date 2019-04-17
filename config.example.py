# -*-- coding:utf-8 -*--
import random
import TLSSigAPI

from cache import FileCache


sdk_app_id = 1
identifier = ''
random = random.randint(10000, 99999)
content_type = 'json'
get_history_url = 'https://console.tim.qq.com/v4/open_msg_svc/get_history'

private_key_path = 'D:\\work\\party-api\\vendor\\party\\party-config\\env\\stable\\qcloud\\private_key'
public_key_path = 'D:\\work\\party-api\\vendor\\party\\party-config\\env\\stable\\qcloud\\public_key'


cache_handle = FileCache('./signature')
if cache_handle.exist():
    user_sig = cache_handle.get()
else:
    with open(private_key_path, 'r') as f:
        private_key = f.read()
        f.close()

    with open(public_key_path, 'r') as f:
        public_key = f.read()
        f.close()

    api = TLSSigAPI.TLSSigAPI(sdk_app_id, private_key, public_key)
    user_sig = api.gen_sig(identifier)
    cache_handle.set(user_sig)
