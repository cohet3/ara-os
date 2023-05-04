# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'sensata.wd1.myworkdayjobs.com'

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
"'''

stp = ''
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://sensata.wd1.myworkdayjobs.com/Sensata-Careers/9/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        "Content-Length":"269",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"wday_vps_cookie=3307645450.8755.0000; TS014c1515=01560d0839f531390a23dc5416868f47e998d2fcf85285c275ef492a5bf0c519bc29cdaac94acb716caada28aaec494d40a561f738; PLAY_LANG=es; PLAY_SESSION=e25bdf8ffd21c9ac68dd297fd0a77e01b53704fc-sensata_pSessionId=5adgi69ra66tdvmlsk2qhe1kc1&instance=wd1prvps0006i; timezoneOffset=-120",
        "Host":"sensata.wd1.myworkdayjobs.com",
        "Origin":"https://sensata.wd1.myworkdayjobs.com",
        "Referer":"https://sensata.wd1.myworkdayjobs.com/Sensata-Careers/9/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"babce7bc18984e69919a0cec383f5223,725,0,",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.42.006",
    }

    headers2 = {
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"wday_vps_cookie=3307645450.8755.0000; TS014c1515=01560d0839f531390a23dc5416868f47e998d2fcf85285c275ef492a5bf0c519bc29cdaac94acb716caada28aaec494d40a561f738; PLAY_LANG=es; PLAY_SESSION=e25bdf8ffd21c9ac68dd297fd0a77e01b53704fc-sensata_pSessionId=5adgi69ra66tdvmlsk2qhe1kc1&instance=wd1prvps0006i; timezoneOffset=-120",
        "Host":"sensata.wd1.myworkdayjobs.com",
        "Referer":"https://sensata.wd1.myworkdayjobs.com/es/Sensata-Careers/job/Tijuana-Mexico/Material-Planning-Supervisor_IRC78790",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.42.006",
    }

    data = '''facets=locations&locations=locations%3A%3Ad151662782ed104009e1d3433bfc9d9d%2Clocations%3A%3Ad151662782ed10400b5b512443dfa3a7%2Clocations%3A%3A07fc7c539e55102ff0c529dda6d781a0&sessionSecureToken=6q2naoq7qmeqgeitfmasgbraj2&clientRequestID=6613bf0b651b4bf297486dc49188d2d9'''

    urls = []
    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    sl.extract(xtr_url)
    sl.WR = ["https://sensata.wd1.myworkdayjobs.com{0}?clientRequestID=34e2a88590da4a73a48f3ae949a58299".format(x.get("url","")) for x in sl.M]
    for x in sl.WR:
        urls.append(x)

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
        ad['description'] = re.sub("&nbsp;|&amp;", "", offer.get("description", ""))
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
