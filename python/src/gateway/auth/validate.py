import requests
from python.config import settings

def token(request):
    if not "Authorization" in requests.headers:
        return None, ("missing credentials", 401)

    token = request.headers("Authorization")

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{settings.auth_svc_address}/validate",
        headers={"Authorization": token}
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
