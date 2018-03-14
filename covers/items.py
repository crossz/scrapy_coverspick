# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoversItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    game = scrapy.Field()
    leader = scrapy.Field()
    pick_product = scrapy.Field()
    pick_team = scrapy.Field()
    pick_line = scrapy.Field()
    pick_desc = scrapy.Field()


class ScoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    team_away = scrapy.Field()
    team_home = scrapy.Field()
    score_away = scrapy.Field()
    score_home = scrapy.Field()
