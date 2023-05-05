# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context


fetched_from = 'maersk.wd3.myworkdayjobs.com'

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
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["4e4d26638c45010787a1f311a2a00000","4e4d26638c45010787a1f144264d0000","4e4d26638c45010787a1f445d5520000"]}},"limit":20,"offset":0,"searchText":""}}' ,
        )
      }
    ),
)


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
        'Content-Length':'176',
        'Content-Type':'application/json',
        # 'Cookie':'wday_vps_cookie=2166789642.61490.0000; TS014c1515=01f6296304b7bcd6efeed7e1fe9afc3c520fe58d77cc9c40686d0cf08248ea0fb588b79453b6a5b85ec21dcf5a87d259dfa445df69; PLAY_SESSION=0acc51970d573089414a798e79331c4744c5f3cd-instance=wd3prvps0007d&maersk_pSessionId=54pjkhmoq51b53na24ejdm1rj8; timezoneOffset=-60; PLAY_LANG=es; wd-browser-id=c613bce2-df27-4817-8a64-13175d8989b8',
        'Host':'maersk.wd3.myworkdayjobs.com',
        'Origin':'https://maersk.wd3.myworkdayjobs.com',
        'Referer':'https://maersk.wd3.myworkdayjobs.com/es/Maersk_Manual/?locations=4e4d26638c45010787a1f311a2a00000&locations=4e4d26638c45010787a1f144264d0000&locations=4e4d26638c45010787a1f445d5520000',
        'sec-ch-ua':'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    req = requests.post(url='https://maersk.wd3.myworkdayjobs.com/wday/cxs/maersk/Maersk_Manual/jobs', headers=headers, data=web)
    datos = req.text

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://maersk.wd3.myworkdayjobs.com/es/Maersk_Manual{0}".format(x.get("url","")) for x in sl.M]

    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
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
        ad['city'] = re.sub(":.*$", "", offer.get("city", ""))
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
