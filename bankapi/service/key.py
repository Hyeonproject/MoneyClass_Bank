'''
json key 값을 가져오는 기능
'''
import json

with open('key.json') as f:
    key = json.loads(f.read())

def get_key(setting, key=key):
    '''비밀 변수 가져오기'''
    try:
        return key[setting]
    except KeyError:
        error_msg = '{0}의 데이터가 없습니다.'.format(setting)
        KeyError(error_msg)

url = 'mysql://{}:{}@{}:{}/{}'.format(get_key('db_user'), get_key('db_password'),
                                      get_key('db_host'), get_key('db_port'),
                                      get_key('db_name'))