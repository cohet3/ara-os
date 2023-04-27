# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'smartnfinal.com.mx'

xtr = '''title
<title>
</title>
description
<h1 class=".*?">
<span class=
extra
<h5>Ciudad</h5>

city
<p>
</p>'''
#<h5>Ciudad</h5><p>Tijuana</p>1486
xtr_url = '''url
<a href="https://www.smartnfinal.com.mx/empleo/
">'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.smartnfinal.com.mx/bolsa-de-trabajo/' ,
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

    req = requests.get(url = web, verify = False)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://www.smartnfinal.com.mx/empleo/{0}".format(x.get("url", "")) for x in sl.M]
    #Para pruebas
    #sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("Â", "", re.sub("Ã¡", "á",re.sub("Ã©", "é", re.sub("Ã­", "í",re.sub("Ã³", "ó",re.sub("Ãº", "ú",re.sub("Ã", "Á", re.sub("Ã", "É",re.sub("Ã", "Í", re.sub("Ã±", "ñ", re.sub("Ã", "Ñ", re.sub("Ã", "Ö", re.sub("Ã", "Ü", re.sub("Ã¼", "ü", re.sub("â", "", re.sub("â|â", " - ", re.sub("â¦", "...", re.sub("â", "\"", re.sub("â", "\"", re.sub("â", "'", re.sub("â¢", "·", offer.get("description", "").decode("unicode-escape").encode("utf-8"))))))))))))))))))))))
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
