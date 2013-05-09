import os, re, sys; sys.path.insert(0, os.path.join("..", ".."))
from datetime import date
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO

class SimpleSpider(Spider):

    def visit(self, link, source=None):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            news_date = date(int(splitted_url[3]), int(splitted_url[4]), int(splitted_url[5]))
#             Por ahora coge el titulo de la url, pero seguramente es mejor cogerlo del HTML
            title = splitted_url[6].split('_')[0]
            print "Date:", news_date, "\nTitle:", title, "\nUrl:", link.url, "\n\n"

    def fail(self, link):
        print "failed:", link.url

    def priority(self, link, method=DEPTH):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            return Spider.priority(self, link, method)
        else:
            return 0.0


spider = SimpleSpider(links=["http://www.huffingtonpost.co.uk/"], domains=["huffingtonpost.co.uk"], delay=0.0)

while True:
    spider.crawl(cached=False)