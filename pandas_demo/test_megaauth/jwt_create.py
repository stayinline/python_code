import jwt
import time
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import requests


def create_key():
    private_key_obj = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_key = private_key_obj.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key_obj.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("PRIVATE KEY:")
    print(private_key.decode())
    print("PUBLIC KEY:")
    print(public_key.decode())
    return private_key


def create_hs256_token(client_id, client_secret):
    token_url = "https://megaauth.data.labillion.cn/application/o/token/"  # 你的 aud
    payload = {
        "iss": client_id,
        "sub": client_id,
        "aud": token_url,
        "exp": int(time.time()) + 300,
        "jti": str(uuid.uuid4()),
    }
    token = jwt.encode(payload, client_secret, algorithm="HS256")
    print(token)
    return token



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




if __name__ == "__main__":
    client_id = "5FbLhz3bY34YEkIp3NucWvAd0fDPBpdvZXM4QwVE"
    client_secret = '92IXakTRaZExrefo0VkNTd2isdpsrVvfwtEccwZDx0eNxgz8GkswzL8F2sBTe0KVirtKbclpM3hR90KpwUSgZofEBod3RvQURMMzmjGaQAyBHjIujeWdQOk3obUpEvPi'


    token = create_hs256_token(client_id, client_secret)


    fetch_query_info_with_custom_sql(token)
