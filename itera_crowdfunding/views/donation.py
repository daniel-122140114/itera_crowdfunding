from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.donation import DonationCreate, DonationUpdate
from pydantic import ValidationError
from itera_crowdfunding.middleware import auth_required
@view_config(route_name='donations', request_method='GET', renderer='json')
@auth_required
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
@auth_required
def create_donation(request):
    try:
        donation = DonationCreate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('donations').insert(donation.model_dump()).execute()
    return res.data

@view_config(route_name='donation', request_method='PUT', renderer='json')
@auth_required
def update_donation(request):
    donation_id = request.matchdict['id']
    try:
        update_data = DonationUpdate(**request.json_body)
    except ValidationError as e:
        return Response(status=400, json_body={'errors': e.errors()})
    
    res = supabase.table('donations').update(update_data.model_dump(exclude_unset=True)).eq("id", donation_id).execute()
    return res.data

@view_config(route_name='donation', request_method='DELETE', renderer='json')
@auth_required
def delete_donation(request):
    donation_id = request.matchdict['id']
    supabase.table('donations').delete().eq("id", donation_id).execute()
    return {"message": "deleted"}
@view_config(route_name="get_top_donation",request_method="GET",renderer="json")
def get_top_donation(request):
    res = supabase.table('users').select("*").order('total_donation',desc=True).limit(25).execute()
    return res.data
@view_config(route_name="get_campaign_donations",request_method="GET",renderer="json")
def get_campaign_donation(request):
    campaign_id = request.matchdict['id']
    res = supabase.table('donations').select("id,campaign_id,amount,is_anonymous,message,donor (id,name,prodi,nik,email,photo_url)").order('created_at').eq('campaign_id',campaign_id).execute()
    return res.data
