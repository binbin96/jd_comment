import scrapy
import json
from ..items import JdCommentItem
from scrapy.loader import ItemLoader


class JdCommentSpiderSpider(scrapy.Spider):
    name = 'jd_comment_spider'

    def start_requests(self):
        headers = {
            'authority': 'club.jd.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://item.jd.com/',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        # 商品编号列表
        productIds = [
            '100019791960',
            '100018601954',
            '100018927438'
        ]
        # url模板
        url_template = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&" \
                       "productId={}&score=0&sortType=5" \
                       "&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1"

        for productId in productIds:
            for page in range(100):  # 页数从0开始，最多爬到99页（也就是第100页）
                url = url_template.format(productId, page)
                meta = {'productId': productId, 'page': page}
                yield scrapy.Request(url=url, headers=headers, meta=meta, callback=self.parse, encoding='gbk')

    def parse(self, response):
        data_str = response.text.lstrip('fetchJSON_comment98(').rstrip(');')  # 删除前后不必要的字符，使其可被json解析
        data = json.loads(data_str)

        loader = ItemLoader(item=JdCommentItem(), response=response)
        loader.add_value('productId', data.get('productCommentSummary').get('productId'))  # 商品编号
        loader.add_value('comments', data.get('comments'))  # 评论列表的数据

        # 只爬取第一页的评论总结和热评
        if response.meta['page'] == 0:
            loader.add_value('productCommentSummary', data.get('productCommentSummary'))
            loader.add_value('hotCommentTagStatistics', data.get('hotCommentTagStatistics'))

        yield loader.load_item()
