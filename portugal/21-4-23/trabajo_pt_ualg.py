# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_pt import db_pt, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'www.ualg.pt'

xtr = '''title
<title>
[|]
description
<div class="field field--name-field-descricao field--type-string-long field--label-hidden field--item">
</article>'''
xtr_url='''url
<td headers="view-field-descricao-table-column" class="views-field views-field-field-descricao"><a href="
"'''
stp = ''
page_ads = 11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.ualg.pt/procedimentos-concursais' ,
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
    # sl.step(stp)
    req =requests.get(url=web)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://www.ualg.pt/procedimentos-concursais{0}".format(x.get('url', '')) for x in sl.M]

    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit()
    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("⦁", "-", offer.get("description", ""))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary",'0')
        ad['company'] = re.sub("-", "", offer.get("company", "Universidade do Algarve"))
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
