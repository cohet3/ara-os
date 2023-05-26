# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'pwc.wd3.myworkdayjobs.com'
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


xtr_url = '''url
"externalPath":"
"'''

stp = '/job/'
page_ads =11
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 260, 20))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["e57e6863118d01e4ab2a597a342baeb5","e57e6863118d01b5cf2e447a342b90b5"]}},"limit":20,"offset":{page},"searchText":""}}',
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
	#sl.step(stp)

	headers={
		'Accept':'application/json',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'es',
		'Connection':'keep-alive',
		'Content-Length':'141',
		'Content-Type':'application/json',
		# 'Cookie':'wday_vps_cookie=2150012426.56370.0000; PLAY_SESSION=22cd30b84bece288abaff6e30847bed31787952c-pwc_pSessionId=p53mm9qbepl89mok0kc7jsr61q&instance=wd3prvps0006b; timezoneOffset=-120; wd-browser-id=1047b094-c2e6-470d-aac7-7c0a9bc131d4; TS014c1515=01f6296304e89048d2346cbc4e743ada7b3e910dcd2b56d2726eea125f65aeb1f95ca5d15cde92ae752461090ae8fb89c218476d6a',
		'Host':'pwc.wd3.myworkdayjobs.com',
		'Origin':'https://pwc.wd3.myworkdayjobs.com',
		'Referer':'https://pwc.wd3.myworkdayjobs.com/es/Global_Experienced_Careers/?locations=e57e6863118d01e4ab2a597a342baeb5&locations=e57e6863118d01b5cf2e447a342b90b5',
		'sec-ch-ua':'"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-platform':'"Windows"',
		'Sec-Fetch-Dest':'empty',
		'Sec-Fetch-Mode':'cors',
		'Sec-Fetch-Site':'same-origin',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	}

	req = requests.post(url = 'https://pwc.wd3.myworkdayjobs.com/wday/cxs/pwc/Global_Experienced_Careers/jobs', headers = headers, data = web)
	datos = req.text
	#print datos
	#exit(0)

	sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

	sl.extract(xtr_url)
	sl.WR = ["https://pwc.wd3.myworkdayjobs.com/es/Global_Experienced_Careers{0}".format(x.get("url", "")) for x in sl.M]

	#Para pruebas
	# sl.printWR()
	#sl.printM()
	#sl.printstatus()
	#sl.WR = sl.WR[0:5]
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
		ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", re.sub("&#39;","'", offer.get("description", "")).decode("unicode-escape").encode("utf-8"))
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
