import requests

AUTHENTIK_BASE = "https://megaauth.data.labillion.cn"
API_TOKEN_ENDPOINT = f"{AUTHENTIK_BASE}/application/o/token/"
API_CHECK_ENDPOINT = f"{AUTHENTIK_BASE}/api/v3/core/users/me/"

# 你的OAuth App配置
CLIENT_ID = "5FbLhz3bY34YEkIp3NucWvAd0fDPBpdvZXM4QwVE"
CLIENT_SECRET = "92IXakTRaZExrefo0VkNTd2isdpsrVvfwtEccwZDx0eNxgz8GkswzL8F2sBTe0KVirtKbclpM3hR90KpwUSgZofEBod3RvQURMMzmjGaQAyBHjIujeWdQOk3obUpEvPi"

USERNAME = "hemaoling"
PASSWORD = "BWefKAa2GJaBDvV"


def get_jwt_access_token():
    """从Authentik获取 JWT Access Token"""
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD,
        "scope": "openid email profile"
    }

    resp = requests.post(API_TOKEN_ENDPOINT, data=payload, timeout=5, verify=False)
    res_json = resp.json()
    print("Auth response:", res_json)

    if "access_token" not in res_json:
        raise Exception("获取access_token失败，请检查client配置或密码")

    return res_json["access_token"]


def validate_token_remote(token: str) -> bool:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    resp = requests.get(API_CHECK_ENDPOINT, headers=headers, timeout=5, verify=False)
    return resp.status_code == 200


def fetch_query_info_with_custom_sql(token):
    query_sql = "SELECT id, first_name, last_name, username, email, last_login FROM ab_user"

    url = "https://megabank.data.labillion.cn/api/v1/sqllab/query_custom_sql?page_index=0&page_size=100"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # ← 用 JWT
        "X-Megaauth-Token": f"{token}"
    }

    form_data = {
        "database_id": 3,
        "sql": query_sql,
    }

    result = requests.post(url, json=form_data, headers=headers, verify=False)
    print("Result:", result.json())


def fetch_query_info_with_ids(token):
    dataset_id = "23::473"

    url = "https://megabank.data.labillion.cn/api/v1/sqllab/query_dataset_id?page_index=0&page_size=100"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # ← 用 JWT
        "X-Megaauth-Token": f"{token}"
    }

    form_data = {
        "dataset_id": dataset_id,
    }
    result = requests.post(url, json=form_data, headers=headers, verify=False)
    print("Result: {}".format(result.json()))


if __name__ == "__main__":
    token = get_jwt_access_token()
    print("Validate token:", validate_token_remote(token))

    if validate_token_remote(token):
        # fetch_query_info_with_custom_sql(token)
        fetch_query_info_with_ids(token)
