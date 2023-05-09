# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'diageo.wd3.myworkdayjobs.com'

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
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 60, 20))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["ce314b15e11d017b6bd2f8648878a12c","ce314b15e11d0175efc627af917808a8"]}},"limit":20,"offset":{page},"searchText":""}}' ,
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
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'142',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=56284ac56961213757b65dcf686d5c7e64f05fc5-diageo_pSessionId=g5eojugqrhipb15ajm0fqnmhcq&instance=wd3prvps0005d; PLAY_LANG=es; wday_vps_cookie=2586220042.61490.0000; TS014c1515=01f62963049cc14a8f16469577afcef011e80ffdbfbb9e12f069cd0cd08b50dfbdb94da3f48c2425e2f4861604a762a8ecc2a9c2d7; timezoneOffset=-120; wd-browser-id=e47baf34-37db-41e0-98bf-7cbd5deb688d',
        'Host':'diageo.wd3.myworkdayjobs.com',
        'Origin':'https://diageo.wd3.myworkdayjobs.com',
        'Referer':'https://diageo.wd3.myworkdayjobs.com/es/Diageo_Careers?locations=ce314b15e11d017b6bd2f8648878a12c&locations=ce314b15e11d0175efc627af917808a8',
        'sec-ch-ua':'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    req = requests.post(url = 'https://diageo.wd3.myworkdayjobs.com/wday/cxs/diageo/Diageo_Careers/jobs', headers = headers, data = web)
    datos = req.text

    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://diageo.wd3.myworkdayjobs.com/es/Diageo_Careers{0}".format(x.get("url","")) for x in sl.M]

    # Para pruebas
    #sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

   
    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub('<p style="text-|&amp;|&nbsp;', "", re.sub("<.*?>", "", re.sub("&lt;", "<", re.sub("&gt;", ">", offer.get("description", "").decode("unicode-escape").encode("latin")))))
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
