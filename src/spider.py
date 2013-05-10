import os, re, sqlite3, sys; sys.path.insert(0, os.path.join("..", ".."))
from datetime import date
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO
from pattern.web import URL, plaintext
from django.utils.encoding import smart_str, smart_unicode

class SQLiteSpider(Spider):
    
    def visit(self, link, source=None):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            article_date = date(int(splitted_url[3]), int(splitted_url[4]), int(splitted_url[5]))
#             Por ahora coge el titulo de la url, pero seguramente es mejor cogerlo del HTML
            title = splitted_url[6].split('_')[0]
#             TODO
            content = ''
            conn = sqlite3.connect('news.db')
            c = conn.cursor()
            c.execute("INSERT INTO news VALUES(?,?,?,?)", (title, str(article_date), link.url, content))
            conn.commit()
            conn.close()
            s = URL(link.url).download()
            content = plaintext(s,linebreaks=2, indentation = True)
            encodedContent=smart_str(content)
            print "Date:", article_date, "\nTitle:", title, "\nUrl:", link.url, "\n\n"
            print "Content:\n",encodedContent
            print "----------------------------------------------------------------------------------------------"

    def fail(self, link):
        print "failed:", link.url,"\n"

    def priority(self, link, method=DEPTH):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            return Spider.priority(self, link, method)
        else:
            return 0.0


conn = sqlite3.connect('news.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS news (title text, date text, url text, content text)''')
conn.commit()
conn.close()

spider = SQLiteSpider(links=["http://www.huffingtonpost.co.uk/"], domains=["huffingtonpost.co.uk"], delay=0.0)

while True:
    spider.crawl(cached=False)