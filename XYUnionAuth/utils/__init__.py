import jwt
import os
import pymongo
import casbin
import casbin_pymongo_adapter
from typing import Union, Dict


def verify_token(token: str) -> Union[Dict[str, str], None]:
    try:
        decoded_token = jwt.decode(
            token, os.environ['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    return decoded_token


def check_permission(token: str, resource: str, action: str, environment_params: dict = {}) -> bool:
    adapter = casbin_pymongo_adapter.Adapter(
        os.environ['MONGODB_URI'], os.environ['DATABASE_NAME'], 'polices')

    enforcer = casbin.Enforcer('casbin/abac_module.conf', adapter)

    decoded_token = verify_token(token)

    if decoded_token is None:
        return False

    request = {**decoded_token, **environment_params}
    enforcer.adapter.load_policy()

    return enforcer.enforce(request, resource, action)
