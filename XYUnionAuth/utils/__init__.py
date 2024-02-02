import jwt
import os
from typing import Union, Dict

def verify_token(token: str) -> Union[Dict[str, str], None]:
    try:
        decoded_token = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    return decoded_token