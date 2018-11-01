import scrapy
from scrapy.selector import Selector

from squarespace.items import SquarespaceItem

class SquarespaceSpider(scrapy.Spider):
    name = "thewearer"
    domain = 'https://www.thewearer.com'
    start_urls = [
        #'https://www.thewearer.com/new-in/',
        'https://www.thewearer.com/summer-sale/',
        'https://www.thewearer.com/shop-designer-earrings/',
        'https://www.thewearer.com/shop-designer-rings/',
        'https://www.thewearer.com/shop-designer-necklaces/',
        'https://www.thewearer.com/shop-designer-bracelets/',
        'https://www.thewearer.com/sunglasses/'
    ]

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        crawler.stats.set_value('store_id', 296)
        return cls(crawler.stats)

    def parse(self, response):
        archive_links = response.xpath("//div[@id='productList']/a/@href").extract()
        for archive_link in archive_links:
            detail_url = self.domain + archive_link
            # yield {
            #     'detail_url': detail_url
            # }

            # category = detail_url.split('=')
            # if (len(category) > 1 and category[1]):
            yield scrapy.Request(detail_url, callback=self.parse_detail)


    def parse_detail(self, response):
        item = SquarespaceItem()
        product_id = response.xpath("//div[@id='productWrapper']/@data-item-id").extract_first()
        item['product_id'] = '296' + ''.join(product_id)
        item['source'] = 'scraper'
        item['store'] = 'The Wearer'
        item['store_id'] = 296
        item['category'] = ''
        item['name'] = response.xpath("//h1[@class='product-title']/text()").extract_first()
        item['product_url'] = response.url
        item['product_image'] = response.xpath("//div[@id='productSlideshow']/div[1]/img/@data-src").extract_first()
        item['style'] = ''
        item['gender'] = ''
        item['size'] = ''
        item['brand'] = 'Thewearer'
        item['product_type'] = ''
        item['description'] = response.xpath("string(//div[@class='product-excerpt'])").extract()
        normal_price = 0
        discounted_price = 0
        price_list = response.xpath("//span[@class='sqs-money-native']/text()").extract()
        if ((len(price_list) > 1) and (price_list is not None)):
            discounted_price = price_list[0]
            normal_price = price_list[1]
        elif ((len(price_list) == 1) and (price_list is not None)):
            normal_price = price_list[0]
            discounted_price = normal_price

        item['retail_price'] = normal_price
        item['sale_price'] = discounted_price
        item['currency'] = 'GBP'
        item['shipping_availability'] = ''
        item['discount_type'] = ''
        item['online'] = 'true'
        item['offline'] = 'false'
        item['latitude'] = '51.5350366'
        item['longitude'] = '-0.1040289'
        item['city'] = 'London'
        item['created'] = '2018-07-02T06:00:26.434912Z'
        item['modified'] = '2018-07-02T06:00:26.437831Z'
        item['status'] = 1
        item['display_address'] = 'Angel, Camden Passage'
        item['zone'] = 3

        yield item
