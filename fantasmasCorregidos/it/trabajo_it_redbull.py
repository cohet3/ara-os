# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobs.redbull.com'

xtr = '''title
<title>
(-)
city

</title>
description
"description":"
"],"externalUrl"
extra
"location":{

company
"label":"
",
contract
"employmentType":"
"'''
xtr_url = '''id
"slug":"
",'''

stp = ''
page_ads = 11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
        'https://jobs-searchapi.eu-central-1.misc-production.redbullaws.com/graphql' ,
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
    headers = {
        "accept":"*/*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"es-ES,es;q=0.9,de-DE;q=0.8,de;q=0.7,en;q=0.6,it;q=0.5",
        "content-length":"802",
        "content-type":"text/plain;charset=UTF-8",
        "origin":"https://jobs.redbull.com",
        "referer":"https://jobs.redbull.com/",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"cross-site",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",

    }
    data = '''{"query":"query ($context: ContextInput, $search: SearchInput) {results: getSearchResults(search: $search, context: $context) {   count   resultSize    resultCountText    featuredMicrosite {      description      linkLabel      title      url      background {        image {          fullUrl          label        }     }    }    jobs {      title      function {        name      }      languages {      name       iso      }      locationText      locations {        name       type       iso      }     slug     workingTime    } }}","variables":{"context":{"country":"es","locale":"es"},"search":{"functions":[],"locations":["1646"],"keyword":"","pageSize":100,"page":1}}} '''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    # print datos
    # exit(0)
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    sl.extract(xtr_url)
    urls = ["https://jobs.redbull.com/it-it/{0}".format(x.get("id","")) for x in sl.M]
    urls = list(dict.fromkeys(urls))
    sl.WR = urls
    #Para pruebas
    #sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("\\\|\\\\r|\\\\t","", offer.get("description", ""))
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
