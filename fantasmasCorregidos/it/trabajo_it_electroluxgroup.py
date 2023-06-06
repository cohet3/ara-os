# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek, torproxy
from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'career.electroluxgroup.com'

xtr = '''extra
</title>

company
"name":"
"
city
"addressLocality":"
"
description
"ExternalDescription":"
",
title
"title":"
"'''

xtr_url = '''url
"reqId":"
"'''

stp = '/careers/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
    # pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://career.electroluxgroup.com/widgets',
        )
    }
     ),
)


# def renew():
    # torproxy.renew(controller)
    # torproxy.connect()
    # print "mi ip: ",torproxy.show_my_ip()

def crawl(web): 

    # renew()
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    # sl.step(stp)
    
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'426',
        'content-type':'application/json',
        # 'Cookie':'VISITED_LANG=en; VISITED_COUNTRY=global; Per_UniqueID=142672e9-f2e5-4f96-8073-2ae5ef456b4b181b3eb827d; OptanonAlertBoxClosed=2022-06-30T09:22:47.371Z; PHPPPE_GCC=a; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiIwMzYzYTlhYy03M2U5LTQyZmYtYmFmNi0wMTU2MWY2MmQ3NjQifSwibmJmIjoxNjYxNzcxMjUxLCJpYXQiOjE2NjE3NzEyNTF9.a_OAZajcBJ2Zg3hFpY_NCHPwHPAvBB59SQas76DALKg; JSESSIONID=0363a9ac-73e9-42ff-baf6-01561f62d764; bm_mi=D5A74E63F1182963BE482291712723B7~YAAQ9n4WAtVuyLOCAQAAJAVJ6RCgVrI2oQ3YMAULf972DnVejQ+VmNmXkt+utMaIZXPUtNHat67ux031w6fFTQhSxM0BV/oShYJyTJ1QaGohRhIIBQTtKZKtao0A2LqlAPiN4qCAKVCRw7idbnitUksnECvSeum00e+q6JJsc1jqFI+FKz42PvplqATSGhJvQ/xb/dO51l40+Fk0mv4EoLNSATkqgVJIiBb6wslRf+jQnQI0QKqt8dcmB23k8LzVIGbIdubEsyTAzB8/jLp1ZzzZ0sCq/YIg0AfgCOhCRrse+ks9PSZ20/FfjiVWXVNRCvNeAoPJDp5QNXhz4A==~1; ext_trk=pjid%3D0363a9ac-73e9-42ff-baf6-01561f62d764&uid%3D142672e9-f2e5-4f96-8073-2ae5ef456b4b181b3eb827d&p_lang%3Den_global&refNum%3DEISAGLOBAL; ak_bmsc=DBFCB4E9A32056928725C8D31448B086~000000000000000000000000000000~YAAQ9n4WAgBvyLOCAQAAEg1J6RCuNeOQzLANjlKbEyTSYQZeEdYVUk10mxH9gUO6w/ZYqukcDV3lIjef/OQlRzMshSWxzGkRjYDdHxHINJjCP9NIaQSi0vDaEg7ndByiWyg/YyZU4Mif0dYBj/qntD0Fd5YH1vncEh9TnIeGFP1P//5de1fQdIjBzY0ivxdURtyEhdPQch6nD8a4NE/ykacQu+xWx6//psxznsLe834JDqrI4TvLT3CmIiWfrdPqhWVUOv8PQB4E0pOr8amS9DmkfLAKfgwDo11bAW53NeF4avUbX+hgFq7HCJgSIZuYypfD1G7RbwRzQ5T2wI9qbxEtDQ2lGW8KU2hEaW3xftltHQcBssM5Fa2o1/6BWefhPpmZvEEAUirp2PTEC3C3nXiPEriJvx8jKjtSsENgsEnAVCxn66FOQjpagKSgRfj7yMLEBTyXKdPI4aNPvy89htRxZd7nlNS9JubsrMXFnEE3TsdLY6QH3v7RRmgFBVZCT38ftVmzOITvSnMBNnohl89i/LVFR2zYN323xnSZd+Ft; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Aug+29+2022+13%3A11%3A00+GMT%2B0200+(hora+de+verano+de+Europa+central)&version=6.30.0&isIABGlobal=false&hosts=&consentId=7965a1d4-45a7-4159-8af2-5beba3f49fb4&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0009%3A1&geolocation=%3B&AwaitingReconsent=false; bm_sv=AD1DDB882E8A5A0A424051F1242977F7~YAAQ9n4WAst7yLOCAQAAb2hM6RBRjyM6Zw993meexCc6w4UTNvqjyh6SMMXIsORr6JBmKJaJsy+RT/1OvhIGgdwcUEU7PB+ACtJz1tX8bHEGoliO7Y4vVrrYUpvAkvVJ2OawKI95N4cz6qP31+mhR/wW9VdFDqDPzLua6K4pGmY1EugYb1zjeLd/iE4RZx/A5UdTWTHy3C7xGQon0ElMpNKYIlt5gP2L4YR+DxY0ZPXbKqqtGNobPPveqzdjki4/FHLiDgn+74iyzw==~1',
        'Host':'career.electroluxgroup.com',
        'Origin':'https://career.electroluxgroup.com',
        'Referer':'https://career.electroluxgroup.com/global/en/search-results?m=3',
        'sec-ch-ua':'"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-csrf-token':'2251ed19cf66446b97426a09a7f5d92c',
    }

    req = requests.post(url = web, headers = headers, data = '{"lang":"en_global","deviceType":"desktop","country":"global","pageName":"search-results","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","jobType","hiringType"],"size":10,"clearAll":true,"jdsource":"facets","isSliderEnable":false,"pageId":"page14","siteType":"external","location":"","keywords":"","global":true,"selected_fields":{"country":["Italy"]}}')
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://career.electroluxgroup.com/global/en/job/{0}".format(y.get("url","")) for y in sl.M]

    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

#    sl.extract(xtr)

#    if not len(sl.M):
#        raise Exception('[WARN] Empty Model')

    for x in sl.WR:

        req = requests.get(url = x)
 
        sl.WR = ["virtual:{0}".format(req.text.encode("UTF-8"))]

        sl.extract(xtr)

        offer = sl.M[0]

        #print sl.M[0]
        #exit(0)

        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("&nbsp;", "", offer.get("description", "")).decode("unicode-escape").encode("UTF-8")
        ad['url'] = x
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

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
