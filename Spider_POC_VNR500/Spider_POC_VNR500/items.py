# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderPocVnr500Item(scrapy.Item):
    YEAR = scrapy.Field()
    CHART_ID = scrapy.Field()
    INDEX = scrapy.Field()
    COMPANY_LEADER = scrapy.Field()
    COMPANY_NAME = scrapy.Field()
    COMPANY_VNR500_Rating = scrapy.Field()
    COMPANY_MDN = scrapy.Field()
    COMPANY_STOCK_CODE = scrapy.Field() 
    COMPANY_HEADQUARTERS = scrapy.Field()
    COMPANY_TEL = scrapy.Field()
    COMPANY_FAX = scrapy.Field()
    COMPANY_EMAIL = scrapy.Field()
    COMPANY_WEB = scrapy.Field()
    COMPANY_FOUNDED_YEAR = scrapy.Field()
    COMPANY_SUMMARY = scrapy.Field()
    COMPANY_NEWS = scrapy.Field()
