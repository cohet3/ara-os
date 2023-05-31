# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek, torproxy
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

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://arrow.wd1.myworkdayjobs.com/AC/0/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9,de-DE;q=0.8,de;q=0.7,en;q=0.6,it;q=0.5",
        "Connection":"keep-alive",
        "Content-Length":"190",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"PLAY_LANG=en-US; PLAY_SESSION=feb98f40b0d18eb086a0f54d5c2d4a48d33bf4e3-ncr_pSessionId=ihehdk8rvj1l02310u15p6n6oh&instance=wd1prvps0003d; wday_vps_cookie=3425085962.61490.0000; TS014c1515=01560d0839e42790910fec09e249769df9cb6bb7901ed8c62de986cb7fc228074d0b72f1da4965a52f80ac62f212c45c9245b51c37; timezoneOffset=-60",
        "Host":"arrow.wd1.myworkdayjobs.com",
        "Origin":"https://arrow.wd1.myworkdayjobs.com",
        "Referer":"https://arrow.wd1.myworkdayjobs.com/ext_non_us/1/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"282cf03832984196bfc7405252d6bdc9,118,0,",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.44.012",
    }

    data = '''facets=Location_Country&Location_Country=Location_Country%3A%3A8cd04a563fd94da7b06857a79faaf815'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://arrow.wd1.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls
    #Para pruebas
    #sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    #exit(0)

    # if not len(sl.WR):
    #     raise Exception('[WARN] Empty web region')

    # sl.extract(xtr)

    # if not len(sl.M):
    #     raise Exception('[WARN] Empty Model')

    for url in urls:
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=9a0ce7c8-0d61-4c8e-a058-bb64431a9bef; PLAY_SESSION=66d1e364b00d617853cc30b11d286250b76d0500-kone_pSessionId=22us23o4l0166llj6qn0aa0c43&instance=wd3prvps0003e; wday_vps_cookie=2753992202.64050.0000; TS014c1515=01f629630491441804b2429560aa3538aee47840e6cb90666a1486e2fdefe7df78800fa1b3318baad626443246356fc84207983cb2; timezoneOffset=-120',
            'Host':'arrow.wd1.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        #print datos
        #exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("iso-8859-1"))]
        sl.extract(xtr)
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", ""))))))))
            ad['url'] = url
            try:
                separacion = offer.get("city", "").split(",")
                ad['city'] = separacion[0]
            except:
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
