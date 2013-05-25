# -*- coding: utf-8 -*-
from spider import *
from whooshSearcher import *



whoosh = WhooshSearcher(True)
spider = WhooshSpider(links=["http://www.huffingtonpost.co.uk/"], domains=["huffingtonpost.co.uk"], delay=0.0, whoosh=whoosh)

while True:
    spider.crawl(cached=False)