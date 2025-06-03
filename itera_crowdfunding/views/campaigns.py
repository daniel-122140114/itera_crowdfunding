from pydantic import ValidationError
from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.schemas.campaign import CampaignCreate, CampaignUpdate
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.middleware import auth_required
import json

@view_config(route_name='campaigns',request_method='GET', renderer='json')
def get_campaigns(request):
    res = supabase.table('campaigns').select("id,title,description,type_id,image_url,target_amount,current_amount,status,is_urgent,created_by (id, nik, prodi, email, name, photo_url),created_at").eq('status','approved').order("created_at",desc=True).order('is_urgent').execute()
    return res.data

@view_config(route_name='campaigns', request_method='POST', renderer='json')
@auth_required
def create_campaign(request):
    try:
        body = CampaignCreate(**request.json_body).model_dump()
    except ValidationError as e:
        return Response(status=400, json_body={"errors": e.errors()})
    
    res = supabase.table('campaigns').insert(body).execute()
    return res.data

@view_config(route_name='campaign',request_method="GET", renderer='json')
def get_campaign(request):
    campaign_id = request.matchdict['id']
    res = supabase.table('campaigns').select("id,title,description,type_id,image_url,target_amount,current_amount,status,is_urgent,created_by (id, nik, prodi, email, name, photo_url),created_at").eq("id", campaign_id).execute()
    if res.data:
        return res.data[0]
    return Response(status=404, json_body={'error': 'Not found'})

@view_config(route_name='campaign', request_method='PUT', renderer='json')
@auth_required
def update_campaign(request):
    campaign_id = request.matchdict['id']
    try:
        data = CampaignUpdate(**request.json_body).model_dump(exclude_unset=True)
    except ValidationError as e:
        return Response(status=400, json_body={"errors": e.errors()})

    res = supabase.table('campaigns').update(data).eq("id", campaign_id).execute()
    return res.data

@view_config(route_name='campaign', request_method='DELETE', renderer='json')
@auth_required
def delete_campaign(request):
    campaign_id = request.matchdict['id']
    res = supabase.table('campaigns').delete().eq("id", campaign_id).execute()
    return {"message": "deleted"}
@view_config(route_name="campaign_type",request_method="GET",renderer="json")
def get_campaign_type(request):
    res = supabase.table('campaign_types').select("*").execute()
    return res.data
@view_config(route_name="campaign_request",request_method="GET",renderer="json")
@auth_required
def campaign_request(request):
    res = supabase.table('campaigns').select("id,title,description,type_id,image_url,target_amount,current_amount,status,is_urgent,created_by (id, nik, prodi, email, name, photo_url),created_at").eq('status','pending').order("created_at",desc=True).order('is_urgent').execute()
    return res.data
