import requests


def auth_with_db():
    username = "hemaoling"
    password = "BWefKAa2GJaBDvV"
    provider = "db"

    host = "https://megatrix.data.labillion.cn"

    auth_params = {
        "username": username,
        "password": password,
        "provider": provider,
    }
    auth_url = f"{host}/api/v1/security/login"
    auth_result = requests.post(auth_url, json=auth_params)
    print(auth_result.json())
    access_token = auth_result.json().get("access_token", "")
    print(access_token)
    return access_token



def query_api_with_token_v2(access_token):
    url = "https://megatrix.data.labillion.cn/api/v1/chart/"

    params = {
        "q": "(order_column:changed_on,order_direction:desc,page:0,page_size:25)"
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "user-agent": "Mozilla/5.0",
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)

    print("status =", resp.status_code)
    print("body =", resp.text)

    resp.raise_for_status()
    return resp.json()["count"]


def auth_with_db_v2():
    auth_url = "https://megatrix.data.labillion.cn/api/v1/security/login"

    payload = {
        "username": "hemaoling",
        "password": "BWefKAa2GJaBDvV",
        "provider": "db",
        "refresh": True,
    }

    resp = requests.post(auth_url, json=payload, timeout=10)

    print("status =", resp.status_code)
    print("body   =", resp.text)

    resp.raise_for_status()

    data = resp.json()
    access_token = data.get("access_token")

    if not access_token:
        raise RuntimeError("login success but access_token missing")

    return access_token


if __name__ == "__main__":
    auth_with_db_v2()

    # access_token = auth_with_db()

    # query_api_with_token_v2(access_token)
