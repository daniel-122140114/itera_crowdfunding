from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.transaction import TransactionCreate, TransactionUpdate
from pydantic import ValidationError

@view_config(route_name='transactions', request_method='GET', renderer='json')
def get_transactions(request):
    res = supabase.table('transactions').select("*").execute()
    return res.data

@view_config(route_name='transaction', request_method='GET', renderer='json')
def get_transaction(request):
    transaction_id = request.matchdict['id']
    res = supabase.table('transactions').select("*").eq("id", transaction_id).execute()
    if res.data:
        return res.data[0]
    return Response(status=404, json_body={'error': 'Not found'})

@view_config(route_name='transactions', request_method='POST', renderer='json')
def create_transaction(request):
    try:
        transaction = TransactionCreate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('transactions').insert(transaction.model_dump()).execute()
    return res.data

@view_config(route_name='transaction', request_method='PUT', renderer='json')
def update_transaction(request):
    transaction_id = request.matchdict['id']
    try:
        update_data = TransactionUpdate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('transactions').update(update_data.model_dump(exclude_unset=True)).eq("id", transaction_id).execute()
    return res.data

@view_config(route_name='transaction', request_method='DELETE', renderer='json')
def delete_transaction(request):
    transaction_id = request.matchdict['id']
    supabase.table('transactions').delete().eq("id", transaction_id).execute()
    return {"message": "deleted"}
