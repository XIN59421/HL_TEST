import re
import time

import scrapy
from scrapy import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By

from ..items import HlScrapyItem


class JDSpider(scrapy.Spider):
    name = 'myJD'
    start_urls = ['https://list.jd.com/list.html?cat=1318,12099,9756']

    def start_requests(self):

        driver = webdriver.Chrome()
        driver.get("https://www.jd.com/")
        driver.implicitly_wait(10)
        driver.find_element(By.LINK_TEXT, '你好，请登录').click()
        driver.find_element(By.LINK_TEXT, '账户登录').click()
        driver.find_element(By.ID, 'loginname').send_keys('15553753009')
        driver.find_element(By.ID, 'nloginpwd').send_keys('59421WangGx')
        driver.find_element(By.ID, 'loginsubmit').click()
        time.sleep(5)
        cookies = driver.get_cookies()
        driver.quit()
        scrapy_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        for url in self.start_urls:
            yield Request(url, cookies=scrapy_cookies)

    def parse(self, response):
        sel = Selector(response)
        list_item = sel.css('#J_goodsList > ul > li')
        for i in list_item:
            JD_item = HlScrapyItem()
            JD_item['imgLink'] = i.css('div.p-img img::attr(src)').extract_first()
            JD_item['title'] = i.css('div.p-name em::text').extract_first()
            JD_item['price'] = i.css('.p-price strong i').extract_first()
            JD_item['color'] = i.css('ul.ps-main li.ps-item a::attr(title)').extract_first()
            JD_item['size'] = i.css('li.gl-item::attr(data-sku)').extract_first()
            JD_item['sku'] = i.css('li.gl-item::attr(data-spu)').extract_first()
            JD_item['details'] = i.css('div.p-name em::text').extract_first()
            JD_item['img_urls'] = i.css('div.p-img a::attr(href)').extract_first()
            yield JD_item
        # 爬取多个页面
        # next_page = sel.css('a.pn-next::attr(href)').extract_first()
        # for j in next_page:
        #     url = response.urljoin(j.extract())
        #     yield Request(url=url)
