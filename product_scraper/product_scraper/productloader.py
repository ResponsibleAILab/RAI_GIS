from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from product_scraper.items import Product

class ProductLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()
