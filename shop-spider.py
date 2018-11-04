import scrapy
class shopSpider(scrapy.Spider):
    name = "shop"
	#response = "a"

    def start_requests(self):
        urls = [
        'https://www.thewearer.com/new-in/',
        'https://www.thewearer.com/summer-sale/',
        'https://www.thewearer.com/shop-designer-earrings/',
        'https://www.thewearer.com/shop-designer-rings/',
        'https://www.thewearer.com/shop-designer-necklaces/',
        'https://www.thewearer.com/shop-designer-bracelets/',
        'https://www.thewearer.com/sunglasses/'
		]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'shop-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    def parse(self, response):
        for product in response.css('div.product-meta'):
            yield {
                'product-title': product.css('div.product-title::text').extract_first(),
                'price': product.css('span.sqs-money-native::text').extract_first(),
                
            }
