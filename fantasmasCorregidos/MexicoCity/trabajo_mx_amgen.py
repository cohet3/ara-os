# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'amgen.wd1.myworkdayjobs.com'

xtr_url = '''url
"externalPath":"
"'''

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


stp = 'AAA'
page_ads = 18

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://amgen.wd1.myworkdayjobs.com/wday/cxs/amgen/Careers/jobs' ,
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
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'84',
        'Content-Type':'application/json',
        #'Cookie':'PLAY_SESSION=4b0a8694dbff082fc1fc1a84270b9be51928197e-amgen_pSessionId=skiehuh12k0iarct4e7uh6hebb&instance=wd1prvps0006d; wday_vps_cookie=3307645450.61490.0000; TS014c1515=01560d083986bd33f51c36a95b34bd0f86616c6ac14d346d3b2290c8075058496a8b08956f8028f1c33f63a76ce56e4b29e18c3962; wd-browser-id=f2f363c1-d320-4830-96a4-3f6b9068427f; timezoneOffset=-120',
        'Host':'amgen.wd1.myworkdayjobs.com',
        'Origin':'https://amgen.wd1.myworkdayjobs.com',
        'Referer':'https://amgen.wd1.myworkdayjobs.com/es/Careers',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    data ='''{"appliedFacets":{"locations":["be0893cb78ed017dab4f57e68144bc3c"]},"limit":20,"offset":0,"searchText":""}'''
    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://amgen.wd1.myworkdayjobs.com/es/Careers{0}".format(x.get("url", "")) for x in sl.M]

    # Para pruebas
    #sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    #sl.extract(xtr)

    #if not len(sl.M):
        #raise Exception('[WARN] Empty Model')

    for url in sl.WR:
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'PLAY_SESSION=4b0a8694dbff082fc1fc1a84270b9be51928197e-amgen_pSessionId=skiehuh12k0iarct4e7uh6hebb&instance=wd1prvps0006d; wday_vps_cookie=3307645450.61490.0000; timezoneOffset=-120; TS014c1515=01560d08395b97e5ddbeee72cacfd18ab410ae839586bbbbefc311b39255f5461c7fc241483b5e5cfdcefd22b4f736d2404939f9f2; wd-browser-id=3cc33460-48a9-4964-af0b-124700189a81',
            'Host':'amgen.wd1.myworkdayjobs.com',
            'Referer':'https://amgen.wd1.myworkdayjobs.com/es/Careers?locations=be0893cb78ed017dab4f57e68144bc3c',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)

        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = offer.get("description", "")
            ad['url'] = url
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
