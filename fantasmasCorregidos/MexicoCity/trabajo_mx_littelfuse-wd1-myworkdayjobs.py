# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'littelfuse.wd1.myworkdayjobs.com'

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

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://littelfuse.wd1.myworkdayjobs.com/wday/cxs/littelfuse/Littelfuse-Careers/jobs' ,
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
        # 'Cookie':'PLAY_SESSION=146ad9d72f4bb651d34f2486585394a637293d49-littelfuse_pSessionId=u665jdh9gvb40k91nvbvs890a9&instance=wd1prvps0001g; wday_vps_cookie=3391531530.3635.0000; TS014c1515=01560d0839f610447ee4bd4d21d81b1e6f8bb29cea073610222ce5188dc04dbaee96da44f6f0f4c4552cfd5d31ddcc8de300bfa3f9; timezoneOffset=-120; wd-browser-id=cb180788-05b9-4904-ad29-f0d16466e0c7',
        'Host':'littelfuse.wd1.myworkdayjobs.com',
        'Origin':'https://littelfuse.wd1.myworkdayjobs.com',
        'Referer':'https://littelfuse.wd1.myworkdayjobs.com/es/Littelfuse-Careers',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    }


    data = '''{"appliedFacets":{"locations":["c88db239144910970dd9bdc053ac273d"]},"searchText":""}'''

    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://littelfuse.wd1.myworkdayjobs.com/es/Littelfuse-Careers{0}".format(x.get("url","")) for x in sl.M]


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
