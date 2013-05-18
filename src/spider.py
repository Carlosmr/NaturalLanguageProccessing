import os, re, sqlite3, sys; sys.path.insert(0, os.path.join("..", ".."))
from datetime import date
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL,plaintext,DOM
from django.utils.encoding import smart_str, smart_unicode

class SQLiteSpider(Spider):
    
    def htmlParser(self,link):
        html = URL(link).download()
        result = ''
        
        body = DOM(html).body
        for e in body.by_tag('p'):
            a = e.by_tag('a')
            img = e.by_tag('img')
            span = e.by_tag('span') 
        
            if a == [] and img == [] and span == []:
                plainText = plaintext(str(e),linebreaks=2, indentation = True)
                content = str(plainText)
                filterContent = content.strip().lower()
                if filterContent != 'share your comment:':
                    result = result + content + '\n'
                    
        pretty = unicode(result.strip())
        return pretty
        
    
    def visit(self, link, source=None):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            article_date = date(int(splitted_url[3]), int(splitted_url[4]), int(splitted_url[5]))
#             Por ahora coge el titulo de la url, pero seguramente es mejor cogerlo del HTML
            title = splitted_url[6].split('_')[0]
#            Parseo el html dejando unicamente el contenido de la noticia
            encodedContent = self.htmlParser(link.url)
            conn = sqlite3.connect('news.db')
            c = conn.cursor()
            c.execute("INSERT INTO news VALUES(?,?,?,?)", (title, str(article_date), link.url, encodedContent))
            conn.commit()
            conn.close()
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