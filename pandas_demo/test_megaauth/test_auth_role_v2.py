import requests

# =========================
# 1. 原始 curl 里的 Cookie（直接拷贝）
# =========================
RAW_COOKIE = (
    "session=.eJxlVW3TqroV_SsdP9cOhBfhfFMRhEdQERJIp-NAgvISEAUVuXP_e8NzbnvaOR8yk4Sw9tprr2T_MTtfHlmXz370j2f299m5oLMfM5JcsjRTErKQVFleaNkivShUSilYpFRLF4pGNUFVEpCIqpoqEgFEvEiULgRRESSZEl0H-kVc6FSTEyKo_LhIdDGTLgsiLeQkBakm6yqVFU1TROmSpIkgS-CSpooAQEpnnMizyx4_2QC-ZDeSsIwvsoavbsmz55T_mP2tn_345yz7OHlqkWJfOKdwtEWvsDu77lu8tlW7rIBXxsI-wJVbwsIbr8A1bOABWMbBUdkHGyVGHnPL5dsu3gXdsrdd3ooTo6HdCP_g2C2R3An7Rrf-m4y31w6IDAMzp5F_29V-Tq3NM7XMIkFDlyD9uau95w6Yb2INbQxM4XsPaK8UwSZGZrv7cH6NJ8YF51e7ggdcyQtsMQ4YwwYZ3YDlLnBqbFxlD8ECo1j2RrP2aj43lqJbOiUO7CEeK8UF8egZtuwCPgwv3xuMefWm2K2dnKLjxBvjDd67Td56IU3CwHGyaljHDXtlmz5P6vYRM7_CpsdQmZ_8wHklDOaTFjjKJy0Gb4yBZyxHbzyKHLeNI45bbqRJV9fg_I2Q622K1Mov1GI9PtmqGxCu-_HtjkfBO70LrvFn0hUD_Vs3jBSuS_dMkPYiW-dFa1bhyBl3f313C73CCPMcBmHiEiOR_9-mdrOS8NqhnMeY_Myv8AK_8kovdxGvfc2HQd5c53pvhB-OUWLE64yOYow2Azb8Ym_BPAYO2wdOEQPOEcE6BhsFIz4snhPwfuaPxDxB7-_aT_MUDG1a0-V3HSPnFdfak1qwTNaT32AfI9ZFEmakZnWCYMX5CqSBjHN9cv5syj9F5iu12BNPHqhpS2v4jICSpyic4nAMnXtIaab4XBeGa_ghNawiCY5cn__iJBb8v7NpzcrkF87_8CWTFxpS6yLZch-zrgi-fYi7VCJXGHmMTPel-vZ0nVq6ZG_MKkXsOeF-n41WLbHCK6wZowB-fu07bWq9rz7yW2rpv_bR5IXr9Yj8PkHyFN_DiOZxPbziYrXCltimv2IKXC_595j-J4mu13ALC65X-du-aLqRMKyOv3BWp9Nv2Nw3yuN3bE-II_t6BPqTSLDHkT1xRNyTIvmsNjxGbm_gEwNeJ8TzZcLkb5VM7wljlV_Jn8yqRF9sfbdiarBxigzp8gmY96TuC2j5VQhgsjcd0631O0Tf91H86Vf7E4aOlIS9G9fiGnLPEMvrw1AQvGi1DQx2CqNQohUbAss0g2owQ4u-p7fIjB7eHujJ1dzmfdkZW8Ho5Cg6BPC2NRfDqX0EymZUl-e2aqXkdl_m2d2Yv0NCsLLTW0KTAXbzN1DMxbzoP4TAHh7HBdJI89qvxxc-LRKlw7Hvmfp-1eNKss9IjSsADvOyWhc1TonxfFwXp8Ppvl17j-xi5Lea-vPj4771y_Ve6jL8gWUmqsPl6sQPVUbpBi7ml36dCc4iI6pykEFnVufLXu_jkMXwHjqXbaZE4pCFe_rB3WsTGHNKs1Xo2g1utHVy1ZwyRdE4j1C8WS_cQSxkCe0xvxlb9e54c7N6KvUjFFIh6dr5WTitvcu-U3e7T3bV0fhqTTFs6kKv20PbPhfhlzaSE2w-SJTqYXdtK1pkL3HJ3GfWXObH97hpt9teT85M0zKZFWs3lsv7Zn49r84Szcxl0R_wg6mfc-M-kCmv59p9SHae5uvNTbrfKpBuG5j253pZj8v2K0V36aBFUfy6LvZtq3vBy8-WAwnX3QO0cctf10tjWUEGGXG3R5d5lS3Tc04fQk8kyR4O9OucCUvxYLfjisWCIgunGHv8wTdWetK85Wv_GvH8DjufKhfnA1fL5fq4y0AzRnoX9YeTvCRzJ3U2WqBm70708ui-gw8fRrerLXzJ1W41Nh_7pDnnkH6pKU6DsJYKKp6EuEpWctndlFgoMqPQd6V00XKF5TFcWnIyVBpTzIqTRvNX8mU8nbsBN7xJz_7151-d-tw-bq-CZg_ev6d11vRF9Z82fu76pJ86OxlTpbqIX4HsnwT0yL-IH6ZMeb9XTLXK2Z__BuuC6xw.aUkteA.t39mxSX6hcdNZyvKFgETLsaLKuw"
)

