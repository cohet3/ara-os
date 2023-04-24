# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_es import db_es, slavy, text, dalek
import libnacho
# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'vates.com'

xtr = '''title
"title":"
",
description
"description":"
",
contract
"workday":"
",
city
"es":"
",'''


xtr_url = '''url
"slug":"
"'''

stp = 'AAA'
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 10))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{page}',
        )
    }
     ),
)


def crawl(web):


    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    ########REQUESTS MULTIPART#########
    #sl.step(stp)
    headers= {
        'accept':'application/json',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'231',
        # 'content-type':'multipart/form-data; boundary=----WebKitFormBoundary9oY5C2BoQv0ORk3j',
        # 'cookie':'_ga=GA1.2.877005431.1637658580; _gid=GA1.2.1977950453.1637658580; _fbp=fb.1.1637658580248.448872610; locale=ImVzIg%3D%3D--cb82f065989e4c5ab2efb8670a59d862438a89c2; _session_id=1db6560e003cac9d1cfa720f682adc35',
        'origin':'https://careers.vates.com',
        'referer':'https://careers.vates.com/jobs',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        # 'x-csrf-token':'EKg29bEJ0OPYUNm80ab03Mof7bsBm+6auQLFK+yBESS1ULa2BmpKdIbJOmM51keQUUz4/a0NXLR+u2RRwuHySw==',
    }
    page = web
    files = {}
    files = {
        'page': (None, page, 'multipart/form-data', headers),
        'locale': (None, 'es', 'multipart/form-data', headers),
    }
    req = requests.get(url = 'https://careers.vates.com/jobs_preview',)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://careers.vates.com/jobs/{0}".format(x.get("url", "")) for x in sl.M]
    ##############################


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
        ad['description'] = re.sub("\\\\n","\n",libnacho.xhtml(re.sub("\\\\\u0026","&",re.sub("\\\\u003c.*?\\\\u003e","",offer.get("description", "")))))
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
