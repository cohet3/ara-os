# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek

# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'fourseasons.wd3.myworkdayjobs.com'

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

stp = 'AAA'
page_ads = 15
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 60, 20))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["1f5f2b443c2d4612ab405619408ef8be"]}},"limit":20,"offset":{page},"searchText":""}}',
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

#################POST#################
    headers= {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US',
        'Connection':'keep-alive',
        'Content-Length':'107',
        'Content-Type':'application/json',
        # 'Cookie':'wday_vps_cookie=2166789642.61490.0000; TS014c1515=01f6296304f56c6db0532a266a71edca3ffdbe8b382e50e04332c15192ba882bd412dbd8e52e293e83978df8dc1ce09c67e4a189de; wd-browser-id=7bd83d3e-dbca-46c6-8dfe-175f1bbc26b2; PLAY_SESSION=cc7343fe333ffad9d92e39c56ccfac3da217b14c-fourseasons_pSessionId=gg8n6foqosl9tkf9isrfhfr3c2&instance=wd3prvps0007d; timezoneOffset=-120',
        'Host':'fourseasons.wd3.myworkdayjobs.com',
        'Origin':'https://fourseasons.wd3.myworkdayjobs.com',
        'Referer':'https://fourseasons.wd3.myworkdayjobs.com/en-US/search/jobs?locations=1f5f2b443c2d4612ab405619408ef8be',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    }

    req = requests.post(url = 'https://fourseasons.wd3.myworkdayjobs.com/wday/cxs/fourseasons/search/jobs', headers = headers, data = web)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://fourseasons.wd3.myworkdayjobs.com/en-US/search{0}".format(x.get("url", "")) for x in sl.M]

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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