# =========================
# 2. Authentik 配置
# =========================
AUTHENTIK_BASE_URL = "https://megaauth.data.labillion.cn"
TIMEOUT = 5


# =========================
# 3. 提取 session
# =========================
def extract_session_cookie(raw_cookie: str) -> str:
    for part in raw_cookie.split(";"):
        part = part.strip()
        if part.startswith("session="):
            return part[len("session="):]
    raise ValueError("session cookie not found")


# =========================
# 4. 请求 authentik 校验用户
# =========================
import requests

AUTHENTIK_BASE_URL = "https://megaauth.data.labillion.cn"
PROVIDER_SLUG = "mega-venus-role"
TIMEOUT = 5


def get_user_from_authentik_provider(session_value: str) -> dict:
    """
    使用 authentik OIDC Provider（固定 provider）
    通过 session cookie 获取 userinfo
    """

    # 1. 先读取 provider 的 openid configuration
    well_known_url = (
        f"{AUTHENTIK_BASE_URL}/application/o/{PROVIDER_SLUG}/"
        ".well-known/openid-configuration"
    )

    conf_resp = requests.get(well_known_url, timeout=TIMEOUT)
    conf_resp.raise_for_status()

    print(conf_resp.text)
    oidc_conf = conf_resp.json()
    userinfo_endpoint = oidc_conf["userinfo_endpoint"]

    # 2. 用 session cookie 调 userinfo
    resp = requests.get(
        userinfo_endpoint,
        cookies={"session": session_value},
        headers={
            "accept": "application/json",
            "user-agent": "megaai-auth-test",
        },
        timeout=TIMEOUT,
    )

    print("authentik provider status:", resp.status_code)

    if resp.status_code != 200:
        raise RuntimeError(resp.text)

    return resp.json()


def get_user_from_authentik_admin_api(session_value: str) -> dict:
    url = f"{AUTHENTIK_BASE_URL}/api/v3/core/users/me/"

    resp = requests.get(
        url,
        cookies={"session": session_value},
        headers={
            "accept": "application/json",
            "user-agent": "megaai-auth-test",
        },
        timeout=TIMEOUT,
    )
    print("resp:", resp)

    if resp.status_code != 200:
        raise RuntimeError(resp.text)

    user = resp.json()

    # 强制校验 provider
    provider = user.get("attributes", {}).get("authentik_provider")
    if provider != "mega-venus-role":
        raise RuntimeError(f"invalid provider: {provider}")

    return user


# =========================
# 5. 提取 Group
# =========================
def extract_groups(user_info: dict) -> list[str]:
    return [g["name"] for g in user_info.get("groups", [])]


import requests


def get_user_groups_from_provider(userinfo_endpoint: str, access_token: str) -> list[str]:
    resp = requests.get(
        userinfo_endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "accept": "application/json",
        },
        timeout=10,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"userinfo failed: {resp.text}")

    userinfo = resp.json()
    return userinfo.get("groups", [])


def allow_login(access_token: str) -> bool:
    groups = get_user_groups_from_provider(
        "https://authentik.xxx.com/application/o/megapipe/userinfo/",
        access_token,
    )
    return "data-engineer" in groups


# =========================
# 6. 单测入口
# =========================
def main():
    print("== MegaAI Authentik Session Test ==")

    session_value = extract_session_cookie(RAW_COOKIE)
    print("session cookie:", session_value)
    print("session extracted OK")

    user_info = get_user_from_authentik_admin_api(session_value)
    # user_info = get_user_from_authentik_provider(session_value)

    groups = extract_groups(user_info)

    print("\n--- RESULT ---")
    print("username :", user_info.get("username"))
    print("name     :", user_info.get("name"))
    print("groups   :", groups)

    # 示例断言（按你系统实际改）
    assert user_info["is_active"] is True
    assert len(groups) > 0


if __name__ == "__main__":
    main()
