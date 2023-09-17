# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HlScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imgLink = scrapy.Field()  # 封面图片链接
    title = scrapy.Field()  # 标题
    price = scrapy.Field()  # 价格
    color = scrapy.Field()  # 颜色
    size = scrapy.Field()  # 尺码
    sku = scrapy.Field()  # 网站货号
    details = scrapy.Field()  # 详情
    img_urls = scrapy.Field()  # 大图的URL

