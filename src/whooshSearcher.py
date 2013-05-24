# -*- coding: utf-8 -*-
from whoosh.index import create_in,open_dir
from whoosh.fields import *
import os.path
from whoosh.qparser import QueryParser
from whoosh.query import *
import sys,traceback

class whooshSearcher:
    
    ix = ""
    writer = ""  
    
    def __init__(self,newIndex):
        if newIndex == True:
            self.addSchema()
        else:
            self.ix=open_dir("index")   
    
    
    
    def addSchema(self):
        schema = Schema(title=TEXT(stored=True), url=ID(stored=True), content=TEXT(stored=True))
        if not os.path.exists("index"):
            os.mkdir("index")
        self.ix = create_in("index", schema)
    
    def addDocument(self,newsTitle,newsUrl,newsContent):
        self.writer = self.ix.writer()
        self.writer.add_document(title=newsTitle, url=newsUrl,content=newsContent)
        self.writer.commit()
        
    def search(self,queryString):
        try:
            with self.ix.searcher() as searcher:
                #query = Or([Term("content","added"),Term("content","algorithm")])
                parser = QueryParser("content", self.ix.schema)
                myQuery = parser.parse(queryString)
                #print list(searcher.lexicon("content"))
                results = searcher.search(myQuery)
                if (len(results)==0):
                       print u"No matches found."
                else:
                    print "Numbers of matches: "+str(len(results))
                    for r in results:
                        print str(r)
                    
        except:
            print "Problems with the result."
            print traceback.print_exc(file=sys.stdout)