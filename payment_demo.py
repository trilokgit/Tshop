from instamojo_wrapper import Instamojo
API_KEY = "test_265e07f45821ef0b92b419880c0"
AUTH_TOKEN = "test_bc66a710941164352d851ee215a"

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')
# Create a new Payment Request
response = api.payment_request_create(
    amount='100',
    purpose='Testing',
    send_email=True,
    email="ttrilok363@gmail.com",
    redirect_url="http://localhost:8000/handle_redirect.py"
)
print(response['payment_request']['longurl'])
