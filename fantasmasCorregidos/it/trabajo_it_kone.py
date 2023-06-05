# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'kone.wd3.myworkdayjobs.com'

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
            'https://kone.wd3.myworkdayjobs.com/Careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be',
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

    clientId="629fc3fc9daa45ab9e57482c5cca99d8"

    headers = {
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"wday_vps_cookie=2586220042.6195.0000; TS014c1515=01f6296304b892dc41cd0b07855d1b21d29ebe92a9805c4040b7d05b20bebd361939d60d20998ab2ebd47c9774f1ea21433e5ade3b; PLAY_LANG=en-US; PLAY_SESSION=593bd64437db67044c77b5c204307715f9a2ae30-kone_pSessionId=pen961l4qn9glrnqtimalp0tha&instance=wd3prvps0005h; timezoneOffset=-60",
        "Host":"kone.wd3.myworkdayjobs.com",
        "Referer":"https://kone.wd3.myworkdayjobs.com/Careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.47.010",
    }

    req = requests.get(url="https://kone.wd3.myworkdayjobs.com/Careers/1/refreshFacet/318c8bb6f553100021d223d9780d30be?clientRequestID={0}".format(clientId),data='',headers=headers)
    token = req.json()['sessionSecureToken']
    #print token

    data = "facets=Country&Country=Country%3A%3A8cd04a563fd94da7b06857a79faaf815&sessionSecureToken={0}&clientRequestID={1}".format(token,clientId)

    headers = {
        "Accept":"application/json,application/xml",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"es-ES,es;q=0.9,en;q=0.8",
        "Connection":"keep-alive",
        "Content-Length":"163",
        "Content-Type":"application/x-www-form-urlencoded",
        #"Cookie":"wday_vps_cookie=2586220042.6195.0000; TS014c1515=01f6296304b892dc41cd0b07855d1b21d29ebe92a9805c4040b7d05b20bebd361939d60d20998ab2ebd47c9774f1ea21433e5ade3b; PLAY_LANG=en-US; PLAY_SESSION=593bd64437db67044c77b5c204307715f9a2ae30-kone_pSessionId=pen961l4qn9glrnqtimalp0tha&instance=wd3prvps0005h; timezoneOffset=-60",
        "Host":"kone.wd3.myworkdayjobs.com",
        "Origin":"https://kone.wd3.myworkdayjobs.com",
        "Referer":"https://kone.wd3.myworkdayjobs.com/Careers/6/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "stats-perf":"{0},62,0,".format(clientId),
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "workday-client-manifest-id":"mvp",
        "X-Workday-Client":"2020.47.010",
    }
    req = requests.post(url="https://kone.wd3.myworkdayjobs.com/Careers/6/replaceFacet/318c8bb6f553100021d223d9780d30be", data=data, headers=headers)
    datos = req.json()['body']['children'][0]['children'][0]['listItems']
    url=['https://kone.wd3.myworkdayjobs.com{0}'.format(x['title']['commandLink']) for x in datos]
    # print url

    for u in url:
        headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wd-browser-id=9a0ce7c8-0d61-4c8e-a058-bb64431a9bef; PLAY_SESSION=66d1e364b00d617853cc30b11d286250b76d0500-kone_pSessionId=22us23o4l0166llj6qn0aa0c43&instance=wd3prvps0003e; wday_vps_cookie=2753992202.64050.0000; TS014c1515=01f629630491441804b2429560aa3538aee47840e6cb90666a1486e2fdefe7df78800fa1b3318baad626443246356fc84207983cb2; timezoneOffset=-120',
            'Host':'kone.wd3.myworkdayjobs.com',
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
        # req = requests.get(url="{0}?clientRequestID={1}".format(u,clientId), data='', headers=headers2)
        req = requests.get(url="{0}".format(u),headers=headers2)
        # print req.text
        # exit(0)
        sl = slavy.slavy()
        sl.metaExtract = True
        datos = req.text
        sl.WR = ["virtual:{0}".format(datos.encode("iso-8859-1"))]
        sl.extract(xtr)

        for offer in sl.M:
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                      published_at='')

            ad['title'] = offer.get("title", "")
            ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", re.sub("&#64;","@", re.sub("&amp;","&", offer.get("description", "").decode("unicode-escape").encode("utf-8"))))
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
