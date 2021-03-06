# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from covers.items import ScoreItem
from covers.items import ExpertpickItem
from covers.items import CoversItem


class JsonWriterPipeline_4_matchups(object):

    def open_spider(self, spider):
        self.file = open('ScoreItem.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, ScoreItem):
            line = json.dumps(dict(item)) + ",\n"
            self.file.write(line)
        return item

class JsonWriterPipeline_4_expertpickscount(object):

    def open_spider(self, spider):
        self.file = open('ExpertpickItem.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, ExpertpickItem):
            line = json.dumps(dict(item)) + ",\n"
            self.file.write(line)
        return item

class JsonWriterPipeline_4_coverscontent(object):

    def open_spider(self, spider):
        self.file = open('CoverspickItem.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, CoversItem):
            line = json.dumps(dict(item)) + ",\n"
            self.file.write(line)
        return item
