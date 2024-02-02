import django
import json
import XYUnionAuth.utils as utils
import os
import pymongo
from django.http import HttpRequest, HttpResponse, JsonResponse
from bson.json_util import dumps

db = pymongo.MongoClient(os.environ['MONGODB_URI']).get_default_database()


def policies(request: HttpRequest):
    token = json.loads(request.body).get('token', None)

    # 检查参数完整
    if token is None:
        return JsonResponse({'error': 'Missing token'}, status=400)

    # 检查token合法性
    if utils.verify_token(token) is None:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    # 增删改查
    if request.method == 'GET':
        # 鉴权
        if not utils.check_permission(token, 'polices', 'read'):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        return JsonResponse({
            'polices': utils.enforcer.get_policy()
        })
    elif request.method == 'POST':
        # 鉴权
        if not utils.check_permission(token, 'polices', 'write'):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)
        utils.enforcer.add_policy(*data['policy'])

        return JsonResponse({'success': 'Policy added'})
    elif request.method == 'DELETE':
        # 鉴权
        if not utils.check_permission(token, 'polices', 'write'):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)

        utils.enforcer.remove_policy(*data['policy'])

        return JsonResponse({'success': 'Policy deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=400)


def check_permission(request: HttpRequest):
    data = json.loads(request.body)

    token = data.get('token', None)
    resource = data.get('resource', None)
    action = data.get('action', None)
    environment_params = data.get('environment_params', {})

    # 检查参数完整性
    if token is None or resource is None or action is None:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    return JsonResponse({'result': utils.check_permission(token, resource, action, environment_params)})
