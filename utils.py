import hashlib
import hmac
import time
import random
import requests
from fake_useragent import UserAgent


def hmac_sha256(key, message):
    """
    使用HMAC-SHA256算法对给定的消息进行加密
    :param key: 密钥
    :param message: 要加密的消息
    :return: 加密后的哈希值
    """
    # 将密钥和消息转换为字节串
    key = key.encode('utf-8')
    message = message.encode('utf-8')

    # 创建HMAC对象，使用SHA256哈希算法
    hmac_obj = hmac.new(key, message, hashlib.sha256)

    # 计算哈希值
    hash_value = hmac_obj.digest()

    # 将哈希值转换为十六进制字符串
    hash_hex = hash_value.hex()

    return hash_hex


def get_b_lsid():
    # 生成前8位固定长度的十六进制
    hex_chars = "0123456789ABCDEF"
    prefix = "".join(random.choices(hex_chars, k=8))

    # 生成时间戳部分（11位十六进制）
    timestamp_ms = int(time.time() * 1000)
    suffix = hex(timestamp_ms)[2:].upper()

    return f"{prefix}_{suffix}"


def get_buvid():
    res = requests.get('https://api.bilibili.com/x/frontend/finger/spi', headers={"user-agent": UserAgent().random}).json()
    return res['data']['b_3'], res['data']['b_4']


def get_bili_ticket():
    o = hmac_sha256("XgwSnGZ1p", f"ts{int(time.time())}")
    url = "https://api.bilibili.com/bapis/bilibili.api.ticket.v1.Ticket/GenWebTicket"
    params = {
        "key_id": "ec02",
        "hexsign": o,
        "context[ts]": f"{int(time.time())}",
        "csrf": ''
    }

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }
    resp = requests.post(url, params=params, headers=headers).json()
    return resp['data']['ticket'], resp['data']['created_at'] + resp['data']['ttl']