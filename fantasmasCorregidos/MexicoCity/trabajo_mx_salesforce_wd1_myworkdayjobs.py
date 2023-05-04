# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'salesforce.wd1.myworkdayjobs.com'


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

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 40, 20))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["75727048dd2b1082bfba5ee91e27fd9f"]}},"limit":20,"offset":{page},"searchText":""}}' ,
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
        'Content-Length':'107',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=f04308b3e1a686fc1ff0d6e629102e6962b44676-salesforce_pSessionId=9l2b9h1fcllv9k5pnurjvufhjp&instance=wd1prvps0003a; PLAY_LANG=en-US; wday_vps_cookie=3425085962.53810.0000; TS014c1515=01dc4a3ac840f8292c5cff3b444b9ad2f86acc928b611ddf167709eb3da8e047a802c891f3921be5ad6533d4433fcecb220e69b20b; timezoneOffset=-120; wd-browser-id=d363ad67-67ae-4c76-8a38-2cf358f202e1',
        'Host':'salesforce.wd1.myworkdayjobs.com',
        'Origin':'https://salesforce.wd1.myworkdayjobs.com',
        'Referer':'https://salesforce.wd1.myworkdayjobs.com/en-US/External_Career_Site?locations=75727048dd2b1082bfba5ee91e27fd9f',
        'sec-ch-ua':'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }


    req = requests.post(url = 'https://salesforce.wd1.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs', headers = headers, data = web)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://salesforce.wd1.myworkdayjobs.com/en-US/External_Career_Site{0}".format(x.get("url", "")) for x in sl.M]

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
        ad['description'] = re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", ""))))))))
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
