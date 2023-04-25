# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'hp.wd5.myworkdayjobs.com'

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

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 200, 20))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"primaryLocation":["336ea9b27e9910b218d5896bc8f0e9c6","336ea9b27e9910b218d51e07b822e9b0","1f4e0f81ca5801a1f1205bdc1806c131"]}},"limit":20,"offset":{page},"searchText":""}}' ,
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
        'Content-Length':'160',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=fc257ecf79223cdf6b3b4488ded9b3dfc230189f-hp_pSessionId=dad9i38jeiedmmkj9tcqlm74uh&instance=wd5prvps0002h; wday_vps_cookie=2904961546.6195.0000; timezoneOffset=-120; PLAY_LANG=es; TS014c1515=018b6354fe6638ceb7eee7101e6e5c39a2fc05be63477f7795ab231cb5ecf4e8e73a529d1b7ddbc80d591186c18f4d71f5ce2ef1b0; wd-browser-id=6b5ef97d-a40a-4538-8887-35215099712e',
        'Host':'hp.wd5.myworkdayjobs.com',
        'Origin':'https://hp.wd5.myworkdayjobs.com',
        'Referer':'https://hp.wd5.myworkdayjobs.com/en-US/ExternalCareerSite?primaryLocation=1f4e0f81ca5801a1f1205bdc1806c131',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }


    req = requests.post(url='https://hp.wd5.myworkdayjobs.com/wday/cxs/hp/ExternalCareerSite/jobs', headers=headers, data=web)
    datos = req.text
    # print datos
    # exit(0)
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    
    sl.extract(xtr_url)
    
    sl.WR = ["https://hp.wd5.myworkdayjobs.com/en-US/ExternalCareerSite{0}".format(x.get("url","")) for x in sl.M]


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
