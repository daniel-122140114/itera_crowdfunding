from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.withdrawal import WithdrawalCreate, WithdrawalUpdate
from pydantic import ValidationError
from itera_crowdfunding.middleware import auth_required

@view_config(route_name='withdrawals', request_method='GET', renderer='json')
@auth_required
def get_withdrawals(request):
    res = supabase.table('fund_withdrawals').select("id,amount,withdrawal_date,status,created_at,created_by (id,nik,prodi,name,email,photo_url)").execute()
    return res.data

@view_config(route_name='withdrawal', request_method='GET', renderer='json')
@auth_required
def get_withdrawal(request):
    withdrawal_id = request.matchdict['id']
    res = supabase.table('fund_withdrawals').select("*").eq("id", withdrawal_id).execute()
    if res.data:
        return res.data[0]
    return Response(status=404, json_body={'error': 'Not found'})

@view_config(route_name='withdrawals', request_method='POST', renderer='json')
@auth_required
def create_withdrawal(request):
    try:
        withdrawal = WithdrawalCreate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('fund_withdrawals').insert(withdrawal.model_dump()).execute()
    return res.data

@view_config(route_name='withdrawal', request_method='PUT', renderer='json')
@auth_required
def update_withdrawal(request):
    withdrawal_id = request.matchdict['id']
    try:
        update_data = WithdrawalUpdate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('fund_withdrawals').update(update_data.model_dump(exclude_unset=True)).eq("id", withdrawal_id).execute()
    return res.data

@view_config(route_name='withdrawal', request_method='DELETE', renderer='json')
@auth_required
def delete_withdrawal(request):
    withdrawal_id = request.matchdict['id']
    supabase.table('fund_withdrawals').delete().eq("id", withdrawal_id).execute()
    return {"message": "deleted"}
