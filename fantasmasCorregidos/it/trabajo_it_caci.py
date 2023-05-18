# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'caci.wd1.myworkdayjobs.com'

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

stp = '/job/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://caci.wd1.myworkdayjobs.com/wday/cxs/caci/External/jobs',
        )
    }
     ),
)


# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()

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
		'Content-Length':'106',
		'Content-Type':'application/json',
		# 'Cookie':'wd-browser-id=66aae72d-571b-4639-af21-02512412dfb8; PLAY_SESSION=19ab48968204b01a1c0b3b8b99ac0f68aa847b01-caci_pSessionId=sup1v871nj2d832pqhrb19uev8&instance=wd1prvps0006f; wday_vps_cookie=3307645450.1075.0000; TS014c1515=01560d0839c2aff732e8dee2a9f0426ede94709a81e0357b3a993fd9c130fcd9608364ffb1566645f59c5b31bcdada1ae611852481; timezoneOffset=-120',
		'Host':'caci.wd1.myworkdayjobs.com',
		'Origin':'https://caci.wd1.myworkdayjobs.com',
		'Referer':'https://caci.wd1.myworkdayjobs.com/External?locations=c2c3b59666d2015fd4c811c9ea963010',
		'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-platform':'"Windows"',
		'Sec-Fetch-Dest':'empty',
		'Sec-Fetch-Mode':'cors',
		'Sec-Fetch-Site':'same-origin',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }

    data = '''{"appliedFacets":{"locations":["c2c3b59666d2015fd4c811c9ea963010"]},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://caci.wd1.myworkdayjobs.com/en-US/External{0}".format(x.get("url", "")) for x in sl.M]
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit(0)

    # if not len(sl.WR):
    #     raise Exception('[WARN] Empty web region')

    # sl.extract(xtr)

    # if not len(sl.M):
    #     raise Exception('[WARN] Empty Model')

    for url in sl.WR:
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=9a0ce7c8-0d61-4c8e-a058-bb64431a9bef; PLAY_SESSION=66d1e364b00d617853cc30b11d286250b76d0500-kone_pSessionId=22us23o4l0166llj6qn0aa0c43&instance=wd3prvps0003e; wday_vps_cookie=2753992202.64050.0000; TS014c1515=01f629630491441804b2429560aa3538aee47840e6cb90666a1486e2fdefe7df78800fa1b3318baad626443246356fc84207983cb2; timezoneOffset=-120',
            'Host':'caci.wd1.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        # print datos
        # exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("iso-8859-1"))]
        sl.extract(xtr)
        # sl.printM()
        # exit(0)
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


# saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug=False)
# saltcellar.crawl = crawl
# saltcellar.exterminate()

# new code for test auto debug script
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


    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
