# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context
from StringIO import StringIO
import gzip
from base_br import db_br, slavy, text, dalek
import libnacho

fetched_from = 'telhanortesaintgobain.pandape.infojobs.com.br'

xtr = '''title
<title>
</title>
contract
"employmentType": "
",
description
"description": "
",
company
"name": "
"
city
"addressLocality": "
",
salary
"minValue":
,'''

stp = '/Detail/'
page_ads = 20
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 6))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://telhanortesaintgobain.pandape.infojobs.com.br/?PageNumber={page}&PageSize=20' ,
        )
      }
    ),
)

#def renew():
    #torproxy.renew(controller)
    #torproxy.connect()
    #print "mi ip: ",torproxy.show_my_ip()
def crawl(web):
    
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    sl.step(stp)
       
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit()

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = libnacho.xhtml(libnacho.emojis(offer.get("description", '')).decode('unicode-escape').encode('latin'))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary",'0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")
        
        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$","",offer.get("title_aux",""))
            
        if not ad["salary"]:
            ad["salary"] = 0

        yield ad

#saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug=False)
#saltcellar.crawl = crawl
#saltcellar.exterminate()

#new code for test auto debug script
if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        debug_mode = True
    elif len(sys.argv) < 2:
        debug_mode = False
    else:
        print "usage: python filename.py (test)"
        print "example for test: python <filename.py> test "
        print "example for run: python <filename.py>"
        exit(1)

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_br, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
