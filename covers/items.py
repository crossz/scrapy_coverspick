# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoversItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_string = scrapy.Field()
    game_string = scrapy.Field()
    leader = scrapy.Field()
    pick_product = scrapy.Field()
    pick_team = scrapy.Field()
    pick_line = scrapy.Field()
    pick_desc = scrapy.Field()


class ScoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_string = scrapy.Field()
    game_string = scrapy.Field()
    team_away = scrapy.Field()
    team_home = scrapy.Field()
    score_away = scrapy.Field()
    score_home = scrapy.Field()

class ExpertpickItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_string = scrapy.Field()
    game_string = scrapy.Field()
    product1_left = scrapy.Field() # i.e. ats_away
    product1_right = scrapy.Field() # i.e. ats_home
    product2_left = scrapy.Field() # i.e. hilo_high
    product2_right = scrapy.Field() # i.e. hilo_low