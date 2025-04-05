import json
import random
from tqdm import tqdm
from broswer import *
from utils import *

# 随机等待函数，模仿人类，防止被风控
def human_like_delay():
    # 90%概率短等待，10%概率长等待
    if random.random() < 0.9:
        time.sleep(random.uniform(0.5, 1.5))
    else:
        time.sleep(random.uniform(2, 3))

class MarketSpider:
    def __init__(self, start_next_id=None, max_count=10000, users_num=1, data_path='./bilibili_market.jsonl'):
        self.nextId = start_next_id
        self.maxCount = max_count
        self.data_path = data_path
        self.users_num =users_num
        self.url = 'https://mall.bilibili.com/mall-magic-c/internet/c2c/v2/list'

    def crawl(self):
        count = 0
        with open("cookies.txt", "r") as f:
            cookie_pool = [line.strip() for line in f]
        pbar = tqdm(total=self.maxCount, unit="组", desc="爬取进度")
        while count < self.maxCount and cookie_pool:
            # human_like_delay()
            cookie_chosen = cookie_pool[count % len(cookie_pool)]

            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
                "content-length": "171",
                "content-type": "application/json",
                "cookie": cookie_chosen,
                "origin": "https://mall.bilibili.com",
                "priority": "u=1, i",
                "referer": "https://mall.bilibili.com/neul-next/index.html?page=magic-market_index",
                "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
                "user-agent": UserAgent().random
            }

            data = {"categoryFilter": "2312", "priceFilters": ["20000-0"], "sortType": "PRICE_ASC",
                    "discountFilters": ["50-70", "30-50"], "nextId": self.nextId}

            response = requests.post(self.url, headers=headers, json=data)
            count += 1
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    self.nextId = response_json['data']['nextId']

                    # 可以爬取并存储为jsonl
                    # with open(self.data_path, 'a', encoding='utf-8') as f:
                    #     f.write(json.dumps(response_json, ensure_ascii=False) + '\n')
                    item_list = response_json['data']['data']
                    for item in item_list:
                        if '灰色的丑小鸭' in item['c2cItemsName']:
                            print(f'ID: {item["c2cItemsId"]}', f'Price:{item["price"]}')
                            self.nextId = None
                    pbar.update(1)
                    time.sleep(random.uniform(0.5, 1.5))
                except Exception as e:
                    print(response)
                    print(response.text)
                    print(e)

            else:
                cookie_pool.remove(cookie_chosen)
                print(f"请求失败，状态码: {response.status_code}，移除当前cookie，剩余{len(cookie_pool)}个cookie")
                print(response.text)

        if not cookie_pool:
            print("cookie已经失效，重新获取cookie")
            cookies = ''
            for _ in range(self.users_num):
                cookies += get_login_cookies(url="https://www.bilibili.com", login_selector=".header-login-entry") + '\n'
            with open("cookies.txt", "w") as f:
                f.write(cookies)


if __name__ == '__main__':
    # 初始化爬虫
    start_next_id = None  # 可以设置为None或上次爬取的最后一个nextId
    max_count = 400  # 设置最大爬取数量
    users_num = 1 # 设置爬取账号数量
    spider = MarketSpider(start_next_id=start_next_id, max_count=max_count, data_path='./bilibili_market.jsonl')

    # 执行爬取
    spider.crawl()



