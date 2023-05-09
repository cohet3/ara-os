# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'baxter.wd1.myworkdayjobs.com'

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


stp = '/get_vacancy/'
page_ads = 11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 60, 20))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"Country":["e2adff9272454660ac4fdb56fc70bb51"]}},"limit":20,"offset":{page},"searchText":""}}' ,
        )
      }
    ),
)


def crawl(web):
    
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    
    ########REQUESTS POST#########
    #sl.step(stp)
    headers= {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'104',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=4e3289a450106f6a77f87bb635b714586dcdf43d-baxter_pSessionId=ckd24ni94dmqulbiefhb24ghk1&instance=wd1prvps0003b; wday_vps_cookie=3425085962.56370.0000; TS014c1515=01dc4a3ac8c8ad0e5398d04fc597f0b6520eae3e9415ea211adf073d58fb2bc6aab066c7bc677948cdbcbdf709adb5f0c19942b1d5; PLAY_LANG=es; timezoneOffset=-60; enablePrivacyTracking=true; wd-browser-id=8d6a0612-713b-42a1-9f71-1dcd9001b405',
        'Host':'baxter.wd1.myworkdayjobs.com',
        'Origin':'https://baxter.wd1.myworkdayjobs.com',
        'Referer':'https://baxter.wd1.myworkdayjobs.com/es/baxter?redirect=/baxter/job/Tijuana-Baja-California/Gerente-de-Moldes-y-Tool-room_JR-082337/apply&Country=e2adff9272454660ac4fdb56fc70bb51',
        'sec-ch-ua':'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    req = requests.post(url = 'https://baxter.wd1.myworkdayjobs.com/wday/cxs/baxter/baxter/jobs', data = web, headers=headers)
    datos = req.text
    # print datos
    # exit(0)
    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://baxter.wd1.myworkdayjobs.com/es/baxter{0}".format(re.sub("\\\\", "", y.get("url",""))) for y in sl.M]


    #Para pruebas
    #sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "").decode('unicode-escape').encode('UTF-8')
        ad['description'] = re.sub('\\\\', '', re.sub('\\\\p', '\p', re.sub('\\\\t', '\t', re.sub('\\\\n', '\n', offer.get("description", "")))))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary",'0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")
        
        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$","",offer.get("title_aux",""))
            
        if not ad["salary"]:
            ad["salary"] = 0

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
