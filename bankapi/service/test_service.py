"""
테스트 할떄 중복되는 부분을 함수로 만들어 봅니다.
"""

def jwt_make(token_data):
    return {'Authorization': 'Bearer {}'.format(token_data)}