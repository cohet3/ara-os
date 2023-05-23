# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'convatec.wd1.myworkdayjobs.com'

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
            'https://convatec.wd1.myworkdayjobs.com/ConvaTec/0/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        #"Cookie":"wday_vps_cookie=2888184330.8755.0000; TS014c1515=014c0a46f416b7f55e827c9597d62151cee6e7a3b41a17be644fd076297200016164217222440d3b312fea3ba70e0d667e6f55e641; PLAY_LANG=es; PLAY_SESSION=ef7ba3433fce0672d27e7b43a10cb26b0a6aa9b9-equifax_pSessionId=sl80nc2m1m5moklcqfl5vt5mpg&instance=wd5prvps0001i; timezoneOffset=-60",
        "Host":"convatec.wd1.myworkdayjobs.com",
        "Origin":"https://convatec.wd1.myworkdayjobs.com",
        "Referer":"https://convatec.wd1.myworkdayjobs.com/gileadcareers/4/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"347015a70f6d430b8ccaa36ebcbdd6fd,1015,0,",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.43.011",
    }

    data = '''facets=Location_Country&Location_Country=Location_Country%3A%3A8cd04a563fd94da7b06857a79faaf815'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://convatec.wd1.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls
    #Para pruebas
    # sl.printWR()
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
            # 'Cookie':'wd-browser-id=d2a18ff3-c684-43dc-9c16-78cdf4daa078; PLAY_SESSION=27ad19ee3f9881a3f79b3b1c93a2d1eb28f76054-convatec_pSessionId=i3u567tdsu8gpa202s537htinp&instance=wd1prvps0007b; wday_vps_cookie=3324422666.56370.0000; TS014c1515=01560d0839d8508abd927ce0da37d21f0d8e17d420910fc540be180b14f212d2a74db10c49c277b489fccfa6365a27838deccf320b; timezoneOffset=-120',
            'Host':'convatec.wd1.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        #print datos
        #exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("\\\\","",re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", "")))))))))
            ad['url'] = url
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


    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
