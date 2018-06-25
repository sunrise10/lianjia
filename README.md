![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsjzbxg71uj20gk0dcwff.jpg)

学习`python`爬虫一周多了，看了看练手例子，突然看到链家网的二手房成交数据很值得去抓取下，也正好看看房价走势

因为最近在学习`scrapy`，所以就用`scrapy`和`xpath`来抓取，抓取的数据就存`MySQL`数据库中，方便以后查看。

抓取之前得先去分析下链家网二手房成交量页面，一看额。。。

![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsjzl48oy9j21ho0gwgue.jpg)
这个价格`2**万`是怎么回事，说实话刚看到这个页面的时候觉得价格得去APP里查看，这还抓**(TM...)啊,不过用开发者工具仔细看了下页面，发现了一个好东西
`https://hz.lianjia.com/chengjiao/103102419296.html`,点进去发现原来如此，这时突然觉得链家好low啊

![意外发现的链接](https://ws1.sinaimg.cn/large/ecd2c314gy1fsjzr89c31j20v80bmadt.jpg)

![点击去的网页](https://ws1.sinaimg.cn/large/ecd2c314gy1fsjzxnaysij21u00nwqoj.jpg)

##### 心里突然有点小激动哈！

![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsk018rqoxj207z07zdg3.jpg)

> 正式开始，我们的思路是首先去列表页把隐藏的详情页，提取出来，然后进详情页，具体的抓取了，抓取的代码相对简单：
```
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
               'xiasha': '下沙'}
    for region in list(regions.keys()):
        for i in range(1, 11):
            start_urls.append('https://hz.lianjia.com/chengjiao/' + region + '//pg' + str(i) + "/")

    def parse(self, response):
        #把隐藏的详情HTML拿出来
        li_item = response.xpath('//ul[@class="listContent"]')
        for li in li_item:
            hrefs = li.xpath('//a[@class="img"]/@href').extract()
            for href in hrefs:
                #进入详情，继续抓
                yield scrapy.Request(url=href, callback=self.more, dont_filter=True)
```
> 进入隐藏的HTML挨个抓取
```
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
```

在这里我只抓取了`1`到`10`页的内容，如果大家想抓全部的内容的话还得在抓取之前，先把总页数先抓过来，也不一定都是`100`，`xpath`是
```
//div[@class="page-box house-lst-page-box"]/@page-data
得到的数据是：{"totalPage":87,"curPage":1}类似这样的信息，具体大家再把87提取出来就可以了
```
![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsk07zwzzij20gk03awec.jpg)

抓取过程中可以看到日志：

![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsk0uk34wxj209r06t3z4.jpg)

接下来就是把抓取的数据存进数据库，说实话我是做android开发的，对于数据库不是很懂(还想着直接存txt嘿嘿，其实就是懒不想去看)，搞了半天才搞好，对于python和数据库链接，我用的是peewee，一个简单、轻巧的 Python ORM。研究了文档半天突然又发现这咋和scrapy一起用啊，没事继续研究,发现也简单。

![image](https://ws1.sinaimg.cn/large/ecd2c314gy1fsk1c5qo7uj2069069mx4.jpg)

>新建一个model

```
# -*- coding: utf-8 -*-

from peewee import *

db = MySQLDatabase('lianjia', host='localhost', port=3306, user='root', passwd='12345678',
                   charset='utf8')


# define base model
class BaseModel(Model):
    class Meta:
        database = db

class LianjiaInfo(BaseModel):
    region = CharField()
    community = CharField()
    deal_time = CharField()
    total_price = CharField()
    unit_price = CharField()
    style = CharField()
    floor = CharField()
    size = CharField()
    orientation = CharField()
    build_year = CharField()
    decoration = CharField()
    property_time = CharField()
    elevator = CharField()
    info = TextField()

db.connect()
db.create_tables([LianjiaInfo], safe=True)

```

> 在pipelines.py中直接插入数据

```
LianjiaInfo.create(region=item['region'],community=item['community'],deal_time=item['deal_time'],
                           total_price=item['total_price'],unit_price=item['unit_price'],style=item['style'],
                           floor=item['floor'], size=item['size'],orientation=item['orientation'],
                           build_year=item['build_year'],decoration=item['decoration'],property_time=item['property_time'],
                           elevator=item['elevator'],info=item['info'])
```
ok看看结果：一共`2516`条数据，按理说一页`30`条，`10`页`9`个区有`2700`条数据，还有`186`条数据不见了，恕我学习`python`爬虫没多久实在是不理解

![这是一部分数据](https://ws1.sinaimg.cn/large/ecd2c314gy1fsk1w0viebj21hc0xce81.jpg)
