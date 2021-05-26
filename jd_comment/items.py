# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class JdCommentItem(scrapy.Item):
    productId = scrapy.Field(
        output_processor=TakeFirst()  # 使得输出的productId是int类型，而不是list
    )
    comments = scrapy.Field()  # 评论列表
    productCommentSummary = scrapy.Field()  # 评价汇总数据
    hotCommentTagStatistics = scrapy.Field()  # 热评标签
