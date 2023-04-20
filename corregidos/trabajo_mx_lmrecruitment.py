# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context
import libnacho

fetched_from = 'lmrecruitment.zohorecruit.com'

xtr = '''city
\\\\x22City\\\\x22\\\\x3A\\\\x22
\\\\x22,
description
\\\\x22Job_Description\\\\x22\\\\x3A\\\\x22
\\\\x22,
contract
\\\\x22Job_Type\\\\x22\\\\x3A\\\\x22
\\\\x22,
title
\\\\x22Job_Opening_Name\\\\x22\\\\x3A\\\\x22
\\\\x22,
province
\\\\x22State\\\\x22\\\\x3A\\\\x22
\\\\x22,'''

xtr_url = '''url
Baja&#x20;California&quot;,&quot;Country&quot;&#x3a;&quot;Mexico&quot;,&quot;id&quot;&#x3a;&quot;
&quot;'''

stp = '/jobs/Careers/'
page_ads = 11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://lmrecruitment.zohorecruit.com/jobs/Careers' ,
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
    ########REQUESTS GET##########
    #sl.step(stp)
    req = requests.get(url = web)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://lmrecruitment.zohorecruit.com/jobs/Careers/{0}".format(x.get("url", "")) for x in sl.M]
    ##############################
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    # sl.extract(xtr)

    # if not len(sl.M):
    #     raise Exception('[WARN] Empty Model')
    for url in sl.WR:
        # print url
        # url = 'https://p2prh.zohorecruit.com/recruit/PortalDetail.na?iframe=true&digest=qLSO.uQAQX5K@eyyPdWNpHGAUnkE7bVo.a85bxdBEmQ-&jobid=481541000015068398&widgetid=481541000000072311&embedsource=CareerSite'
        req = requests.get(url)
        datos = req.text
        # print datos
        # exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)
        for offer in sl.M:
                
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

            ad['title'] = offer.get("title", "").decode("unicode-escape").encode("utf-8")
            ad['description'] = re.sub(";", "\n", libnacho.xhtml(offer.get("description", "").decode("unicode-escape").encode("utf-8")))
            ad['url'] = url
            ad['city'] = offer.get("city", "").decode("unicode-escape").encode("utf-8")
            ad['province'] = offer.get("province", "").decode("unicode-escape").encode("utf-8")
            ad['salary'] = offer.get("salary",'0')
            ad['company'] = offer.get("company", "")
            ad['contract'] = offer.get("contract", "").decode("unicode-escape").encode("utf-8")

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
