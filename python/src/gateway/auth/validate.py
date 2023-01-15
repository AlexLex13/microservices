import requests

def token(request):
    if not "Authorization" in requests.headers:
        return None, ("missing credentials", 401)

    token = request.headers("Authorization")

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{settings}/validate",
        headers={"Authorization": token}
    )
