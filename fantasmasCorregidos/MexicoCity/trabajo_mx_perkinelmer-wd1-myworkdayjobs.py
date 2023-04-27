# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'perkinelmer.wd1.myworkdayjobs.com'

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
            'https://perkinelmer.wd1.myworkdayjobs.com/wday/cxs/perkinelmer/External/jobs' ,
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
        'Content-Length':'104',
        'Content-Type':'application/json',
        # 'Cookie':'wd-browser-id=337cf7f6-99d3-4341-a930-ccdb4600c924; PLAY_SESSION=b0b91bd2a72b2fc65bc02469f74ebce6e7ea00f6-perkinelmer_pSessionId=iqv8pbnb7rqni3iq13nn3jhmfu&instance=wd1prvps0004c; wday_vps_cookie=3441863178.58930.0000; TS014c1515=01560d083903114d9be1c98a725b03121c8a40771bf6b7be79d794247838c982d9733a76adf552754e10b7a5ff7a04668b9ffde124; timezoneOffset=-120; _ga=GA1.4.141975882.1653918729; _gat=1',
        'Host':'perkinelmer.wd1.myworkdayjobs.com',
        'Origin':'https://perkinelmer.wd1.myworkdayjobs.com',
        'Referer':'https://perkinelmer.wd1.myworkdayjobs.com/en-US/External?Country=e2adff9272454660ac4fdb56fc70bb51',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }


    data = '''{"appliedFacets":{"Country":["e2adff9272454660ac4fdb56fc70bb51"]},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://perkinelmer.wd1.myworkdayjobs.com/en-US/External{0}".format(x.get("url","")) for x in sl.M]

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
