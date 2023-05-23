# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
import libnacho
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'enirecruit.taleo.net'

xtr = '''city
"addressRegion":"
"
title
"title":"
"
description
"description":"
",'''

#busca en la oferta, description":

xtr_url='''url
"contestNo":"
"'''
#el valor de la url es el diccionario "contestNo:" "IRC218313"

stp = '/jobdetail.ftl?job='
page_ads = 44 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://enirecruit.taleo.net/careersection/rest/jobboard/searchjobs?lang=en&portal=10205100322',
            #la sacas de Request URL (en headers, introduciendo el codigo de una de las ofertas)
        )
    }
     ),
)


# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()

def crawl(web): 

    #cookies=libnacho.get_cookies('slavy','https://enirecruit.taleo.net')
    #print cookies
    #exit(0)

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    #sl.step(stp)

    ########REQUESTS POST#########
    headers= {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'539',
        'Content-Type':'application/json',
        # 'Cookie':'locale=en; _ga=GA1.2.1351237635.1648706871; _gid=GA1.2.1672466540.1648706871; _gat_UA-96904592-25=1; __atuvc=4%7C12%2C3%7C13; __atuvs=62454554d090c922002',
        'Host':'enirecruit.taleo.net',
        'Origin':'https://enirecruit.taleo.net',
        'Referer':'https://enirecruit.taleo.net/careersection/ext/jobsearch.ftl?lang=en',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'tz':'GMT+02:00',
        'tzname':'Europe/Madrid',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',

        #lo sacas de Request Headers
    }
    payload = '''{"multilineEnabled":false,"sortingSelection":{"sortBySelectionParam":"1","ascendingSortingOrder":"false"},"fieldData":{"fields":{"KEYWORD":"","LOCATION":""},"valid":true},"filterSelectionParam":{"searchFilterSelections":[{"id":"LOCATION","selectedValues":["354205013364"]},{"id":"JOB_FIELD","selectedValues":[]}],"activeFilterId":"LOCATION"},"advancedSearchFiltersSelectionParam":{"searchFilterSelections":[{"id":"ORGANIZATION","selectedValues":[]},{"id":"LOCATION","selectedValues":[]},{"id":"JOB_FIELD","selectedValues":[]}]},"pageNo":1}'''
    #lo sacas de payload -> view source
    req = requests.post(url = web, headers = headers, data = payload)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]
    sl.extract(xtr_url)
    sl.WR = ["https://enirecruit.taleo.net/careersection/ext/jobdetail.ftl?job={0}".format(x.get("url", "")) for x in sl.M]
    #lo sacas de la url de la oferta 
    ##############################

    # Para pruebas
    sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    #sl.extract(xtr)

    #if not len(sl.M):
        #raise Exception('[WARN] Empty Model')

    for url in sl.WR:

        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Cookie':'restoreQuery=true; savedQuery=%7B%22queryString%22%3A%22f%253Dnull%2526s%253D1%257CD%2526a%253Dnull%2526multiline%253Dfalse%22%7D; locale=it; JSESSIONID=Oa7V6AyDzPXIaKd8syN0IZV6IDzvcvgnw5oo4-8LnFAa1nrZeMWi!-833403120; _ga=GA1.2.321810941.1648560426; _gid=GA1.2.857266122.1648560426; __atssc=google%3B2; __atuvc=24%7C13; __atuvs=62431d1b68efda07009',
            'Host':'enirecruit.taleo.net',
            'Referer':'https://enirecruit.taleo.net/careersection/ext/jobsearch.ftl',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        }

        req = requests.get(url, headers=headers)
        datos = req.text
        #print datos
        #exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)
    
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                    published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", ""))
            ad['url'] = url                               #esto se cambia
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
