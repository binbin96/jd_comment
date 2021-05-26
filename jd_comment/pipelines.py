# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class JdCommentPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_URI = crawler.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        cls.MONGODB_DB_NAME = crawler.settings.get('MONGODB_DB_NAME', 'jd')  # database的名称
        return cls()

    def open_spider(self, spider):
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client[self.MONGODB_DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 从item中获取数据，如果没有数据，则默认为[]。保证这三个数据的类型恒定为列表
        comments = item.get('comments', [])
        productCommentSummary = item.get('productCommentSummary', [])
        hotCommentTagStatistics = item.get('hotCommentTagStatistics', [])

        productId = {'productId': item.get('productId')}  # 商品编号字典，用于合并入评论列表、热评

        # 将评论放入comments。如果comments不存在，会自动创建。
        for x in comments:
            x.update(productId)  # 把productId添加到字典中
            myquery = {'id': x.get('id'),
                       'guid': x.get('guid'),
                       'productId': x.get('productId'),
                       'nickname': x.get('nickname')}
            newvalues = {'$set': x}
            self.db.comments.update_one(myquery, newvalues, upsert=True)

        # 将评论总结放入summary
        for x in productCommentSummary:
            x.update(productId)
            myquery = {'skuId': x.get('skuId'),
                       'productId': x.get('productId')}
            newvalues = {'$set': x}
            self.db.summary.update_one(myquery, newvalues, upsert=True)

        # 将热评放入hotcomments
        for x in hotCommentTagStatistics:
            x.update(productId)
            myquery = {'id': x.get('id'),
                       'productId': x.get('productId')}
            newvalues = {'$set': x}
            self.db.hotcomments.update_one(myquery, newvalues, upsert=True)
