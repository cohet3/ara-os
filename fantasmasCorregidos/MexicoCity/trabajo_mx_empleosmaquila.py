# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2
from urllib import quote
from base_mx import db_es, slavy, text, dalek

fetched_from = 'empleosmaquila.com'

xtr_viewstate = '''viewstate
id="__VIEWSTATE" value="
"
viewstategenerator
id="__VIEWSTATEGENERATOR" value="
"
eventvalidation
id="__EVENTVALIDATION" value="
"'''

xtr = '''bad_title
<title>
</title>
company
<span id="LblTEmpresa">
</
title
<span id="LblSubject">
</
description
<span id="LblRequi">
<p>Puesto:
contract
<span id="LblTipoContrato">
</
salary
<span id="LblSalario">
</
province
<span id="LblTestado">
</
city
<span id="LblCiudad">
</'''

stp = 'viewjobpre.aspx\?JobID=\d{3,}'
page_ads = 20
page_stp = 1
pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 72))

pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.empleosmaquila.com/listaofertas.aspx?Ciudad=ALL&Search=' ,
        )
      }
    ),
)

def crawl(web):
    sl = slavy.slavy()
    sl.start('https://www.empleosmaquila.com/')
    sl.headers['Host'] = "www.empleosmaquila.com"
    sl.headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    sl.headers['Cookie'] = "ASP.NET_SessionId=re5ho4dsqh5sqpcnm4jjvjzu"
    sl.headers['Connection'] = "keep-alive"
    sl.headers['Upgrade-Insecure-Requests'] = "1"
    sl.headers['Accept-Language'] = "en-US,en;q=0.5"
    sl.headers['Accept-Encoding'] = "gzip, deflate, br"
    sl.headers['Referer'] = "https://www.empleosmaquila.com/listaofertas.aspx?Ciudad=ALL&Search="
    sl.headers['Content-Type'] = "application/x-www-form-urlencoded"
    sl.metaExtract = True
    sl.extract(xtr_viewstate)
    sl.WR = [web.format(viewstate = re.sub('/','%2F',quote(sl.M[0].get('viewstate',''))),viewstategenerator = re.sub('/','%2F',quote(sl.M[0].get('viewstategenerator',''))),eventvalidation = re.sub('/','%2F',quote(sl.M[0].get('eventvalidation',''))))]
    #sl.extract('')
    #sl.printM()
    #exit(0)
    sl.step(stp)
    
    sl.WR = ["https://www.empleosmaquila.com/viewjobpre.aspx?JobID={0}".format(re.sub('^.*?JobID=','',item)) for item in sl.WR]
    
    #Para pruebas
    #sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:3]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')
        
        salary = re.sub('\.00|\+.*?$|[A,a].*?$|\D','',offer.get("salary","0"))
        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = salary if salary else "0"
        ad['company'] = offer.get("company", "")
        
        if 'ompleto' or 'lance' or 'medio' in offer.get("contract", ""):
            ad['contract'] = offer.get("contract", "")

        yield ad

#saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug=False)
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
