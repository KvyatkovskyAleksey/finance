# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinanceItem(scrapy.Item):
    firm_name = scrapy.Field()
    fund_name = scrapy.Field()
    ticker = scrapy.Field()
    short_term_gain = scrapy.Field()
    short_term_gain_pct = scrapy.Field()
    long_term_gain = scrapy.Field()
    long_term_gain_pct = scrapy.Field()
    record_date = scrapy.Field()
    estimate_date = scrapy.Field()
    ex_date = scrapy.Field()
    pay_date = scrapy.Field()
    avoid_distribution_date = scrapy.Field()
    source_url = scrapy.Field()
