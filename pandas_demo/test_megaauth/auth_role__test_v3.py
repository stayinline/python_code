import os
import requests

# 配置信息
BASE_URL = "https://megaauth.data.labillion.cn"  # 替换为你的实际地址
TOKEN = "3cSa0l3jd3thowu8GjPjQkNdRn03awecTqYAG7Lhb5Z5vRpfaDqXkLFqm5jF"  # 替换为你的API Token
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def get_all_authentik_users():
    """
    查询authentik中所有用户的基本信息（包含所属组）
    返回：所有用户的信息列表
    """
    all_users = []
    page = 1  # 分页起始页
    page_size = 100  # 每页获取的用户数量（可根据需要调整）

    while True:
        try:
            # 构造请求参数，支持分页
            params = {
                "page": page,
                "page_size": page_size
            }

            # 发送GET请求获取用户列表
            response = requests.get(
                f"{BASE_URL}/api/v3/core/users/",
                headers=HEADERS,
                params=params,
                timeout=10
            )

            # 检查请求是否成功
            response.raise_for_status()
            data = response.json()

            # 提取当前页的用户数据
            current_page_users = data.get("results", [])
            if not current_page_users:
                break  # 没有更多用户，退出循环

            # 处理每个用户的信息，提取关键字段和所属组
            for user in current_page_users:
                user_info = {
                    "uuid": user.get("uuid"),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "name": user.get("name"),
                    "is_active": user.get("is_active"),  # 是否激活
                    "last_login": user.get("last_login"),  # 最后登录时间
                    "groups": [g["name"] for g in user.get("groups_obj", [])]  # 所属组
                }
                all_users.append(user_info)

            # 检查是否有下一页（根据API返回的分页信息判断）
            if not data.get("next"):
                break  # 没有下一页，退出循环

            page += 1  # 进入下一页

        except requests.exceptions.RequestException as e:
            print(f"请求出错：{e}")
            break
        except Exception as e:
            print(f"处理用户数据时出错：{e}")
            continue

    return all_users


if __name__ == "__main__":
    # 获取所有用户信息
    users = get_all_authentik_users()

    # 输出用户信息
    print(f"共查询到 {len(users)} 个用户：")
    print("-" * 80)
    for idx, user in enumerate(users, 1):
        print(f"用户 {idx}:")
        print(f"  UUID: {user['uuid']}")
        print(f"  用户名: {user['username']}")
        print(f"  邮箱: {user['email']}")
        print(f"  姓名: {user['name']}")
        print(f"  是否激活: {user['is_active']}")
        print(f"  最后登录: {user['last_login'] if user['last_login'] else '从未登录'}")
        print(f"  所属组: {', '.join(user['groups']) if user['groups'] else '无'}")
        print("-" * 80)