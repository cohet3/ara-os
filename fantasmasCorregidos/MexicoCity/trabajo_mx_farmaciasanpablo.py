# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'farmaciasanpablo-careers.com'

xtr = '''title
<title>
</title>
company
"hiringOrganization" content="
"
city
<span class="jobGeoLocation">
(\(|</span>)
description
class="jobdescription">
<p class="job-location">'''

stp = '/job/'
page_ads = 16

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://farmaciasanpablo-careers.com/search/?q=&q2=&alertId=&locationsearch=Mexico&title=&location=Mexico&date=' ,
        )
      }
    ),
)

#def renew():
    #torproxy.renew(controller)
    #torproxy.connect()
    #print "mi ip: ",torproxy.show_my_ip()
def crawl(web):
    #renew()
    #sl.inputEncoding = 'latin1' # 'iso-8859-1'
    #sl.outputEncoding = 'utf-8'
    #sl.headers['Host'] = ""
    #sl.headers['User-Agent'] = ""
    #sl.headers['Accept'] = ""
    #sl.headers['Accept-Language'] = ""
    #sl.headers['Accept-Encoding'] = ""
    #sl.headers['Cookie'] = ""
    #sl.headers['Referer'] = ""
    #sl.headers['Content-Type'] = ""
    #sl.headers['Content-Length'] = ""
    #sl.start('')
    #-------------
    #response = urllib2.urlopen(web)
    #html = response.read()
    #sl = slavy.slavy()
    #sl.start(web)
    #sl.metaExtract = True
    #sl.WR = ["virtual:{0}".format(html)]
    #sl.extract(xtr)
    #-------------
    #req = urllib2.Request(url=url, headers=sl.headers, data=data)
    #response= urllib2.urlopen(req)
    #html = response.read()
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    #~ buf = StringIO(response.read())
    #~ f = gzip.GzipFile(fileobj=buf)
    #~ html = f.read()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    #sl = slavy.slavy()
    #sl.start(web)
    #sl.metaExtract = True
    #sl.WR = ["virtual:{0}".format(html)]
    #sl.extract(xtr)
    #-------------
    #sl.WR = [web]
    #sl.polite(0,1)

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    sl.step(stp)

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
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
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
