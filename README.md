# b站市集爬取
由于b站市集没有搜索功能，想要低价淘自己想要的手办过于麻烦，故写了这个爬虫代码。

## 使用方法
1. 安装运行环境
```bash
pip install -r requirements.txt
playwright install
```
2. 修改bilibili_market.py中的参数
```python
start_next_id = None  # 可以设置为None或上次爬取的最后一个nextId
max_count = 400  # 设置最大爬取组数(总共会爬取的商品数量为 max_count * 10，也就是说爬取的一组包含10个商品)
users_num = 1 # 设置爬取账号数量（默认1个账号）
item_name = '灰色的丑小鸭' # 设置要爬取的商品名称，可以是名字的一部分
```
3. 运行bilibili_market.py
```bash
python bilibili_market.py
```
运行时会自动打开浏览器，注意扫码登录

3. 运行后会直接在终端中输出最低商品的ID和价格（价格单位是“角”，换算为元要除以100）。稍微修改代码，也可以将数据存储到文件中。


## 一些建议
1. 同一个账号不要过于高频的访问（大概1s访问一次），否则很快就会触发风控（412错误）。可以尝试在访问之间加上随机的sleep时间（bilibili_market.py中有human_like_delay()函数）
2. 如果你有多个账号，可以尝试使用多个账号流水线爬取（bilibili_market.py中有users_num参数），并且流水线足够长的话可以不使用sleep的操作（大概超过4个账号就能实现）。
3. 多账号爬取的功能我没有过多测试，可能存在bug。
4. 代码中，爬取的商品按价格升序，还是用了筛选功能
```python
data = {"categoryFilter": "2312", "priceFilters": ["20000-0"], "sortType": "PRICE_ASC",
        "discountFilters": ["50-70", "30-50"], "nextId": self.nextId}
# "categoryFilter": "2312"代表筛选出手办
# "priceFilters": ["20000-0"]代表价格在200以上
# "sortType": "PRICE_ASC"代表按价格升序
# discountFilters": ["50-70", "30-50"]代表折扣在50%-70%和30%-50%之间
# 这些参数可以通过浏览器的开发者工具查看
```

