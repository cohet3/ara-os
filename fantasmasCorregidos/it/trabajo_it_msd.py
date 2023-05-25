# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobs.msd.com'

xtr = '''extra
<html lang="en"

title
"title":"
"
city
"PostalAddress","addressLocality":"
"
contract
"employmentType":"
"
description
"description":"
",'''

stp = ''
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://jobs.msd.com/widgets',
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
    # sl.step(stp)
    headers = {
    "accept":"*/*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "content-length":"389",
    "content-type":"application/json",
    # "cookie":"VISITED_LANG=en; VISITED_COUNTRY=gb; Per_UniqueID=174af93a748118-100200-2940-174af93a74a65; _ga=GA1.3.557754132.1600673528; _gid=GA1.3.1129429368.1600673528; PHPPPE_GCC=a; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiI1OWYwYzE3MC1hMTVjLTRhOTMtYmNmZS05ODhmYTg1ZjUzNzgifSwibmJmIjoxNjAwNjg3OTA3LCJpYXQiOjE2MDA2ODc5MDd9.HxNgcRDIvRBWE45t6YqwCp8wTbf9aw30MlC1eQrmeOE; JSESSIONID=59f0c170-a15c-4a93-bcfe-988fa85f5378; ext_trk=pjid%3D59f0c170-a15c-4a93-bcfe-988fa85f5378&uid%3D174af93a748118-100200-2940-174af93a74a65&p_lang%3Den_gb&refNum%3DMSD1GB",
    "origin":"https://jobs.msd.com",
    "referer":"https://jobs.msd.com/gb/en/search-results",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "x-csrf-token":"b9a47bda5bf841f8bd36adf169a60767",
    }
    req = requests.post(url=web, data="""{"lang":"en_gb","deviceType":"desktop","country":"gb","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","subCategory","country","state","city","type","division"],"pageName":"search-results","size":10,"clearAll":false,"jdsource":"facets","isSliderEnable":false,"keywords":"","global":true,"selected_fields":{"country":["Italy"]}}""", headers=headers)
    data = req.json()["refineSearch"]["data"]["jobs"]
    # for d in data:
    #     print d
    #     exit(0)
    sl.WR = []
    for x in data:
        if "italy" in x.get("country", "").lower():
            sl.WR.append("https://jobs.msd.com/gb/en/job/{0}".format(x.get("jobId","")))
        elif x.get("multi_location_array"):
            for location in x.get("multi_location_array", ""):
                city = location['location']
                if city and "italy" in city.lower():
                    sl.WR.append("https://jobs.msd.com/gb/en/job/{0}".format(x.get("jobId","")))
    # exit(0)
    # sl.WR = filter(None, sl.WR)
    # print(data)
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
        ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")).decode("unicode-escape").encode("utf-8")
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

