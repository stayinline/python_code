# import pytest
# from unittest.mock import patch
# from authentik_groups import check_user_permission
#
# AUTHENTIK_BASE_URL = "https://megaauth.data.labillion.cn"
#
# USERINFO_ENDPOINT = "https://megaauth.data.labillion.cn/application/o/megapipe/userinfo/"
# ALLOW_GROUPS = ["data-engineer"]
#
#
# def mock_userinfo(groups):
#     return {
#         "sub": "123",
#         "preferred_username": "test_user",
#         "groups": groups,
#     }
#
#
# @patch("auth.requests.get")
# def test_user_has_permission(mock_get):
#     # 模拟 authentik userinfo 返回
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = mock_userinfo(
#         ["data-engineer", "other-group"]
#     )
#
#     assert check_user_permission(
#         USERINFO_ENDPOINT,
#         ALLOW_GROUPS,
#         access_token="fake-token",
#     ) is True
#
#
# @patch("auth.requests.get")
# def test_user_has_no_permission(mock_get):
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = mock_userinfo(
#         ["data-analyst"]
#     )
#
#     assert check_user_permission(
#         USERINFO_ENDPOINT,
#         ALLOW_GROUPS,
#         access_token="fake-token",
#     ) is False
#
#
# @patch("auth.requests.get")
# def test_userinfo_failed(mock_get):
#     mock_get.return_value.status_code = 401
#
#     with pytest.raises(RuntimeError):
#         check_user_permission(
#             USERINFO_ENDPOINT,
#             ALLOW_GROUPS,
#             access_token="bad-token",
#         )
