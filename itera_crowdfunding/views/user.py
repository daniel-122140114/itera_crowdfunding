from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.user import UserCreate, UserUpdate
from pydantic import ValidationError
from itera_crowdfunding.middleware import auth_required

@view_config(route_name='users', request_method='GET', renderer='json')
def get_users(request):
    res = (
        supabase
        .table('users')
        .select("*")
        .execute()
    )
    return res.data

@view_config(route_name='user', request_method='GET', renderer='json')
def get_user(request):
    user_id = request.matchdict['id']
    res = supabase.table('users').select("*").eq("id", user_id).execute()
    if res.data:
        return res.data[0]
    return Response(status=404, json_body={'error': 'Not found'})

@view_config(route_name='users', request_method='POST', renderer='json')
def create_user(request):
    try:
        user = UserCreate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('users').insert(user.model_dump()).execute()
    return res.data

@view_config(route_name='user', request_method='PUT', renderer='json')
@auth_required
def update_user(request):
    user_id = request.matchdict['id']
    try:
        update_data = UserUpdate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('users').update(update_data.model_dump(exclude_unset=True)).eq("id", user_id).execute()
    return res.data

@view_config(route_name='user', request_method='DELETE', renderer='json')
@auth_required
def delete_user(request):
    user_id = request.matchdict['id']
    supabase.table('users').delete().eq("id", user_id).execute()
    return {"message": "deleted"}
