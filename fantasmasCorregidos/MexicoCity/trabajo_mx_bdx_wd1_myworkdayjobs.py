# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'bdx.wd1.myworkdayjobs.com'

xtr = '''title
"title" : "
"
description
"description" : "
",
contract
"employmentType" : "
"
company
"name" : "
"
city
"addressLocality" : "
"'''

xtr_url = '''url
"externalPath":"/job/.*?/
"'''
token='''token
token: "
"'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://bdx.wd1.myworkdayjobs.com/wday/cxs/bdx/EXTERNAL_CAREER_SITE_MEXICO/jobs' ,
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
            'Content-Length':'58',
            'Content-Type':'application/json',
            'Cookie':'PLAY_SESSION=67c16b0dd1b2fa2c4fefeaae6518769b6b6b6e99-bdx_pSessionId=n0jd3t7e96vrfj0l5i136a2t5d&instance=wd1prvps0006g; PLAY_LANG=es; wday_vps_cookie=3307645450.3635.0000; timezoneOffset=-120; enablePrivacyTracking=true; wd-browser-id=42b04e31-a89e-44ca-bbad-27581e280813; CALYPSO_CSRF_TOKEN=74017a21-d5ba-40da-aa47-74729da5de0d; TS014c1515=01dc4a3ac8c49ea4e08adbef88d78e324bb1fa1500db7e24c75f5b0cc594f9f594d41027b5ceaa133d873e74b146273b7f742f7a93',
            'Host':'bdx.wd1.myworkdayjobs.com',
            'Origin':'https://bdx.wd1.myworkdayjobs.com',
            'Referer':'https://bdx.wd1.myworkdayjobs.com/es/EXTERNAL_CAREER_SITE_MEXICO',
            'sec-ch-ua':'"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-CALYPSO-CSRF-TOKEN':'74017a21-d5ba-40da-aa47-74729da5de0d',
    }

    data = '''{"appliedFacets":{},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://bdx.wd1.myworkdayjobs.com/es/EXTERNAL_CAREER_SITE_MEXICO/job/MEX-Cuautitlan-Izcalli/{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls
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
        ad['description'] = re.sub("&#43;", "+", re.sub("&nbsp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", "")))))))))
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
