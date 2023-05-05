# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'noblecorp.wd1.myworkdayjobs.com'

xtr = '''extra
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

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://noblecorp.wd1.myworkdayjobs.com/wday/cxs/noblecorp/noblecorp/jobs' ,
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
        'Content-Length':'84',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=d9923bcc576b1aaf03f6512a0b652668f5805958-noblecorp_pSessionId=87gng2rc20h3e1c9hns94rd2ia&instance=wd1prvps0006a; wday_vps_cookie=3307645450.53810.0000; TS014c1515=01560d08399f488953b4601f409d0f847694f35b0e177253b9e072dfc312ce71ae05b39a4d4483931f04af20db8ba106df70ce9b37; timezoneOffset=-120; _ga=GA1.4.1349732563.1653899509; _gat=1; wd-browser-id=6d99f9ff-458a-4e36-aa4d-3c9b0827596d',
        'Host':'noblecorp.wd1.myworkdayjobs.com',
        'Origin':'https://noblecorp.wd1.myworkdayjobs.com',
        'Referer':'https://noblecorp.wd1.myworkdayjobs.com/es/noblecorp/jobs',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }


    data = '''{"appliedFacets":{"locations":["329cae01418a01981c4456a576d675a2"]},"searchText":""}'''

    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)
    
    sl.WR = ["https://noblecorp.wd1.myworkdayjobs.com/es/noblecorp{0}".format(x.get("url","")) for x in sl.M]

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
