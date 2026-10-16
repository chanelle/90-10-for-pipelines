import os
def client_config():
    return {"base_url": "https://api.example-payments.test", "token": os.environ["PAYMENTS_API_TOKEN"]}
