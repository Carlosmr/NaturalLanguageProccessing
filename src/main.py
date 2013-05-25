# -*- coding: utf-8 -*-
from whooshSearcher import *

w = WhooshSearcher(False)
answer="y"
while (answer=="y"):
    query=raw_input("What do you want to search?\n")
    w.search(unicode(query))
    answer = raw_input("\nSomething else?(y/n)\n")

    

