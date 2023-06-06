# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'fourseasons.wd3.myworkdayjobs.com'
xtr = '''city
"addressLocality" : "
"
extra
"identifier" : {

company
"name" : "
"
title
"title" : "
"
description
"description" : "
",
contract
"employmentType" : "
"'''

stp = 'AAA'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://fourseasons.wd3.myworkdayjobs.com/search/1/refreshFacet/318c8bb6f553100021d223d9780d30be',
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
    
    clientId="2191989458e84dc78ddf4ae358690098"

    headers = {
    	"Accept":"application/json,application/xml",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
		"Connection":"keep-alive",
		"Content-Type":"application/x-www-form-urlencoded",
		#"Cookie":"wday_vps_cookie=2602997258.3635.0000; TS014c1515=01f6296304ffe083cee42f78bda66fbd0492cdccb94a61b2652e16fabca59db0652b6fc911bdcbd8af7197d5b619b6eac6c9b07b34; PLAY_LANG=en-US; PLAY_SESSION=a2796ec7a8b390a90956f2ba156f0a35c9de51f1-fourseasons_pSessionId=5olkjac834t90sr3qnkf9n2fn9&instance=wd3prvps0001g; timezoneOffset=-60",
		"Host":"fourseasons.wd3.myworkdayjobs.com",
		"Referer":"https://fourseasons.wd3.myworkdayjobs.com/search/1/refreshFacet/318c8bb6f553100021d223d9780d30be",
		"Sec-Fetch-Dest":"empty",
		"Sec-Fetch-Mode":"cors",
		"Sec-Fetch-Site":"same-origin",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"workday-client-manifest-id":"mvp",
		"X-Workday-Client":"2020.47.010",
    }

    req = requests.get(url="https://fourseasons.wd3.myworkdayjobs.com/search/1/refreshFacet/318c8bb6f553100021d223d9780d30be?clientRequestID={0}".format(clientId), data='', headers=headers)
    token = req.json()['sessionSecureToken']
    #print token

    data = "facets=Location_Country&Location_Country=Location_Country%3A%3A8cd04a563fd94da7b06857a79faaf815&sessionSecureToken={0}&clientRequestID={1}".format(token,clientId)

    headers = {
    	"Accept":"application/json,application/xml",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
		"Connection":"keep-alive",
		"Content-Length":"190",
		"Content-Type":"application/x-www-form-urlencoded",
		#"Cookie":"wday_vps_cookie=2602997258.3635.0000; PLAY_LANG=en-US; PLAY_SESSION=a2796ec7a8b390a90956f2ba156f0a35c9de51f1-fourseasons_pSessionId=5olkjac834t90sr3qnkf9n2fn9&instance=wd3prvps0001g; timezoneOffset=-60; TS014c1515=01f629630468c70984a765288a8b7a27deae006a438b4a118fe22ef24fffd396fc887c6c62b83d39e9382417a273058e8910bab6db",
		"Host":"fourseasons.wd3.myworkdayjobs.com",
		"Origin":"https://fourseasons.wd3.myworkdayjobs.com",
		"Referer":"https://fourseasons.wd3.myworkdayjobs.com/search/6/refreshFacet/318c8bb6f553100021d223d9780d30be",
		"Sec-Fetch-Dest":"empty",
		"Sec-Fetch-Mode":"cors",
		"Sec-Fetch-Site":"same-origin",
		"stats-perf":"{0},67,0,".format(clientId),
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"workday-client-manifest-id":"mvp",
		"X-Workday-Client":"2020.47.010",
    }
    req = requests.post(url="https://fourseasons.wd3.myworkdayjobs.com/search/6/replaceFacet/318c8bb6f553100021d223d9780d30be", data=data, headers=headers)
    datos = req.json()['body']['children'][0]['children'][0]['listItems']
    url=['https://fourseasons.wd3.myworkdayjobs.com{0}'.format(x['title']['commandLink']) for x in datos]
    #print url

    for u in url:
        headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=ce63ad23-d4c1-4140-8efa-84ec39b81e81; PLAY_SESSION=b49ef68709989fc398db931da83c46b8397a9977-heinz_pSessionId=fmpooec7179cp36j2u6q56em29&instance=wd1prvps0005f; wday_vps_cookie=3458640394.1075.0000; TS014c1515=01560d0839c8e68f38a625087b09a1dc8537853ec9944bfbd18f4f71d0a1ca0e3a14097b3ad1aee5cd768048fc30cf7852103b4386; timezoneOffset=-120',
            'Host':'fourseasons.wd3.myworkdayjobs.com',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }

        req = requests.get(url="{0}".format(u), data='', headers=headers2)
        datos = req.text
        # print datos
        # exit(0)
        sl = slavy.slavy()
        sl.metaExtract = True
        sl.WR=['virtual:{0}'.format(datos.encode("iso-8859-1"))]
        #sl.WR = sl.WR[0:5]
        #exit(0)

        sl.extract(xtr)

        if not len(sl.M):
            raise Exception('[WARN] Empty Model')

        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                      published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "").decode("unicode-escape").encode("utf-8"))
            ad['url'] = u
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
