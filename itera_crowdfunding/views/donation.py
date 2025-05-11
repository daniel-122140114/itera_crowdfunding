from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.donation import DonationCreate, DonationUpdate
from pydantic import ValidationError

@view_config(route_name='donations', request_method='GET', renderer='json')
def get_donations(request):
    res = supabase.table('donations').select("*").execute()
    return res.data

@view_config(route_name='donation', request_method='GET', renderer='json')
def get_donation(request):
    donation_id = request.matchdict['id']
    res = supabase.table('donations').select("*").eq("id", donation_id).execute()
    if res.data:
        return res.data[0]
    return Response(status=404, json_body={'error': 'Not found'})

@view_config(route_name='donations', request_method='POST', renderer='json')
def create_donation(request):
    try:
        donation = DonationCreate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('donations').insert(donation.model_dump()).execute()
    return res.data

@view_config(route_name='donation', request_method='PUT', renderer='json')
def update_donation(request):
    donation_id = request.matchdict['id']
    try:
        update_data = DonationUpdate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('donations').update(update_data.model_dump(exclude_unset=True)).eq("id", donation_id).execute()
    return res.data

@view_config(route_name='donation', request_method='DELETE', renderer='json')
def delete_donation(request):
    donation_id = request.matchdict['id']
    supabase.table('donations').delete().eq("id", donation_id).execute()
    return {"message": "deleted"}
