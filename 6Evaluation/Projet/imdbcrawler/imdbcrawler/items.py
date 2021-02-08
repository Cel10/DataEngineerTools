# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classement = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    year = scrapy.Field()
    synopsis = scrapy.Field()
    metascore = scrapy.Field()
    note = scrapy.Field()
    time = scrapy.Field()
    genres = scrapy.Field()    
    directors = scrapy.Field()  
    actors = scrapy.Field() 
    characters = scrapy.Field()
    rang = scrapy.Field()
    #link = scrapy.Field() 
