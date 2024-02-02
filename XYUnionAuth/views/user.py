import os
import json
import pymongo
import jwt
import django
from django.http import HttpResponse, JsonResponse, HttpRequest
import XYUnionAuth.utils as utils

db = pymongo.MongoClient(os.environ['MONGODB_URI']).get_default_database()


def login(request: HttpRequest):
    if request.method == 'POST':
        username = json.loads(request.body).get('username', None)
        password = json.loads(request.body).get('password', None)

        # 验证参数是否齐全
        if username is None or password is None:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        # 验证用户密码
        result = db['users'].find_one(
            {'username': username, 'password': password})
        if result:
            # 抹除 password 和 _id
            del result['password'], result['_id']

            # 生成 token
            token = jwt.encode(
                result,
                os.environ['SECRET_KEY'],
                algorithm='HS256',
                headers={
                    'expiresIn': '14d'
                }
            )
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

        # 成功
        return JsonResponse({
            'success': True,
            'user': {
                'username': result['username'],
                'email': result['email'],
                'avatar': result['avatar']
            },
            'token': token
        })
    else:
        return JsonResponse({'error': 'Method not allow'}, status=400)

def register(request: HttpRequest):
    if request.method == 'POST':
        username = json.loads(request.body).get('username', None)
        password = json.loads(request.body).get('password', None)
        email = json.loads(request.body).get('email', None)
        avatar = json.loads(request.body).get('avatar', None)

        # 验证数据完整性
        if username is None or password is None or email is None or avatar is None:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)

        # 验证用户名是否已存在
        if db['users'].find_one({'username': username}):
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # 添加用户
        db['users'].insert_one({
            'username': username,
            'password': password,
            'email': email,
            'avatar': avatar
        })

        # 返回结果
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Method not allow'}, status=400)

def verify_token(request: HttpRequest):
    token = json.loads(request.body).get('token', None)
    
    if token is None:
        return JsonResponse({'error': 'Invalid token'})

    result = utils.verify_token(token)
    
    if result is None:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    else:
        return JsonResponse(result)