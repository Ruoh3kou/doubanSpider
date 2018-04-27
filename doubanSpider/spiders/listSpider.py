import os
import scrapy
import urllib.request
from scrapy.selector import Selector
from doubanSpider.items import doubanItem
from scrapy.linkextractors import LinkExtractor


class ListSpider(scrapy.Spider):
    name = "listSpider"
    allowed_domains = ["douban.com"]
    start_urls = ["https://www.douban.com/tag/%E6%97%A5%E6%9C%AC/movie"]

    print("begin to scrap....")

    def parse(self, response):
        item = doubanItem()  # title,score,cover_img_url
        lists = response.xpath('//div[@class="mod movie-list"]//dl')
        for i in lists:
            item['title'] = i.xpath(
                './dd/a/text()').extract_first()
            item['score'] = i.xpath(
                './dd/div[2]/span[2]/text()').extract_first()
            item['mainurl'] = i.xpath(
                './dd/a/@href').extract_first()
            cover_img_url = i.xpath(
                './dt/a/img/@src').extract_first()

            if cover_img_url:
                file_name = item['title'][:10] + '.png'
                file_path = os.path.join(
                    'C:\\Users\\11018\\projects\\doubanSpider\\pics', file_name)
                urllib.request.urlretrieve(cover_img_url, file_path)
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://www.douban.com/tag/%E6%97%A5%E6%9C%AC/movie' + \
                next_url[0]
            print(next_url)
            yield scrapy.Request(next_url)
