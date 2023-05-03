# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'orange.jobs'

xtr = '''city
<span class="location_workplace">
<span.*?
title
"title":"
",
description
"description":"
",
country
"addressCountry":"
"}'''

xtr_url = '''url
"joid":
,
country
"countriestitle":"
",'''

stp = 'offer.do?joid='
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://orange.jobs/jobs/v3/search?keyword=mexico' ,
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
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9",
        "Connection":"keep-alive",
        "Content-Length":"101",
        "Content-Type":"application/json",
        "Cookie":"JSESSIONID=E66057B075AF19AD62F04802E211BA70; __utmz=195751154.1599729979.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=195751154.1708318940.1599729979.1599807649.1600074995.4; huaweielbsession=3972071d6d830378ae1964e4e18c6944",
        "Host":"orange.jobs",
        "Origin":"https://orange.jobs",
        "Referer":"https://orange.jobs/jobs/search.do?lang=EN",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
    }

    data = '''{"index":"1","nb":"60","latmin":"","latmax":"","lngmin":"","lngmax":"","carto":"","place":["ID:3204"]}'''

    req = requests.post(url='https://orange.jobs/jobs/flux/offers/search?lang=en', headers=headers, data=data)
    datos = req.text
    urls = []
    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]
    sl.extract(xtr_url)
    for x in sl.M:
        if 'Mexico' in x.get("country", ""):
            urls.append("https://orange.jobs/jobs/offer.do?joid={0}".format(x.get("url", "")))
    
    sl.WR = urls

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
