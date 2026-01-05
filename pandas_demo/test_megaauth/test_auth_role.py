import os, requests

BASE_URL = "https://megaauth.data.labillion.cn"  # 换成你实际对外的地址
TOKEN = "3cSa0l3jd3thowu8GjPjQkNdRn03awecTqYAG7Lhb5Z5vRpfaDqXkLFqm5jF"  # 你的 API Token
USER_UUID = "86d21b7f-ea29-454d-ad1e-082ecbe32900"

url = f"{BASE_URL}/api/v3/core/users/{USER_UUID}/"
headers = {"Authorization": f"Bearer {TOKEN}"}

r = requests.get(
    f"{BASE_URL}/api/v3/core/users/",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"uuid": USER_UUID},  # ← 过滤条件
    timeout=10)
r.raise_for_status()
print(r.json())
user = r.json()["results"][0]  # 过滤后只有一条
groups = [g["name"] for g in user["groups_obj"]]
print("用户所属组：", groups)


# 正确的，可执行的