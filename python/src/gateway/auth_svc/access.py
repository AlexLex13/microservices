import requests
from python.config import settings

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)
    
    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{settings.auth_svc_address}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)