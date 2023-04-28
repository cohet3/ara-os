# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests, datetime
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'coyote.wd5.myworkdayjobs.com'

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

stp = 'AAA'
page_ads = 15

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://coyote.wd5.myworkdayjobs.com/coyotecareers/1/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'169',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Cookie':'PLAY_SESSION=014aeb62d704760e5f2036730441132f9bf84674-coyote_pSessionId=np03cb21rubceli8thss1uqi2e&instance=wd5prvps0007h; PLAY_LANG=en-US; wday_vps_cookie=2485531146.6195.0000; TS014c1515=018b6354fe2b803abbd8a15e21addd3b929505aa785397b200e2f5c8556872b683cbb447f244efc0326ad7795a02d57ba05e303500; timezoneOffset=-120',
        'Host':'coyote.wd5.myworkdayjobs.com',
        'Origin':'https://coyote.wd5.myworkdayjobs.com',
        'Referer':'https://coyote.wd5.myworkdayjobs.com/coyotecareers/1/refreshFacet/318c8bb6f553100021d223d9780d30be',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'Session-Secure-Token':'9cq72u9sbtk28vqaoabrm897ro',
        'stats-perf':'c0cc321ba55b4a219897347af2758ee3,209,0,',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Workday-Client':'2022.22.7',
    }

    data ='''facets=locations&locations=locations%3A%3Ab80218277ff7016679e1116271aa7d12&sessionSecureToken=9cq72u9sbtk28vqaoabrm897ro&clientRequestID=5b4f467d110d43c7aa4d6e101e634577'''
    
    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://coyote.wd5.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]

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
