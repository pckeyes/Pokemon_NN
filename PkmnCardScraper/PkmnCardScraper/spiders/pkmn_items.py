#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 15:57:38 2018

@author: piperkeyes
"""

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Card(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    HP = scrapy.Field()
    pkmn_type = scrapy.Field()
    card_set = scrapy.Field()
    rating = scrapy.Field()
    image = scrapy.Field()