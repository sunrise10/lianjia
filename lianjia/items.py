# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class LianjiaItem(Item):
    region = Field()            #行政区域
    community = Field()         #房源名称
    deal_time = Field()         #房源名称
    total_price = Field()       #总价
    unit_price = Field()        #每平米单价
    style = Field()             #房屋户型
    floor = Field()             #楼层高度
    size = Field()              #建筑面积
    orientation = Field()       #朝向
    build_year = Field()        #建造时间
    decoration = Field()        #装修
    property_time = Field()     #产权年限
    elevator = Field()          #电梯
    info = Field()              #周边学校
