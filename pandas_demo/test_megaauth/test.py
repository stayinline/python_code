import requests

AUTHENTIK_BASE = "https://megaauth.data.labillion.cn"
API_CHECK_ENDPOINT = f"{AUTHENTIK_BASE}/api/v3/core/users/me/"


def validate_token_remote(token: str) -> bool:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    resp = requests.get(API_CHECK_ENDPOINT, headers=headers, timeout=5)

    # print("status=", resp.status_code)
    # print("resp=", resp.text)

    return resp.status_code == 200


import requests

def fetch_query_info_with_custom_sql(token):
    query_sql = "SELECT id, first_name, last_name, username, email, last_login FROM ab_user"

    url = "https://megabank.data.labillion.cn/api/v1/sqllab/query_custom_sql?page_index=0&page_size=100"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
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
        "Authorization": f"Bearer {token}",
        "X-Megaauth-Token": f"{token}"
    }

    form_data = {
        "dataset_id": dataset_id,
    }
    result = requests.post(url, json=form_data, headers=headers, verify=False)
    print("Result: {}".format(result.json()))

if __name__ == "__main__":
    token = "PlgKCo0xf7CU50mftXUiBCwtGy6El9UTqiqrNlJN3El3a2MQGiYRlzXqM8si"
    print("megaauth valid token:", validate_token_remote(token))

    if (validate_token_remote(token)):
        # fetch_query_info_with_custom_sql(token)
        fetch_query_info_with_ids(token)
