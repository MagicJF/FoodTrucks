# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from datetime import datetime

def removespaces(value):
    return value.replace("  "," ")

def ConvertTimestamp(ts):
    ts = int(ts[:-3])
    return(datetime.utcfromtimestamp(ts).strftime('%Y.-%m-%d'))

def RedondearPrecios(price):
    return ("precio sin decimales")


class Wallabot5Item(scrapy.Item):
    # define the fields for your item here like:

    ItemUrl = scrapy.Field()
    item_title = scrapy.Field()
    item_price = scrapy.Field()   
    distance = scrapy.Field()     
    web_slug = scrapy.Field()
    item_description = scrapy.Field()
    modification_date = scrapy.Field()
    item_images = scrapy.Field()
    seller_details = scrapy.Field()



 