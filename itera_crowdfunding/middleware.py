
from jose import jwt
from pyramid.httpexceptions import HTTPUnauthorized
import os
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET","SECRET")
SUPABASE_JWT_ALGORITHM = 'HS256'

def auth_required(handler):
    def wrapper(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPUnauthorized(json_body={"error": "Authorization header missing or invalid"})

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[SUPABASE_JWT_ALGORITHM],options={"verify_aud":False})
            request.user = payload  # inject user info ke request
        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized(json_body={"error": "Token expired"})
        except jwt.JWTError as e:
            raise HTTPUnauthorized(json_body={"error": "Token invalid","message" : f"{str(e)}"})
        return handler(request)
    return wrapper