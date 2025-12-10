import requests




if __name__ == "__main__":

    "https://megaauth.data.labillion.cn/application/o/megabank/"
    AUTHENTIK_URL = "https://megaauth.data.labillion.cn"  # 根据你的部署改
    TOKEN_ENDPOINT = f"{AUTHENTIK_URL}/application/o/token/"

    client_id = "5FbLhz3bY34YEkIp3NucWvAd0fDPBpdvZXM4QwVE"
    client_secret = "92IXakTRaZExrefo0VkNTd2isdpsrVvfwtEccwZDx0eNxgz8GkswzL8F2sBTe0KVirtKbclpM3hR90KpwUSgZofEBod3RvQURMMzmjGaQAyBHjIujeWdQOk3obUpEvPi"

    username = "hemaoling"
    password = "BWefKAa2GJaBDvV"

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
    }

    resp = requests.post(TOKEN_ENDPOINT, data=data, verify=True)

    if resp.status_code == 200:
        j = resp.json()
        access_token = j.get("access_token")
        refresh_token = j.get("refresh_token")
        print("Access token:", access_token)
        print("Refresh token:", refresh_token)
    else:
        print("Error:", resp.status_code, resp.text)
