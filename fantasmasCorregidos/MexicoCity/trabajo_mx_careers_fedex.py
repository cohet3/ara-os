# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'careers.fedex.com'

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

stp = ''
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 80, 20))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"Location_Country":["e2adff9272454660ac4fdb56fc70bb51"]}},"limit":20,"offset":{page},"searchText":""}}' ,
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
        'Accept-Language':'en-US',
        'Connection':'keep-alive',
        'Content-Length':'113',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=f82cb039210b6b4313dcef5d8dbd784bc2416653-fedex_pSessionId=bnk2o9ttgdl2rdp87c1s4fou5c&instance=wd1prvps0002e; wday_vps_cookie=3408308746.64050.0000; TS014c1515=01dc4a3ac84a83f5d8434fcefb6115e3fa9cd09e0703923e15a76ef518bafa519fad20740d9a02e1c2a874f197fc2dbfd42e92bd27; timezoneOffset=-60; wd-browser-id=68cd9837-8df1-4c58-9663-576774e41e0f',
        'Host':'fedex.wd1.myworkdayjobs.com',
        'Origin':'https://fedex.wd1.myworkdayjobs.com',
        'Referer':'https://fedex.wd1.myworkdayjobs.com/FXE-LAC_External_Career_Site?Location_Country=e2adff9272454660ac4fdb56fc70bb51',
        'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    req = requests.post(url = 'https://fedex.wd1.myworkdayjobs.com/wday/cxs/fedex/FXE-LAC_External_Career_Site/jobs', headers = headers, data = web)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://fedex.wd1.myworkdayjobs.com/en-US/FXE-LAC_External_Career_Site{0}".format(x.get("url","")) for x in sl.M]
    

    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

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
        ad['city'] = re.sub("^.*?/.*?/.*? ", "", offer.get("city", ""))
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
