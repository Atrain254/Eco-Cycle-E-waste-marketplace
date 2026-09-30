import os, base64, requests
from datetime import datetime

def get_mpesa_access_token():
    consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
    consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    return response.json().get('access_token')

def generate_stk_password(shortcode, passkey, timestamp):
    data_to_encode = shortcode + passkey + timestamp
    return base64.b64encode(data_to_encode.encode()).decode('utf-8')
def initiate_stk_push(phone_number, amount, account_reference):
    access_token = get_mpesa_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = os.environ.get('MPESA_SHORTCODE')
    passkey = os.environ.get('MPESA_PASSKEY')
    password = generate_stk_password(shortcode, passkey, timestamp)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": os.environ.get('MPESA_CALLBACK_URL'),
        "AccountReference": account_reference,
        "TransactionDesc": "Eco-Cycle Salvage Payment"
    }

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()