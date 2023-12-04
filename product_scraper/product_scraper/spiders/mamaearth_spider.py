import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from product_scraper.items import Product
from product_scraper.productloader import ProductLoader

class MySpider(CrawlSpider):
    name = 'crawl_spider'
    allowed_domains = ['mamaearth.in']
    start_urls = ['https://mamaearth.in/product/']
    rules = (
        Rule(LinkExtractor(allow=('products', )), callback='parse_product'),
    )

    def parse_product(self, response):
        loader = ProductLoader(item=Product(), response=response)

        # Extract product information using CSS selectors or XPath
        loader.add_css('name', 'h1.product-title::text')
        loader.add_css('price', 'span.product-price::text')
        loader.add_css('description', 'div.product-description::text')

        # Add more fields as needed

        # Load and return the Product item
        return loader.load_item()
