# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'studioemme.va.it'

xtr = '''title
<h1 class="entry-title">
</h1>
description
<div class="job_description">
<div class="job_application application">
city
"address":"
"'''

xtr_url = '''url
<a href=\\\\"
"'''

stp = '/offerta-lavoro'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://studioemme.va.it/jm-ajax/get_listings/',
        )
    }
     ),
)


# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()

def crawl(web): 

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    # sl.step(stp)
    headers = {
    "accept":"*/*",
    "accept-encoding":"gzip, deflate",
    "accept-language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "content-length":"631",
    "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
    "origin":"https://studioemme.va.it",
    "referer":"https://studioemme.va.it/annunci/",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "x-requested-with":"XMLHttpRequest",
    }
    req = requests.post(url=web, data="lang=&search_keywords=&search_location=&filter_job_type%5B%5D=apprendistato&filter_job_type%5B%5D=determinato&filter_job_type%5B%5D=indeterminato&filter_job_type%5B%5D=altro&filter_job_type%5B%5D=libero-professionista-partita-iva&filter_job_type%5B%5D=&per_page=20&orderby=featured&order=DESC&page=1&show_pagination=false&form_data=search_keywords%3D%26search_region%3D0%26filter_job_type%255B%255D%3Dapprendistato%26filter_job_type%255B%255D%3Ddeterminato%26filter_job_type%255B%255D%3Dindeterminato%26filter_job_type%255B%255D%3Daltro%26filter_job_type%255B%255D%3Dlibero-professionista-partita-iva%26filter_job_type%255B%255D%3D", headers=headers)
    data = req.text
    # print data
    # exit(0)

    sl.WR = ["virtual:{0}".format(data.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["{0}".format(re.sub("\\\\", "", x.get("url", ""))) for x in sl.M]

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
        ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", ""))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$", "", offer.get("title_aux", ""))

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
