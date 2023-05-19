# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'trevigroup-careers.com'

xtr = '''title
"Title" : "
",
contract
"JobSchedule" : "
",
description
"ExternalDescriptionStr" : "
",
city
"PrimaryLocation" : "
"'''

xtr_url = '''url
"Id" : "
",'''

stp = 'co_id='
page_ads =10 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            # 'https://www.trevigroup-careers.com/en/viewdoc.asp?co_id=2449#.X5FBhNAzY2w',
            'https://hcqr.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_2005,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BTITLES%3BCATEGORIES%3BPOSTING_DATES%3BFLEX_FIELDS,limit=24,locationId=300000000345157',
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
    req = requests.get(url = web)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://hcqr.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?expand=all&onlyData=true&finder=ById;Id=%22{0}%22,siteNumber=CX_2005".format(x.get("url", "")) for x in sl.M]
    urls = sl.WR
    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

    # if not len(sl.WR):
    #     raise Exception('[WARN] Empty web region')

    # sl.extract(xtr)

    # if not len(sl.M):
    #     raise Exception('[WARN] Empty Model')
    for url in urls:
        req = requests.get(url)
        datos = req.text
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr)
        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                    published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("&nbsp;","",re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")))
            ad['url'] = url
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
