# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'studiocpa.it'

xtr = '''title
<title>
</title>
description
<div class="awsm-job-content">
</div>
city
"address":"
"'''

xtr_url='''url
">		<a href="
"'''
stp = ''
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 4))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'action=loadmore&paged={page}&listings_per_page=10',
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
    #sl.step(stp)

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'44',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie':'_iub_cs-70989776=%7B%22timestamp%22%3A%222022-10-04T11%3A08%3A49.107Z%22%2C%22version%22%3A%221.41.0%22%2C%22purposes%22%3A%7B%221%22%3Atrue%2C%222%22%3Atrue%2C%223%22%3Atrue%2C%224%22%3Atrue%2C%225%22%3Atrue%7D%2C%22id%22%3A%2270989776%22%7D; usprivacy=%7B%22uspString%22%3A%221YN-%22%2C%22firstAcknowledgeDate%22%3A%222022-10-04T11%3A08%3A49.104Z%22%2C%22optOutDate%22%3Anull%7D',
        'Host':'www.studiocpa.it',
        'Origin':'https://www.studiocpa.it',
        'Referer':'https://www.studiocpa.it/offerte-di-lavoro/',
        'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }

    req = requests.post(url = 'https://www.studiocpa.it/wp-admin/admin-ajax.php', headers = headers, data = web, verify = False)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["{0}".format(x.get("url", "")) for x in sl.M]
    
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
