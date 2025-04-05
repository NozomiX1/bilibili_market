from typing import Optional, List, Tuple, Dict
from playwright.sync_api import sync_playwright, Cookie, Mouse


def convert_cookies(cookies: Optional[List[Cookie]]) -> Tuple[str, Dict]:
    if not cookies:
        return "", {}
    cookies_str = ";".join([f"{cookie.get('name')}={cookie.get('value')}" for cookie in cookies])
    cookie_dict = dict()
    for cookie in cookies:
        cookie_dict[cookie.get('name')] = cookie.get('value')
    return cookies_str, cookie_dict


def get_login_cookies(url: str, login_selector: str):
    """获取登录后的Cookies（同步模式）"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)
        page.click(login_selector)
        page.wait_for_selector(".header-entry-avatar img", timeout=120000)
        page.wait_for_load_state('networkidle')
        page.goto("https://mall.bilibili.com/mall-magic-c/internet/c2c/v2/list")
        cookies = context.cookies()
        target_cookies, _ = convert_cookies(cookies)
        browser.close()

        return target_cookies


