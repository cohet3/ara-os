# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
import libnacho
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobs.stationf.com'
#EXTRACTO DESPUES DEL HTTPS

xtr = '''title
<title>
</title>
city
<i class='icon-secondary icon-location'>
</li>
description
Job Description
<div class='block block-job-text block-job-more'>
contract
Contract Type:
</strong>
province
Location:
</strong>'''
#BUSCAR CODIGO FUENTE DE LA OFERTA Y RASTREAR

xtr_url='''url
"slug":"
"'''
#EN PAGINA CON LAS OFERTAS, BUSCAR ID OFERTA -> RESPONSE BUSCAR ID 

stp = '/companies/'
#CODIGO COMUN A LAS OFERTAS
page_ads = 18 
#NUMERO DE OFERTAS POR PAGINA + 1
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))  #NUMERO DE PAGINAS + 1
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"requests":[{{"indexName":"wk_cms_jobs_production","params":"query=italy&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&maxValuesPerFacet=100&page=0&facets=%5B%22contract_type_names.en%22%2C%22organization.name%22%2C%22office.city%22%2C%22department%22%5D&tagFilters="}}]}}',
            #BUSCAR ID OFERTA POOST-> PAYLOAD -> VIEW SOURCE Y PONER EL {{PAGE}} DONDE CORRESPONDA
        )
    }
     ),
)

def crawl(web): 

    sl = slavy.slavy()
    #sl.start(web)
    sl.metaExtract = True
    #sl.step(stp)                                                  #ESTE METODO SI LAS OFERTAS SON GET
 
    ############################################################   #ESTE CODIGO SI LAS OFERTAS SON POST (REQUESTSPOST)
    headers= {
        'accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '296',
        'content-type': 'application/x-www-form-urlencoded',
        'Host': 'csekhvms53-dsn.algolia.net',
        'Origin': 'https://jobs.stationf.co',
        'Referer': 'https://jobs.stationf.co/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    }
    #BUSCAR ID OFERTA -> HEADERS -> REQUEST HEADERS Y PONERLO EN FORMATO PYTHON
    
    req = requests.post(url = 'https://csekhvms53-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.0.0)%3B%20JS%20Helper%20(0.0.0-5a0352a)&x-algolia-application-id=CSEKHVMS53&x-algolia-api-key=YzZjN2MzMWQ5OGZiZTcwOGRiMjA4YTc1ZmQ2ZTZhYWQ4Yzk3MDEzNmZhZjdiYWU0M2JmMDcwM2I1NTNhMWZmYmZpbHRlcnM9d2Vic2l0ZS5yZWZlcmVuY2UlM0FzdGF0aW9uLWYtam9iLWJvYXJk', headers = headers, data = web)
    #EL URL LO SACAMOS DE BUSCAR ID OFERTA -> HEADERS -> REQUEST URL
    #datos = req.text
    #print datos
    #exit(0)

    datos = req.json()['results']
    sl.WR=[]

    #print datos 
    #exit(0)

    for d in datos:
        for c in d['hits']:
            if 'italy' in c['office']['country'].lower():

                #print c['office']['country']
                #print c['organization']['website_organization']['slug'] 
                #print c['slug']
                #exit(0)
        
                sl.WR.append('https://jobs.stationf.co/companies/{0}/jobs/{1}'.format(c['organization']['website_organization']['slug'],c['slug']))
        

    

    #sl.printWR()                        #Para pruebas
    # sl.printM()
    # sl.printstatus()
    #sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = libnacho.emojis(re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        try:
            variable= offer.get("province", "").split(',')
            variable2=variable[0]                
            ad['province'] = ''.join(variable2)      
        except:     
            ad['province'] = offer.get("province", "")
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
