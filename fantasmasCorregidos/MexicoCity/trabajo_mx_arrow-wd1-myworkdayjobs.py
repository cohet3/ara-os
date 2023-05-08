# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'arrow.wd1.myworkdayjobs.com'

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
            'https://arrow.wd1.myworkdayjobs.com/AC/1/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        'Accept':'application/json,application/xml',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'190',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Cookie':'wday_vps_cookie=3408308746.58930.0000; TS014c1515=01560d08396e216a916d7d5089642d4583143c4e2ac944385745e06d5db57935885d5a2d2e7d0de10be08f4fc0bac0eaa1959df356; PLAY_SESSION=213b0d6d085277da1fb67e1325462bd0fc9b18f7-arrow_pSessionId=gi1kjl4qqos7flkbgqfu1p2mlp&instance=wd1prvps0002c; PLAY_LANG=es; timezoneOffset=-120',
        'Host':'arrow.wd1.myworkdayjobs.com',
        'Origin':'https://arrow.wd1.myworkdayjobs.com',
        'Referer':'https://arrow.wd1.myworkdayjobs.com/AC/1/refreshFacet/318c8bb6f553100021d223d9780d30be',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'Session-Secure-Token':'ud5s674khme86poea3slog1lot',
        'stats-perf':'b39c9e5cf5494afc83e5aa7e7a9ffaaa,129,0,',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Workday-Client':'2022.22.7',
    }

    data = '''facets=Location_Country&Location_Country=Location_Country%3A%3Ae2adff9272454660ac4fdb56fc70bb51&sessionSecureToken=ud5s674khme86poea3slog1lot&clientRequestID=0cbf1f8304be45aba81e93efebef255c'''

    req = requests.post(url=web, headers=headers, data=data)
    datos = req.text
    
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://arrow.wd1.myworkdayjobs.com{0}".format(x.get("url","")) for x in sl.M]

   
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
        ad['description'] = re.sub("&#39;", "'", re.sub("&nbsp;|&amp;", "", offer.get("description", "")))
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
