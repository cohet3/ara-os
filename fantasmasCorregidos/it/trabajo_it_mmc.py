# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'mmc.wd1.myworkdayjobs.com'

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

stp = '/job/'
page_ads =11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://mmc.wd1.myworkdayjobs.com/careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be',
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

    clientId="5942d176653646798706abf682f647f9"

    headers = {
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"PLAY_LANG=es; PLAY_SESSION=827c3070144bc765b2b16151e9eb4392b7ef28c6-mmc_pSessionId=mev8v8e9urqipjcu6244uf2dml&instance=wd1prvps0007d; wday_vps_cookie=3324422666.61490.0000; TS014c1515=01560d083936b2bf1231517c3d1966fdd3c4e0fb55ca8a7f55f93fa2851e0f0c4bb2a7903431a30b95a26a11e203c174d5550ec15f; timezoneOffset=-60",
        "Host":"mmc.wd1.myworkdayjobs.com",
        "Referer":"https://mmc.wd1.myworkdayjobs.com/careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.45.010",
    }

    req = requests.get(url="https://mmc.wd1.myworkdayjobs.com/careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be?clientRequestID={0}".format(clientId), data='', headers=headers)
    token = req.json()['sessionSecureToken']

    data = "facets=Location_Country&Location_Country=Location_Country%3A%3A8cd04a563fd94da7b06857a79faaf815&sessionSecureToken={0}&clientRequestID={1}".format(token,clientId)

    headers = {
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
        "Connection":"keep-alive",
        "Content-Length":"190",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"PLAY_LANG=es; PLAY_SESSION=827c3070144bc765b2b16151e9eb4392b7ef28c6-mmc_pSessionId=mev8v8e9urqipjcu6244uf2dml&instance=wd1prvps0007d; wday_vps_cookie=3324422666.61490.0000; TS014c1515=01560d083936b2bf1231517c3d1966fdd3c4e0fb55ca8a7f55f93fa2851e0f0c4bb2a7903431a30b95a26a11e203c174d5550ec15f; timezoneOffset=-60",
        "Host":"mmc.wd1.myworkdayjobs.com",
        "Origin":"https://mmc.wd1.myworkdayjobs.com",
        "Referer":"https://mmc.wd1.myworkdayjobs.com/careers/7/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"{0},111,0,".format(clientId),
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.45.010",
    }

    req = requests.post(url="https://mmc.wd1.myworkdayjobs.com/careers/7/replaceFacet/318c8bb6f553100021d223d9780d30be", data=data, headers=headers)
    datos = req.json()['body']['children'][0]['children'][0]['listItems']
    url=['https://mmc.wd1.myworkdayjobs.com{0}'.format(x['title']['commandLink']) for x in datos]
    #print url

    for u in url:
        headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=ce63ad23-d4c1-4140-8efa-84ec39b81e81; PLAY_SESSION=b49ef68709989fc398db931da83c46b8397a9977-heinz_pSessionId=fmpooec7179cp36j2u6q56em29&instance=wd1prvps0005f; wday_vps_cookie=3458640394.1075.0000; TS014c1515=01560d0839c8e68f38a625087b09a1dc8537853ec9944bfbd18f4f71d0a1ca0e3a14097b3ad1aee5cd768048fc30cf7852103b4386; timezoneOffset=-120',
            'Host':'mmc.wd1.myworkdayjobs.com',
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
