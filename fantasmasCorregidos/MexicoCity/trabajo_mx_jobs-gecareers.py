# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobs.gecareers.com'

xtr = '''extra
"ml_title":"

company
"Organization","name":"
"
city
"addressLocality":"
"
contract
"employmentType":"
",
description
"description":"
",
title
"title":"
",'''

xtr_url = '''url
"jobId":"
",'''

stp = '/job/'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://jobs.gecareers.com/global/en/search-results' ,
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
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'434',
        'content-type':'application/json',
        # 'cookie':'PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJmNTFlOTE0MS04NDk4LTRlNTgtYjAzYi1kNWU0MmQwNTk5MjYifSwibmJmIjoxNjM4MzQyODQ1LCJpYXQiOjE2MzgzNDI4NDV9.w4AYbcOgrN5pCTF6A3NM-8MOFGkbz8lRcuF0eYQYe4k; JSESSIONID=f51e9141-8498-4e58-b03b-d5e42d059926; VISITED_LANG=en; VISITED_COUNTRY=global; _gcl_au=1.1.1669309192.1638342846; Per_UniqueID=17d74d7e56acd-100200-1e16-17d74d7e56b4c5; _ga=GA1.3.773903269.1638342846; _gid=GA1.3.2075009161.1638342846; ext_trk=pjid%3Df51e9141-8498-4e58-b03b-d5e42d059926&uid%3D17d74d7e56acd-100200-1e16-17d74d7e56b4c5&p_lang%3Den_global&refNum%3DGE11GLOBAL; _fbp=fb.1.1638342846677.801534842; PHPPPE_GCC=a; _ga=GA1.2.773903269.1638342846; _gid=GA1.2.2075009161.1638342846; _gat_UA-167196821-1=1',
        'origin':'https://jobs.gecareers.com',
        'referer':'https://jobs.gecareers.com/global/en/search-results',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'x-csrf-token':'ea31a557b2f54fe6b0689d3091537362',
    }

    data = '''{"lang":"en_global","deviceType":"desktop","country":"global","pageName":"search-results","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","business","experienceLevel"],"size":20,"clearAll":false,"jdsource":"facets","isSliderEnable":false,"pageId":"page1","siteType":"external","keywords":"","global":true,"selected_fields":{"country":["Mexico"]}}'''

    req = requests.post(url='https://jobs.gecareers.com/widgets', headers=headers, data=data)
    datos = req.text
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    sl.extract(xtr_url)
    sl.WR = ["https://jobs.gecareers.com/global/en/job/{0}".format(x.get("url","")) for x in sl.M]

    # Para pruebas
    # sl.printWR()
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
        ad['description'] = offer.get("description", "").decode("unicode-escape").encode("utf-8")
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
