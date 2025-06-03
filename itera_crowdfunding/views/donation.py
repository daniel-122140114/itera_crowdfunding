from pyramid.view import view_config
from pyramid.response import Response
from itera_crowdfunding.schemas.campaign import CampaignUpdate
from itera_crowdfunding.supabase_client import supabase
from itera_crowdfunding.schemas.donation import DonationCreate, DonationUpdate
from pydantic import ValidationError
from pyramid.settings import asbool
from pyramid.httpexceptions import HTTPBadRequest
from midtransclient import Snap
from pyramid.httpexceptions import HTTPBadRequest
from uuid import uuid4
from itera_crowdfunding.schemas.transaction import TransactionCreate,TransactionUpdate
from datetime import datetime

from itera_crowdfunding.middleware import auth_required
@view_config(route_name='donations', request_method='GET', renderer='json')
@auth_required
def get_donations(request):
    res = supabase.table('donations').select("id,amount,is_anonymous,message,status,campaign(id,title,description,image_url,target_amount,status,current_amount),transaction(order_id,campaign_id,amount,payment_type),donor(prodi,name,email,photo_url)").order("created_at",desc=True).execute()
    return res.data
@view_config(route_name='user_donations', request_method='GET', renderer='json')
@auth_required
def user_donations(request):
    donor_id = request.matchdict['id']
    res = supabase.table('donations').select("id,amount,is_anonymous,message,status,campaign(id,title,description,image_url,target_amount,status,current_amount),transaction(order_id,campaign_id,amount,payment_type),donor(prodi,name,email,photo_url)").eq('donor',donor_id).execute()
    return res.data

@view_config(route_name='donation', request_method='GET', renderer='json')
def get_donation(request):
    donation_id = request.matchdict['id']
    res = supabase.table('donations').select("id,amount,is_anonymous,message,status,campaign(id,title,description,image_url,target_amount,status,current_amount),transaction(order_id,campaign_id,amount,payment_type),donor(prodi,name,email,photo_url)").eq("id", donation_id).execute()
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
@view_config(route_name="get_all_donation",request_method="GET",renderer="json")
def get_all_donation(request):
    res = supabase.table('users').select("*").gt('total_donation',0).order('total_donation',desc=True).execute()
    return res.data
@view_config(route_name="get_campaign_donations",request_method="GET",renderer="json")
def get_campaign_donation(request):
    campaign_id = request.matchdict['id']
    print(campaign_id)
    print("This is called")
    res = supabase.table('donations').select("id,campaign,amount,is_anonymous,message,donor(id,name,prodi,nik,email,photo_url)").order('created_at').eq('campaign',campaign_id).execute()
    return res.data
@view_config(route_name='donation_create_payment', request_method='POST', renderer='json')
@auth_required
def create_donation_payment(request):
    try:
        body = request.json_body
        user = supabase.table('users').select("*").eq("id", body['donor_id']).execute().data[0]
        print(user)
        order_id = f"donation-{uuid4().hex}"
        frontend_url =request.registry.settings["pyramid.frontend_url"]
        snap = Snap(
            is_production=asbool(request.registry.settings.get("midtrans.production", False)),
            server_key=request.registry.settings["midtrans.server_key"],
            client_key=request.registry.settings["midtrans.client_key"],
        )
        
        compaign_id=body["campaign_id"]
        transaction_params = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": body["amount"],
            },
            "customer_details": {
                "first_name": user.get("name", ""),
                "email": user.get("email", ""),
            },
            "callbacks": {
                "finish": f"{frontend_url}/payment-success?donationId={compaign_id}"
            }
        }

        transaction = snap.create_transaction(transaction_params)

        transaction_data = TransactionCreate(
            order_id=order_id,
            donor_id=user["id"],
            campaign_id=body["campaign_id"],
            amount=body["amount"],
            payment_type="qris",
            transaction_status="pending"
        )
        result = supabase.table("transactions").insert(transaction_data.model_dump()).execute()
        print(result.data[0]['id'])
        donation_data = DonationCreate(
            amount=body['amount'],
            campaign=body['campaign_id'],
            donor=user['id'],
            is_anonymous=False,
            message=body['message'],
            transaction=result.data[0]['id'],
            status='pending',
        )
        print(donation_data.model_dump())
        supabase.table('donations').insert(donation_data.model_dump()).execute()
        return {
            "snap_token": transaction["token"],
            "redirect_url": transaction["redirect_url"],
            "order_id": order_id,
        }

    except ValidationError as e:
        return Response(status=400, json_body={"errors": e.errors()})
    except Exception as e:
        return Response(status=500, json_body={"error": str(e)})

@view_config(route_name="midtrans_webhook", request_method="POST", renderer="json")
def midtrans_webhook(request):
    body = request.json_body

    order_id = body.get("order_id")
    transaction_status = body.get("transaction_status")
    payment_type = body.get("payment_type")
    transaction_time = body.get("transaction_time")
    settlement_time = body.get("settlement_time")
    va_numbers = None

    if isinstance(body.get("va_numbers"), list) and len(body["va_numbers"]) > 0:
        va_numbers = body["va_numbers"][0].get("va_number")

    update_data = {
        "transaction_status": transaction_status,
        "payment_type": payment_type,
        "transaction_time":  transaction_time,
        "settlement_time": settlement_time,
        "va_numbers": va_numbers,
        "fraud_status": body.get("fraud_status"),
    }

    update_data = {k: v for k, v in update_data.items() if v is not None}

    result = supabase.table("transactions").update(update_data).eq("order_id", order_id).execute()
    print(result.data)
    if not result.data:
        return Response(status=404, json_body={"error" : "Transaction not found"})
    donation_update_data = {
        "status": "paid"
    }
    supabase.table('donations').update(donation_update_data).eq('transaction',result.data[0]['id']).execute()
    supabase.table('users').update({"total_donation": supabase.table('users').select("total_donation").eq('id',result.data[0]['donor_id']).execute().data[0]['total_donation']+result.data[0]['amount']}).eq('id',result.data[0]['donor_id']).execute()
    campaign_result = supabase.table('campaigns').select("*").eq('id',result.data[0]['campaign_id']).execute()
    campaign_update_data = {
        "current_amount":campaign_result.data[0]['current_amount']+result.data[0]['amount']
    }
    supabase.table('campaigns').update(campaign_update_data).eq('id',result.data[0]['campaign_id']).execute()
    if result.data:
        return {"status": "success", "updated": result.data}
    return Response(status=404, json_body={"error": "Transaction not found"})
