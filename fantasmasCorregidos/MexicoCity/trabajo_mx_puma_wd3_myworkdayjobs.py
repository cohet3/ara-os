# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'puma.wd3.myworkdayjobs.com'

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

xtr_url='''url
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
            'https://puma.wd3.myworkdayjobs.com/Jobs_at_Puma/1/refreshFacet/318c8bb6f553100021d223d9780d30be' ,
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

    headers={
    'Accept':'application/json,application/xml',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'es-ES,es;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'190',
    'Content-Type':'application/x-www-form-urlencoded',
    #'Cookie':'_ga=GA1.4.1707333300.1620663334; PLAY_LANG=es; PLAY_SESSION=fc6dbfe51c6cddd7ed9ba7963c75361a51f8b736-puma_pSessionId=7ppp3cva37cie8utioa5e3nkt2&instance=wd3prvps0002g; wday_vps_cookie=2737214986.3635.0000; timezoneOffset=-120; _gat=1',
    'Host':'puma.wd3.myworkdayjobs.com',
    'Origin':'https://puma.wd3.myworkdayjobs.com',
    'Referer':'https://puma.wd3.myworkdayjobs.com/Jobs_at_Puma/0/refreshFacet/318c8bb6f553100021d223d9780d30be',
    'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile':'?0',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'stats-perf':'befbd91fa9f74d30bc2e22ac001b4a37,168,0,',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'workday-client-manifest-id':'mvp',
    'X-Workday-Client':'2021.19.005',
    }

    data = '''facets=Location_Country&Location_Country=Location_Country%3A%3Ae2adff9272454660ac4fdb56fc70bb51'''

    req = requests.post(url = 'https://puma.wd3.myworkdayjobs.com/Jobs_at_Puma/0/replaceFacet/318c8bb6f553100021d223d9780d30be', headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://puma.wd3.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
    # sl.printWR()
    # exit(0)

    for url in sl.WR:

        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=a00c0877-2827-4b31-925d-2334ab181295; PLAY_SESSION=20336af7245146bacf10f33dbb50799561d60ca1-puma_pSessionId=9ir9a2iafp8694593s5tivu4r7&instance=wd3prvps0004a; wday_vps_cookie=2569442826.53810.0000; TS014c1515=01f629630435ed263892602800c7dd009acc8002d73f4f51cf524a70d8011e56f64063cd3e4122406bf4777355f8680998e53e0326; timezoneOffset=-120; _ga=GA1.4.733697891.1649675361; _gat=1',
            'Host':'puma.wd3.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        }

        req = requests.get(url,headers=headers)
        datos = req.text
        # print datos
        # exit(0)

        sl.WR = ["virtual:{0}".format(datos.encode("iso-8859-1"))]

        sl.extract(xtr)
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = offer.get("description", "")
            ad['url'] = url
            ad['city'] = offer.get("city", "")
            ad['province'] = offer.get("province", "")
            ad['salary'] = offer.get("salary", '0')
            ad['company'] = offer.get("company", "") # "Puma"
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
