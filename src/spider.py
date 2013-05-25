# -*- coding: utf-8 -*-
import os, re, sqlite3, sys; sys.path.insert(0, os.path.join("..", ".."))
from datetime import datetime
from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL,plaintext,DOM
from django.utils.encoding import smart_str, smart_unicode
from whooshSearcher import *

class WhooshSpider(Spider):
    
    def __init__(self, links, domains, delay, whoosh):
        Spider.__init__(self, links=links, domains=domains, delay=delay)
        self.whoosh=whoosh
    
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
                    result = result + plainText + '\n '
                    
        pretty = unicode(result.strip())
        return pretty
        
    
    def visit(self, link, source=None):
        match = re.search("huffingtonpost.co.uk/\d{4}/\d{2}/\d{2}/", link.url)
        if match:
            splitted_url = link.url.split('/')
            article_date = datetime.datetime(int(splitted_url[3]), int(splitted_url[4]), int(splitted_url[5]))
            title = splitted_url[6].split('_')[0]
            encodedContent = self.htmlParser(link.url)
            self.whoosh.addDocument(title, link.url, article_date, encodedContent)
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
