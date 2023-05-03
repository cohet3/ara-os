# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'levistraussandco.wd5.myworkdayjobs.com'

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
"'''

stp = ''
page_ads = 48

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["c4fc5e1b31d40164a12903cd51017dc3","0d4da4dc87120151bd5fa261fd018061","517def9c1c0f0117b38b6c4f4b01c7be","0d4da4dc871201ee5abc935ffd01ef60","3652e0f1df580104df8fd2de5101a7ed","cf6792ac2be91087525ffba7a8c3bb47","cf6792ac2be91087526f5df40cfbc762","a77c19161eeb010e6b68ec5cfd016522","0d4da4dc871201a4a5041560fd010d61","517def9c1c0f01ff4a0979504b010abf"]}},"searchText":""}}' ,
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
        'Content-Length':'84',
        'Content-Type':'application/json',
        # 'Cookie':'wday_vps_cookie=2921738762.8755.0000; TS014c1515=018b6354fed7d3ed36525a612232385180ea506dff816baba2b1eab55e5105d0a4eaa13f310bd0355ee33bee2a5fe0127d9e6cf6b0; PLAY_SESSION=dfb34302f90751d962a8a892e9936dc4d2f20eb2-levistraussandco_pSessionId=f7rbanmqoe5uvm9332ce9qqi51&instance=wd5prvps0003i; wd-browser-id=c5c765d6-4abc-4b00-92b9-413db040021e; timezoneOffset=-120',
        'Host':'levistraussandco.wd5.myworkdayjobs.com',
        'Origin':'https://levistraussandco.wd5.myworkdayjobs.com',
        'Referer':'https://levistraussandco.wd5.myworkdayjobs.com/es/External/jobs',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }
    
    req = requests.post(url = 'https://levistraussandco.wd5.myworkdayjobs.com/wday/cxs/levistraussandco/External/jobs', headers = headers, data = web)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://levistraussandco.wd5.myworkdayjobs.com/es/External{0}".format(x.get("url", "")) for x in sl.M]

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
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub('&#43;', '+', re.sub("&#39;", "'", re.sub('&amp;', '&', re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")))))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$", "", offer.get("title_aux", ""))

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
