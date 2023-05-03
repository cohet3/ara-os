# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'aptiv.com'

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

stp = ''
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://aptiv.wd5.myworkdayjobs.com/APTIV_Careers/0/refreshFacet/318c8bb6f553100021d223d9780d30be' ,
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

    headers= {
    'Accept':'application/json,application/xml',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'es-ES,es;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'163',
    'Content-Type':'application/x-www-form-urlencoded',
    #'Cookie':'PLAY_SESSION=d17a8d35c17bb064cfa147edf0c45983a6e07969-aptiv_pSessionId=3i66hlscp43sol8akde8c3214q&instance=wd5prvps0001a; wday_vps_cookie=2888184330.53810.0000; timezoneOffset=-120; PLAY_LANG=en-US',
    'Host':'aptiv.wd5.myworkdayjobs.com',
    'Origin':'https://aptiv.wd5.myworkdayjobs.com',
    'Referer':'https://aptiv.wd5.myworkdayjobs.com/APTIV_Careers/3/refreshFacet/318c8bb6f553100021d223d9780d30be',
    'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile':'?0',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'stats-perf':'39176ae2bf4b4ef0ae6bb0b5ef3d928c,1261,0,',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'workday-client-manifest-id':'mvp',
    'X-Workday-Client':'2021.20.011',
    }

    data = '''facets=Country&Country=Country%3A%3Ae2adff9272454660ac4fdb56fc70bb51'''

    req = requests.post(url = 'https://aptiv.wd5.myworkdayjobs.com/APTIV_Careers/3/replaceFacet/318c8bb6f553100021d223d9780d30be', headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://aptiv.wd5.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    print "Total de enlaces " + str(len(sl.WR))
    # exit(0)


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
