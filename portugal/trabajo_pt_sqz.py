# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_pt import db_pt, slavy, text, dalek
import libnacho
# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'sqs.zohorecruit.eu'

xtr = '''salary
\\\\x22Salary\\\\x22\\\\x3A\\\\x22
\\\\x22,
city
\\\\x22City\\\\x22\\\\x3A\\\\x22
\\\\x22,
description
\\\\x22Job_Description\\\\x22\\\\x3A\\\\x22
\\\\x22,
title
\\\\x22Job_Opening_Name\\\\x22\\\\x3A\\\\x22
\\\\x22,'''

xtr_url = '''url
Country&quot;&#x3a;&quot;Portugal&quot;,&quot;id&quot;&#x3a;&quot;
&quot;'''

stp = 'jobs/Careers'
page_ads = 11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://sqs.zohorecruit.eu/',
        )
    }
     ),
)



def crawl(web):

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    ########REQUESTS GET##########
    sl.step(stp)
    req = requests.get(url = web)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://sqs.zohorecruit.eu/jobs/Careers/{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = libnacho.urls(sl.WR)
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

        title = urllib2.unquote(offer.get("title", "").decode('unicode-escape'))
        ad['title'] = re.sub("\\\\u201d",'"',re.sub("<.*?>", "", HTMLParser.HTMLParser().unescape(title)))
        description = urllib2.unquote(offer.get("description", "").decode('unicode-escape'))
        ad['description'] = re.sub("\\\\u20ac",'Euros ',re.sub("\\\\u201d",'"',re.sub("<.*?>", "", HTMLParser.HTMLParser().unescape(description))))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        salary = urllib2.unquote(offer.get("salary", "").decode('unicode-escape'))
        ad['salary'] = re.sub("\\\\u20ac",'Euros ',re.sub("\\\\u20acliq",'"',re.sub("<.*?>", "", HTMLParser.HTMLParser().unescape(salary))))
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()

