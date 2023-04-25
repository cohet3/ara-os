# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'spgi.wd5.myworkdayjobs.com'

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
            'https://spgi.wd5.myworkdayjobs.com/SPGI_Careers/0/replaceFacet/318c8bb6f553100021d223d9780d30be' ,
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
        "Content-Length":"232",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"PLAY_LANG=en-US; PLAY_SESSION=0de7e39c1c362d0a0c08f079b43fc3b560f980aa-spgi_pSessionId=er962i4s2mflhl9a5i2cs27pso&instance=wd5prvps0003e; wday_vps_cookie=2921738762.64050.0000; TS014c1515=014c0a46f4e7d8fab713275231ddcb101f5d17dd7585d45fd6a12abd06a318747f22ca9130acb813825f6af7dbbeefed2ca4b7f2e5; timezoneOffset=-120",
        "Host":"spgi.wd5.myworkdayjobs.com",
        "Origin":"https://spgi.wd5.myworkdayjobs.com",
        "Referer":"https://spgi.wd5.myworkdayjobs.com/SPGI_Careers/0/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"44ba5b9445264825885cb18c97400b87,201,0,",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.42.006",
    }

    data = '''facets=Location_Region_State_Province&Location_Region_State_Province=Location_Region_State_Province%3A%3A4c151630730401f53cfbd6d8586390b8'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://spgi.wd5.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
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
        separador = url.split("/")
        urlpre = "/".join(separador[0:6])
        urlpost = "".join(separador[-1])
        url = str(urlpre) + '/' + str(urlpost)
        # print url
        # exit(0)
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'PLAY_SESSION=ff297c6dd6831d61387287b169b4203abfa92689-spgi_pSessionId=gp6j0i97kboathfmep0hrldijb&instance=wd5prvps0002b; wday_vps_cookie=2904961546.56370.0000; TS014c1515=018b6354fe8c0f1d0c5ae41b68098d103650a453438e5cf817799bde69068b8b46d261d9699bb6c4670a3b8fd85bf6eac450092780; timezoneOffset=-60; enablePrivacyTracking=false; wd-browser-id=38f3a211-d44c-428d-93e8-f7f0f0bf971d',
            'Host':'spgi.wd5.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        # print datos
        # exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            # ad['description'] = re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", ""))))))))
            ad['description'] = offer.get("description", "")
            ad['url'] = url
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
