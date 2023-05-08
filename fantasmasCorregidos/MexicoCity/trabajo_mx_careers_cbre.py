# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'careers.cbre.com'

xtr = '''duplicados
<title>
</title>
title
<div class="article__content__view__field view--title">
</div>
extra
Areas of Interest

city
<article class="article article--details regular-fields--cols-2Ͷ view--separator-custom-w-bar article--separator-not js_collapsible">.*?<div class="article__content__view__field__value">
</div>
description
<article class="article article--details regular-fields--cols-2Ͷ view--separator-custom-w-bar js_collapsible">.*?<div class="article__content__view__field__value">
</article>'''

xtr_url = '''url
<a href="https://careers.cbre.com/en_US/careers/JobDetail/
"'''

stp = '/JobDetail/ -mailto'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 25, 6))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://careers.cbre.com/en_US/careers/SearchJobs/?9577=%5B17181%5D&9577_format=10224&listFilterMode=1&jobRecordsPerPage=6&jobOffset={page}' ,
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
    sl.extract(xtr_url)
    sl.WR = []
    for url in sl.M:
        sl.WR.append('https://careers.cbre.com/en_US/careers/JobDetail/{0}'.format(url.get('url', '')))

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
        if len(offer.get("description", "")) > 10:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub(' +', ' ', re.sub(' ', ' ', offer.get("description", "")))
            ad['url'] = offer.get("@url", "")
            ad['city'] = re.sub(" -.*$", "", offer.get("city", ""))
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
