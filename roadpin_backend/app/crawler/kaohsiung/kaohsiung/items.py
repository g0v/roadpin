# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class KaohsiungItem(Item):
    # define the fields for your item here like:
    # name = Field()
    county_name  = Field()
    the_category = Field()
    the_idx      = Field()
    the_data     = Field()
    geo          = Field()
    start_timestamp = Field()
    end_timestamp   = Field()

