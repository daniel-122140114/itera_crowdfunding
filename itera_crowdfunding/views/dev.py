import requests
from pyramid.view import view_config
from pyramid.response import Response
import os
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xyzcompany.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "anon-key")

@view_config(route_name='get_token', request_method='POST', renderer='json')
def get_token(request):
    data = request.json_body
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response(json_body={'error': 'Email and password required'}, status=400)

    url = f'{SUPABASE_URL}/auth/v1/token?grant_type=password'
    headers = {
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json'
    }
    payload = {'email': email, 'password': password}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return Response(json_body={'error': 'Login failed', 'detail': response.json()}, status=401)
