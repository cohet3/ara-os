# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'ingredion.wd1.myworkdayjobs.com'

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
"commandLink":"
",'''

stp = '/job/'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://ingredion.wd1.myworkdayjobs.com/IngredionCareers/fs/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9",
        "Connection":"keep-alive",
        "Content-Length":"163",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"PLAY_LANG=es; PLAY_SESSION=ee91d0d90ea44b2f1903503794f45a9a94a44fa7-ingredion_pSessionId=6kuatp6rfbri3ajsqvrqooa5kr&instance=wd1prvps0007c; wday_vps_cookie=3324422666.58930.0000; timezoneOffset=-120; TS014c1515=01560d08395b9fdce6dc34511983c79ec595de6652087fa36b45332c14953448fb1864d76ed929453e1ba4c56e6b52b053cb8dbd9f",
        "Host":"ingredion.wd1.myworkdayjobs.com",
        "Origin":"https://ingredion.wd1.myworkdayjobs.com",
        "Referer":"https://ingredion.wd1.myworkdayjobs.com/es/IngredionCareers",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"5792fc575a644a309f26e976573016d5,770,0,0",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.41.009",
    }

    data = '''facets=Country&Country=Country%3A%3Ae2adff9272454660ac4fdb56fc70bb51&sessionSecureToken=i4mmqegjs8pekuf8c62e3ad5hr&clientRequestID=9531f259d6124e909eb79e144fea2c40'''

    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    sl.extract(xtr_url)
    sl.WR = ["https://ingredion.wd1.myworkdayjobs.com{0}".format(x.get("url","")) for x in sl.M]

    # Para pruebas
    #sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

   
    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
