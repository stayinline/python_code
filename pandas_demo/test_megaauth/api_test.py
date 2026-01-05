import requests


def auth_with_db():
    username = "hemaoling"
    password = "BWefKAa2GJaBDvV"
    provider = "db"

    host = "https://megabank.data.labillion.cn"

    auth_params = {
        "username": username,
        "password": password,
        "provider": provider,
    }
    auth_url = f"{host}/api/v1/security/login"
    auth_result = requests.post(auth_url, json=auth_params)
    access_token = auth_result.json().get("access_token", "")
    print(access_token)
    return access_token


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


def fetch_query_info_with_ids(token):
    dataset_id = "23::473"

    url = "https://megabank.data.labillion.cn/api/v1/sqllab/query_dataset_id?page_index=0&page_size=100"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    form_data = {
        "dataset_id": dataset_id,
    }
    result = requests.post(url, json=form_data, headers=headers, verify=False)
    print("Result: {}".format(result.json()))


def query_api_with_token(token):
    URL = "https://megatrix.data.labillion.cn/api/v1/chart/"

    params = {
        "q": "(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)"
    }

    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9",
        "user-agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}",
    }

    resp = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=10,
    )

    resp.raise_for_status()
    data = resp.json()

    count = data["count"]
    print("chart count =", count)

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

    # 调试用（强烈建议你先加上）
    print("status =", resp.status_code)
    print("body =", resp.text)

    resp.raise_for_status()
    return resp.json()["count"]

if __name__ == "__main__":
    access_token = auth_with_db()
    # fetch_query_info_with_custom_sql(access_token)
    # fetch_query_info_with_ids(access_token)
    # fetch_query_info_with_ids(access_token)
    query_api_with_token_v2(access_token)
