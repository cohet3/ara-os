# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'motorolasolutions.wd5.myworkdayjobs.com'

xtr = '''city
"addressLocality" : "
"
extra
"identifier" : {

company
"name" : "
"
title
"title" : "
"
description
"description" : "
",
contract
"employmentType" : "
"'''

xtr_url = '''url
"externalPath":"
",'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://motorolasolutions.wd5.myworkdayjobs.com/wday/cxs/motorolasolutions/Careers/jobs' ,
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
    #sl.step(stp)

    headers = {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'90',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=55778fca88f7dcda4f0803af52dc581a4a103556-motorolasolutions_pSessionId=q5cir9kpm2vr77l83feptl2o43&instance=wd5prvps0004c; wday_vps_cookie=2938515978.58930.0000; TS014c1515=018b6354fee41c9c65f5bfbce88747f03d8667dbec677ac8e148336ba6309ee8238d10ed672f7ba3ebd4ddd80ec823372870ba877f; timezoneOffset=-120; wd-browser-id=cdcf4e0f-1e3a-40ea-b0c1-1563f58f805f',
        'Host':'motorolasolutions.wd5.myworkdayjobs.com',
        'Origin':'https://motorolasolutions.wd5.myworkdayjobs.com',
        'Referer':'https://motorolasolutions.wd5.myworkdayjobs.com/es/Careers',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    data = '''{"appliedFacets":{"locationCountry":["e2adff9272454660ac4fdb56fc70bb51"]},"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://motorolasolutions.wd5.myworkdayjobs.com/es/Careers{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls

    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", ""))))))))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
