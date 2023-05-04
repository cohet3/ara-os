# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'dofiscal-editores.sherlockhr.computrabajo.com'

xtr = '''title
<title>
</title>
description
<p class="mt30 t_word_wrap">
<h3 class="mt20 fwB">Resumen del empleo</h3>
extra
<div class="vt"><span class="icon i_address"></span></div>
<div class="w100 pl15">
city

</div>
extra
<div class="vt"><span class="icon i_salary"></span></div>
<div class="w100 pl15">
salary

</div>
extra
<div class="vt"><span class="icon i_workday"></span></div>
<div class="w100 pl15">
contract

</div>'''

xtr_url = '''url
<h3 itemprop="title" class="fs20"><a itemprop="url" href="
">'''

stp = '/ofertas/'
page_ads = 36

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://dofiscal-editores.sherlockhr.computrabajo.com/ofertas/' ,
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
    sl.step(stp)
    headers = { 
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'es-ES,es;q=0.9',
        'cache-control':'no-cache',
        # 'cookie':'_ga=GA1.2.1426512509.1679648492; _gid=GA1.2.1410057348.1680089608; __RequestVerificationToken=Vl2_k3HAbrBNhs92liHUlReQRi5jE3MOlH3kRI-lCkiPvMICU4VcpoNpRNKZ2B5rT7gUs0cLR-8bescNnVf89PuvIf01; SCV=SID=02',
        'pragma':'no-cache',
        'referer':'https://dofiscal-editores.sherlockhr.computrabajo.com/ofertas/',
        'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'script',
        'sec-fetch-mode':'no-cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    data='''v=oxq446KY_M1HRSJz1N80DhWSP9rwsH5AJKRggWGSjro1'''
    req =requests.get(url=web, data=data, headers=headers)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://dofiscal-editores.sherlockhr.computrabajo.com{0}".format(x.get('url', '')) for x in sl.M]

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