# import requests
#
# def get_user_groups_from_provider(userinfo_endpoint: str, access_token: str) -> list[str]:
#     resp = requests.get(
#         userinfo_endpoint,
#         headers={
#             "Authorization": f"Bearer {access_token}",
#             "accept": "application/json",
#         },
#         timeout=10,
#     )
#
#     if resp.status_code != 200:
#         raise RuntimeError("userinfo failed")
#
#     return resp.json().get("groups", [])
#
#
# def check_user_permission(
#     userinfo_endpoint: str,
#     allow_groups: list[str],
#     access_token: str,
# ) -> bool:
#     user_groups = get_user_groups_from_provider(
#         userinfo_endpoint,
#         access_token,
#     )
#     return bool(set(user_groups) & set(allow_groups))
