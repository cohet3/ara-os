# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from =  "getecsa"

xtr = '''city
city:"
"
title
job:\{name:"
",
description
"GBP",".*?","
","https:'''

xtr_url = '''url
"slug":"
",'''

stp = '\?Id='

page_ads = 12

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2) )
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://albatross.recruitcrm.io/v1/external-pages/jobs-by-account/get?account=Getecsa_jobs',
        )
      }
    ),
)

def crawl(web):
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    ########REQUESTS POST#########
    #sl.step(stp)
    headers= {
        'accept':'application/json, text/plain, */*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'2',
        'content-type':'application/json;charset=UTF-8',
        'origin':'https://recruitcrm.io',
        'referer':'https://recruitcrm.io/',
        'sec-ch-ua':'"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-site',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    }
    data ='''{}'''
    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://recruitcrm.io/apply/{0}?source=Jobspage".format(x.get("url", "")) for x in sl.M]
    ##############################
    # sl.extract('')
    #Para pruebas
    # sl.printWR()    
    # sl.printM()
    #sl.printstatus()
    # sl.WR = sl.WR[0:3]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['url'] = offer.get("@url", "")
        ad['title'] = re.sub("\\\\u002F","/",offer.get("title", ""))
        ad['company'] = offer.get("company", "Getecsa")
        
        if offer.get("city") == "D.F.":
            ad['city'] = "Ciudad de México"
        else:
            ad['city'] = re.sub("\\\\u002F","/",offer.get("city", ""))
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary", "")
        ad['contract'] = offer.get("contract", "")
        ad['description'] =re.sub("\\\\n","",re.sub("\\\\u002F","/",re.sub("\\\\u003C.*?\\\\u003E","",offer.get("description", ""))))

        yield ad

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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug=debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
