# -*- coding: utf-8 -*-
import scrapy

from lianjia.items import LianjiaItem

class Lianjiaspider(scrapy.Spider):
    name = 'lianjia1'
    allowed_domains = ['hz.lianjia.com']
    start_urls = []
    regions = {'xihu': '西湖',
               'xiacheng': '下城',
               'jianggan': '江干',
               'gongshu': '拱墅',
               'shangcheng': '上城',
               'binjiang': '滨江',
               'yuhang': '余杭',
               'xiaoshan': '萧山',
               'xiasha': '下沙',
               }
    for region in list(regions.keys()):
        for i in range(1, 11):
            start_urls.append('https://hz.lianjia.com/chengjiao/' + region + '//pg' + str(i) + "/")

    def parse(self, response):
        li_item = response.xpath('//ul[@class="listContent"]')
        for li in li_item:
            hrefs = li.xpath('//a[@class="img"]/@href').extract()
            for href in hrefs:
                yield scrapy.Request(url=href, callback=self.more, dont_filter=True)

    def more(self, response):
        item = LianjiaItem()
        info1 = ''
        # 地区
        area = response.xpath('//section[1]/div[1]/a[3]/text()').extract()[0]
        item['region'] = area.replace("二手房成交价格", "")
        # 小区名
        community = response.xpath('//title/text()').extract()[0]
        item['community'] = community[:community.find(" ", 1, len(community))]
        # 成交时间
        deal_time = response.xpath('//div[@class="wrapper"]/span/text()').extract()[0]
        item['deal_time'] = deal_time.replace("链家成交", "").strip()
        # 总价
        item['total_price'] = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[
                                  0] + '万'
        # 单价
        item['unit_price'] = response.xpath('//div[@class="price"]/b/text()').extract()[0] + '元/平'

        # 户型
        introContent = response.xpath('//div[@class="content"]/ul/li/text()').extract()
        item['style'] = introContent[0].strip()
        # 楼层
        item['floor'] = introContent[1].strip()
        # 大小
        item['size'] = introContent[2].strip()
        # 朝向
        item['orientation'] = introContent[6].strip()
        # 建成年代
        item['build_year'] = introContent[7].strip()
        # 装修情况
        item['decoration'] = introContent[8].strip()
        # 产权年限
        item['property_time'] = introContent[12].strip()
        # 电梯配备
        item['elevator'] = introContent[13].strip()
        # 其他周边等信息
        infos = response.xpath('//div[@class="content"]/text()').extract()
        if len(infos) != 0:
            for info in infos:
                info = "".join(info.split())
                info1 += info
            item['info'] = info1
        else:
            item['info'] = '暂无信息'
        return item
