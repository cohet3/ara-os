# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'candidatimodulogroup.altamiraweb.com'

xtr = '''city
"addressLocality": "
"
title
data-title="Titolo">
</span>
description
class="FORM ScTableTitle">
<input name="'''

xtr_url = '''url
data-title="Titolo"><.*?href="
"'''

stp = '/Annunci/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 10))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{page}',
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
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'16952',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Cookie':'_gid=GA1.2.1970040985.1629366855; _ga=GA1.2.224437164.1629182346; _ga_267NWN6GPQ=GS1.1.1629371169.1.1.1629371830.0; AltamiraLanguageCookie=Culture=it-IT; ASP.NET_SessionId=4oddith0lsx4art5uoy1ljte; Altamira.Web.Security=; _gat_AltamiraAll=1; __utma=219575563.224437164.1629182346.1629463052.1629463052.1; __utmc=219575563; __utmz=219575563.1629463052.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=219575563.1.10.1629463052; Altamira.CookiePrivacy=1,1,1,1',
        'Host':'candidatimodulogroup.altamiraweb.com',
        'Origin':'https://candidatimodulogroup.altamiraweb.com',
        'Referer':'https://candidatimodulogroup.altamiraweb.com/',
        'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile':'?0',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    req = requests.post(url='https://candidatimodulogroup.altamiraweb.com/', headers=headers, data='''__VIEWSTATE=%2Fc7%2FxWYu7NTHRYyTHGu95xXhOygJ5%2BGtxzcCoq5iZRM%2F3G9V1DqhroKcTevc3BWICIVnaTvrXb2d0x%2FCeTyglHPIw46Zd%2BABioidSJOq%2BiM%2FSKKd6iXhLxtLn%2F%2FEVoebaP5Jnv8p5XBUxgaIP73lqiUXuDFzWngOdLVuGvZXvDcXLTDoVMC3Tog7UNuh%2Bzs9fZL4FxFfVJweSAewVpprraSHA8E1evBdSb6x2c2%2B1pZXX2xdh9caWQTpkoQvl8Io8qal0rDRsWCfWgbIAADw4ociM4DOZH55cuoUKKS3lVwiMzdAOLTDEY4suGEH4zBnfe02HCzxl5i1LXNAnA4WlY3rCuFg4ZHHzyl%2BzZSBnEYXfUVjsrKcZzLMMgLacjvr95kiM64M6PyyMEvMSXUMG%2BGAewNPuhS7bLBd%2FByFLJ7VQTe1cPolz0IDIAVo7kbloQeGB7yIhKls3rTivCCt3ZfPYz4OWBdta3f2rrwpJPeVZBnaoPHlZ8RWPJ%2BQvUj56FrT5pnBkALA8HYyI85WkIeuNtqqH66ol8lvE7YldzIe12Fw%2FT2lr9zQAv6NjgJrCI74Vkt5tQjCb7YEAyJuol3gX4%2FH3EnIY9U3G9nk6986HW5LtCpHatJZyF8m%2Bg%2B4MFsKWWeclMPK5QkAt3jXqjDKJfRdkOuiVnbfh0%2Fh1V8ULl10EkJSBp0gMrlmkp2lXMdEod7VyX71yVAXFUeQvqcTwABLTMtbKp384ngQ9OFEOKcwMt7w1FLAVPVppbIcW08NQNs0SYkA8sdDGtz7QnOxEH%2BdQuIcSSQAlO4p8ERbjbReffEgZFCkey6PTq4x%2BChO2eu3jWXsnMWUtwoW%2BVN4NVqJZWp0ap2ZzwYAnYYOKHB%2FZjPW7CIoznlWrojIhZVTyyoX5tKKSCRp63HiOj8EFtqgrZ3iTQyoV0dcNDp3tvZ4MLm0OoBGh0%2BGi9bmjIif%2BKD9Izp%2F4d7thmsNq7t5Yp0sSpG473XokWcWiQFUh%2FOyzTxedFfSOtN7L%2F811bK90ZZLmHNJF6EeLy3Py7Ew1jpllG3e4WRIvcJ0rdWKgJ4jZp%2FzFIIRB9dcuChn6QrFk6NDWwzR8uB3vBFXzRISucWSahgBj0V2JXgPnPEZWNLaRF0%2FDYQp3qUfDG4wGr7cXEYgFGMQeAZ1FlEcK%2FYwXKsNvvuIGZMMhHBD5Hr6EVQ6ZpNySAGXdvEZRiuNPpv1MxTVt6jOtJ9xi52Ef5V2%2FW592yKq7Jz4H%2B1nXvSfB4iMpsNY3zdgogHa3v%2B0JMlH6%2BMWYVwgBIv2tFq3R%2FOX5DmU1%2FHEd7XNT%2Fahv0124sDSvR8ngBaw08Y%2Bw1otZ7MAirNtC9BFuh0I9oqBkFPlcBCuTq9gLwGFjYOK9Dp14raBKcbGWPyvMbqlE8vxSg6N3rwq1NAWxOxRpGwKSZmTBPyDAMh1kBzkMRh%2F4CQgN3kk16XpKSh8sPu1O6RIvGdE%2BkiLDqXD8WtilCTLVHaCS3haJGcUZkLz1MXmvPPQMC8Bw1YEfSFW5HusX%2B2z%2FIzK9CrnisplA4ZTQJCTtbKmwHNX%2BZXPX6qgcWuvmYVybso3flbhSvu9XpKLN6Ljz2aQbfQ2Al4PujVJgSYhVfAJTsgX8%2BZFBz0aRwEsWmQxIwM2zgSsErCZVmu%2FVKIgXYCA9kXXG54ownPyLU%2FdItmr%2Bvs9nrPb76qItLVka4yAuFBFUEq4aayH0xdElRcGM0UHjdKMhobglpctjZ%2BV6n2T9b8BGI68nQqf8TQZcK9bVXFsarHFMdZ28gTNYYOLPxOPLF5ktG0GtWRjEABJnU5H9qEp87brxcQ2jDLxZuYwVBqmT9z5SEuBp7yrL996kAPLHCOR5WfNok%2BFyKGgTD34%2Bc5qRplTr4w3JqL3TEYK3tvxOs2ErOKugfmHLnnohzFPpI4DYs5dCDoKMS3DCSMdAuEmH6RY4i3c7JHO7moYD8q6uOIMBI52FvNqLKZmyjAyFcNEupde7Plr7DSnGOxmwtfAamd%2BVK7CvPVZTfoNhqUKRRM%2FZJvlflrFFchZ3%2Fp%2BWVQt8taiCyyAX09C%2BD5YjgHc9VV2SmO8MPn5blHCbQefcmjGPZzXmjSS8Flz9OLL%2BGvnz6YqAhqaCsS%2FxKlKgsqv%2FaLRQ6lyCY1xsjL6vCRH3b6zvjvsQJVZuGlOcVhJDIiMvd2zQ9uqo0Fx%2Bc9lZZTt6a8kVGmOYPw9A53bndNjbqfIG2ZdqBmgJ1gh0%2B5tHlcoxCr3O4Fer3smscH0d6Pwnq73HGh%2FBPKlRQCs0i%2BLWliNggTBMYqJoKhqzDj1dLlM2gr9s0XXzlI526cs46rJS%2FHGciofNaWuyIklxTTzHkqILSY3QC9CXDuWP%2BanTmpgNQqPXajVDvfodYfpnVYkbTJZivm7ONOe480N3QKvTgYlRigTvnG0Hys8iVNFu7vI1EJrFpW6VF92sHyjRtOOigGn0ejVoJ4JT9HHAaB7kZ8xnGGhcZrRO6F27jo7hFT8LmuFs7Fy%2ByDNEvlmlITIQzKOKoeiqq%2B17yqCbEwxl1crRaKw4YTcT97szcNCiPbhA30EYNrTSaWm6ooaswu%2FwUyLzTCv0vUhFHBSXVKpeA2Byj2YukhnwrDy2GlsX0PVQap3FNR0eYjhdxQPZns6KuefqVgYisPnZzJ8HDQN6Gi%2Bq8E4cB7YYHiBYvFq2zQ4ZK1E%2BFAxdc6wofksZ2fD22pZOs9RriWIRDidt3ukuBHj63pOLgWkvKagWi7j4I0dNiSkNLhXX8bINY3wZ6%2BpAqZsC8V84JBVJdlXVK2eKKeQHP8l7sgZS6SCUTN5AzZ6TUG%2F%2Bmqyvat80Onux6haJCiPM0VUKp5uI82LHgEkfmlZZcclKN8aPz0v1V4ofytuiOUckLjffDU7A56t3a0La7DOWGJvyKlHbpPNYdx3fVYg5tYST7CEd%2F8qG%2B630vlkYF84TizQfDmijFMowQ2KCLyxH2ESuxjJGL0L8umVyBpHLY0yCt57UKhZQGQJbNnV79ZOrCkyD8%2B%2FxDXFVaIcKNW177R7Mq0rHbdp572GlulKQro%2FLI1MR8P9MMAkQt3xmv4VHbU058DJlVGRelO6S464qpZHxpC2RQN9i8T4i2GrH5bW8ZTXxdf5gs5petdGEjDyj4r14gAn0iCFEoY4kztl%2F0RroO6b2GRl45NOnp%2FxfvIAsDCTJY9UZpiP%2F1bHr2cSUfWpOZerrvmEsN4G1b1j0HUEATfMaCADkQyoG%2F%2FWcbC30YD3nP5s%2BG87Ksv8F5dTGT8B8I13MIdvLmAGGxPJqANnOGK5b2yo5pKrxvNUycnk673D86irGZmbTUWYwfF1hHfTFC%2BF7vsl0h0MCB12nvPdoXQEZ6V9kRSNjq76IFUlwy%2FEROEynjfsTA70xzGbvEYuOh1Z4vdmFbE9QmGWp3z7Cs3yasMrWvaALFyF148ZdCUKjGNBHncTldtGJgBZYuu186Lvrzy3NiBHX%2B7h5l0NYaDRhQS%2Fqh3SDpsf9dgi%2FWFkALVOanMN5Hlb8nY0Tibxh9AXtM9SDX4%2FGaBmkSm0OmNfweTJ0JWW0fyNvAsWkksyVNxvFQHf2pXAnouYXJXBa%2FbNlzP0pDVl%2FjxakaFA9OblfH1c6gx9Q%2FAg5kXtZu66Plih6ANWXsTvcXW76IA0lBJ3Isq0Kt39V1xO6HkOr6CQ3IN08tQCdLE6UWq64DRp80dX8IO4Ddi6Vxo5d70%2BZHq%2FPEnZXMVAoT%2FACroyLWijvYwrOkp5VtfXay3RChqJ5Ygr%2BGIBT8532QPuY8S1pegZY8s5yT0qh9SzNSVDtRYjWcZCya2JGdi88AdOa0dnoA7odQKij1n9HoF%2F43Q8P5Sxkf%2FC1m2y6igm6%2FENTBHumEISK6NQnLGdH4ORs0yRfoAG%2F4plnzXESAoNdQ4uKnEDbI9vJJCGYjU00aWLBfMGKguNUczndfyUEutDss9R%2BFrTid3qp%2F9WmJ3MTtL9mm1kq04igjeRfzd3O3lqEwSxtE10UuP4krW%2FI4jR4GPJhUB3q0TF8EnfNfc%2BB1n6ZLjjJpaSZps9DotcB602xwbqgmxZbBRcJ2W5VVOVpVnTHUAuAHN5LTCy8RPz9l2%2BjhnDQjh%2FUahvews7EDnn8q4wwEkDbf5dF4IyyZ3pQRBH0Rz5bBkr32rM%2F42YKn1Af6vMJkA51NTzrSC6KkqzZUyNq73tDDlZejwcXuUVXOXl1kZhydqGHZD6Nnz5qXRtVZ50058q2P4QAXGo%2B%2BmHe%2FsdNzVHuyZCqlmjcQqj9g6mUaEq%2B%2FAn5JNdM0seaOC5HRz2tGZAHUXDshwe8%2BX2jiR%2F%2FIIYOFvsgjFUagd3zxF7zX1Jiv68xfgkB91zxwwgA8QHs6v1f4jAWAV39%2BqFZMtPtPRG51P9Y%2F3riw96s4UFHg00%2FDF7zjEZCNiTbH62TEOezvvj9ZDGGxzF7y6zh%2BdL2w7WW1KFwpm211dUV6mXqbYWu%2FKZOTx5CATqZEr2UP1oDF1TxMPsxb0XBeInhNvGtndFrriXBkp86z2PuzhLDgregMVs6zbe6WKyGxRtXN6M7u8mFJz9yNYtFOEHlDKdXp%2BiagJKhkKkb2ypEwGpxIa12Fhw1qbISvEfd53rkgrKmFEu15Re13T64CgZKO4vJWeijWiCeshdG0FN%2BL2gz6a5MONRhA9IyaYx1RdIgRx7Ik1kRA0%2BjTe%2BbdBG0wVnoyTMpsVbGeGjzJymLJx2ONQZvlP040ZTk0nC3iZfEfIhjmrIZwLDyAAiC5NNRZbLSH3Gxx9H7bOxMQJaMuoDfLPFVHUQG5wt9CEWw9txgO97gmkUIAG1xobtroiUhwXuM3wcybgP7CQ22eLkPcLoLpLvB8J1%2FcEdHwk062t6thKua9hS4De76UYogVvxb%2B9KM8ERczt8Qi9J4TaX85WyNhJ84JidU95T786vUiT%2Fq84oenb9Um3DyBrrU5lzrTVOl3TGl9y8N3xECB%2Fwwuda%2FartEHQj8pWAXvpdO6FeJY0ODVe9ig73tGUcsfaNb3DOvqEP%2BVqA6xoA7Hp3t0328m16Gs9Np4JNU1sNlEg1L2GneOaehZgs%2FU38ACF7F%2BB5GMHmtFJZT1q53MYQOfpvB8tuqWpIO7T3QHj8apf1cgLSQ%2FqsmE0k7hdrMv9w9ZdXgx8LD5fTcauq6iWk3Q4XeNdjY3lT%2BjIwOUBXZrqjKYnWg6%2F0o2en6IXEawxOL2D7BqpXIdmz8jXoDknnnGA2DWAEB%2BF2GK9N2dkosRMkuHlqtBy9iNqG44FMVgpQDSaPORUrD7fBo6v%2FTcn%2F5fvmf5SBFtRA79KKplbD6TfbpTlWDTayXS8Hxmkfhj1r7isz3c0NiLfsl7qknWLLfkewxfYU%2BD5RKCdtl6rdAjPdTpirY%2B%2BfqcklWtYz8HZt1QdBN39y9E9cH0aPBCLMmHIBrO%2BIHs%2B0jtotYXUsgCs1%2BTCmlTupmJN0kyVZXhdRIfPWsfJaERHUHnoyGekv%2BxzOy8p25tkm560o8pZwYO9rlzBVyN0%2BTOhwj0DuNVaoeVQCJ4kDtOcbJDQ68NYaJds%2Bxh7khe6CE10lrJ15jEAbQM7yMyB28bJIdIaVjwSnpKVZu0wP5epgtvQBsUNw6u8GytVmoGPyD1HXzkNEzVliPvkjymzoMC7CDkkFjtk9JljFhxTP2z2dR2BERlNl5q%2BKJEbf0MfR5d09MOXf0EFVc9jazU4PpkdXgQko3tT8RhzZDrZ9xMlIcOIiskx7aqhFXCTNYKqhbfY%2Fr1DOjhv2Yr3F0hBpRyzEphTkkOOa5hMAQ0%2BwAXHZHLYx0INtoxILiQOihrWYojOEW0HZx%2B3gDJv9shHLCk9xIF4S16S%2BpzzNAFUHK2mLff7k4C4y8sU0qDvKciVxm18GhpSgpcW8CFejXYeCuGIH0uutCq76L4wVwhLmIyraNHaf%2BqcQpchLnerymGj8%2Bb%2Br9p2YPxYIZKM8EJkHJSPmd3i9x9jKFZmOePDRK5R8jGsmYgAi2cUCyem%2B6kuUlsunl5VmVKmdhzK4yEW4W9PjcebY5WTcz%2BO4R2hAWFwwNIIzcrxajLQcdDpqzgpfJ%2FztldzpS9LhQ%2BAHQwI8Bz9lg0oKtZ70aPi8dHVyNKwfHNchJpZOnJDoLPd3beIPFsIxAcuFmpBo80chN1ctRaXcA4l%2FpjOhjuLulzaYMW4U8rPNWym5TgUprStDRal1kYK%2BeEg1g7KsQ%2FYJq0kW2jnbwechrBj2V40fvPeVmdk8IbJzNJ4Darrk8FGbMX1Be4qChm2h4AcUiqzhukgoldRXsm%2BrWg5ZDHlj3nBeuNGgQo8lPaPUyjHS9RXdd1VZnDMtWHgHVSb30NVv61yUi51VZ3otax9YONpeWBEDIXcXLKA1bAToGs1XtKIphYfp8hhc3JPNI33nsf2E%2FxOG5ZD8o0x6ZZmoNzp8oZ%2Bh%2Fe%2BjbJe0L5avwiQ52YMJ4GPvSLxGGIiWAhL7hlDINlY8bss4RzbBCEfbHDe8Qmo2N3UpgXBEW6UJzjp4rCIUXN90uHqMoP1AL%2BwFkSuNKNwL%2FuZh6yXJ2tZS22drqsffB9VLzCR2MmNnoJ6H1A3YUDonsrrCmKZindf4KDlNJ%2BXnkxetwoM27egYi9%2FKkLh6oVWM%2FhcP5xh%2FFSeadqghEPJjeTa7YPc1ThSMhTHMpN2%2F1jDkf5SAV0Yf2YZYdxdlYUxhAklGnNAvUFImIvzrxYzlksarlq7jUU3pEBU8LPCh4os0a7SHcbNRGOLgG9y%2BzHsPIoyEHRCrcQPDBij%2BO7bJ6bKRmnbl%2FqD5NO%2BLJhUDkgN0sBOt0L3NgrvxunwI72sw9MyKS9wF9apV2JhQ9k5ln%2B57aQnDlVaPqtDdQ7RoXESQDgBqigHyOMOZoD0mnu8k8F4ihmqFzVAI%2FPBc8NEG70y7f5ZuL%2BxT1kPP4JIX6loAmmVfY3SkdHf9Hcybg0r1OdsyvypTc%2BT99F3nZN%2BoeBAeIIsFERRAgXF2wPlbD0vVUeb6cPiEEvuumvdZstaYeBk%2BtoYz5cOB%2BFi8cbjDq%2FEwnPeOvZQWHUHn25WgNXqW2SVrkWLJIX%2FaGRhjz%2Fu014%2Brjs7t5qEkWJapjKrgJa0gO7rWPujUM6PRh6tGyl9kp27rYR7zgThQGZ%2BACAQO7JqPhcM2KjmQy6lIV5o%2BCc8%2BsbMfuAWRshVFA8SxCtbbYx1sENaRj4no1rFGNSM1FGrqh6pk6Tp6jZqX6iumB1BNRBF8d%2FzK5TZ70CkCDd1FY8wJVP7V7g1cUICG9HK2VIMMyiXbn583zV%2B5FKYdDShwnkol1eyAg4hjFp%2FUxPg2OlggddZY3oKpNUtFv6ErXMKOwO6mYC0z26Cleul79QtriNJMriP2v1eVVgGVGc7sW02uUbVWmBV%2BZD%2BzRSHQrerjy5%2FGqsQ734BApR1iHKgRgnwRRZSGBlya5O06x8qxJB4vhi%2BsajwZDXm8FB8yvNmVAZ5TIK%2BVnoZWTtYpawQ4BuWQvl9HpetIWJ9DzlE3Ka9EHV6KoJvhq%2FBtjOW2%2FraYxsuNbd0vxM05%2FSsI1xonuLQtT%2FuiYZLquJ18qImBecqpNJ%2Fkttnt334CWdvyCG7RshvfIufzwxc8gdfFlVqN2%2BQvxqb41H6doA5IZzK8iq2eQhSMv1sFkbCrwYbJdz8dkNt9E8U4u1lb9jJ1dG25JMmd9S3bNgzUnwBdg2ewnCZsI4Vr%2Fk457diLDGy9G9nIG2so%2BT9uvSG7azJer1vYi99fQMnY1N8rZgfi%2B%2FRJAnKXFMbQkNtbjaon1vBtxGZhgkHoMRp4Gv3yH9CUTg%2B9dn2fufmdc1u7OMJI%2FZ6VtSpLWcquKhDhR6E6cezhqIJ%2BXC0TF%2FGa0JZG8xub3TBZab9AgprhxTojAs0fufxV1SijHht8ErLDpEXK%2B5keWG9Um5NFi83O6GLeeKoctdH8OvLkeukm2I7MlCRfsqCUr4PTTGXhF39eea%2FAGWYvscxabzJ66XQhr31JjBzChRCFzSaB%2FAH45QferB0Dgp3%2BwmbyuE1G1A149A4RoNmP7CwGiXY7fwpYots0%2BumxlHJ1G2kJ8YwdjE9cBsm2dXL5BDZiN21KjeAEVCTXsRuZXYgW%2B0LDuhadvr2EK2LDahqQyeWT0oH70cPjiYKmkSu%2Babf4NFjNQB1%2BhSYGJUUANAk7r41DsZk8RPwpH6ndcsvElRVBSo2VWf0JtvVpmYAe2Hlj%2FXAteZmOAKQVBFoGKKft5it9gGFoc6dqqtciEzk6CLuRtnqhimFieqJ5uI24kw%2Fe4FgjS9im4uWgJc%2BClhgRO44u3Xd3v1jIjO4vBao4WoHEuILx2QQQ3Tcyvy1dI%2Fjoo9RCTj7TNz0Z%2FTiVYQ%2FPEoENH2VDazj7bnmvlvEalgadFxTVf%2FH3BfnFFibbhR6ZHGxH%2Fth0d0PE2mwM6Mu2wHnCUDeagoRgYoxzPZEqcWK1ZYgQgoLYQY26R0im89LW0yh%2FEq1P3elCALxAKCtI0%2BUoN4Mdu63lofgkVFuOMt84Brpkq5J3%2BBBqt3rv8vf9yz6lJ%2BYBzWKiMBS4Eb30m%2FJ1dJRkByIM6eQV7wPDi5%2Bv16sAXj5jlDkMHfO%2FPhfQj%2Ftn4XBit2m2epIY1HqnN2kluSwv2UXV1AfzLpCKgyxZiF%2B1N7OfSzHxuaq12fNtLtbeoDhnStaUPNs282aJf7BKgQejEWE0VKg8ob6HFPPwzAo4Q8x4AGcTPPuI3CrZumJwp7E8pUE1LuooTVameVJMDxFKPNXjFag9BHhK7C8N17NPen5Gx4oXh6%2Boba3NRPRShDUABlAKKHwP6x9kmM%2BRpD%2BgPVbJmsYvJhXPLN7BIUBBRH79AHx0VI5irag5rizSmtjcYNcMiYXXdSWOPCfIJp%2F2W%2B%2Fi7goJ2WpufO43gFSn8j64rN1woReaTjZ%2FEIOCxKM1Io6ssnSQE6AwfmBeTJy2wb%2BcLbBw3YOUeB0Z7Z%2FddWLVc7NXwXtXHqJp4jqwH6ySUnKeGkofXOW91Y5ZjoM3dFB41I91Lz9il2QWjdBzbwEzPUwJrmVN4a%2FjbgJGU0U0s0qewuMEuI4bOpvDOL5XHF5TfiRiF2UbVBueSN0CG%2FKXhgW4Gby9dzzrZ0zaW5feU9klT5x6QExcOfwkBWfD6gHFPodAYvY%2BqpNwsZ7A9%2Bkj0fDKitHc24YTs4DBJgRRVJxrEeWidrhys0JEV2cqHwXNVOyZJ2EjuPYvJWZsvY3gKkhhzG%2B45%2Fw%2FDZJiQJ0EVFLIX5St%2F4Xf1RYxPUUBQlPTUzglax9eso9MGUn%2FtjezmqQeHkSv9zINVNWA1hDrFS9da6Y8VGK0T17I0HLdz6fjwm9dZQV5Rd9TqhlBLuK5jzSZjYd83gFWYywYg0aGeUmW4qFbufyrtR1tEpZ2zOkGf9FxRvg%2BjWlmDDJDyWh6%2Fd0I9aoCyS0I3H1u00py6sDMrW3mNL%2FlA4VUukwpczADmM4gGt9et4hyDsMMOG0DLbhpF5UbFclqU8ySgYYUz4HeCX2w3dIlpu2lKMI2oPnOwwcz6CegpvyJMX9n%2FRbvPxe8JZgJGfS0H5abZQFbc8yOqKjDwHown0g5hPCP7eSDGsMSNnTFlrAKn%2BXYX%2B5sJg46HFBh%2B98SPbZr2YUzOjNHaP2lNyiL8KVorBHqKF2B8ijRzKUfm9rGuMROhksdQGccnhPZZGEb5OKOfRgp%2BvXYYfynyeMVLWuuruGvEy0wBJcjIAEe7RBQtbQBK1rcg4wI3AlExROZPMzjQKi4%2FEwf60LpSECmsz306dbt6wyVfCVSw48Uu%2B5MrSdudAmy7a9yONGWWBMY59Id2R84kneJLxZRVhWS82Wn9r4WOFawl3B0Qyjttrbgc%2BMZ250JSMzoqHq%2FJJwbArg8teisqRKM0Y0LEJcNcoWdYpuxgJv06tRYVCO%2BuMg6vz8Y%2BCaBVGC0aHkKFieFLfnS3jOPorv%2FzL7glpdT2stYxpHgtxKIsGjhWZti7bSRCZsW6PHOeUgl7d2mLo0VCTEZoMb%2FvbpjMIHP%2FjSBgdOipX%2BP8Sf2x1A5liiIo%2FR8c8ucqmqjb73%2Favk5esdQUMdBgUTeMcA%2FuhA1cbdUnD21yAPGwFPEH0frbvLZRomdBEgFYzjGiV5JiMZJlaNvSSElAax6B3kVIEYR3PYMP1sWp6%2FOzk2ITIO3XSOTT4KpdSidg0lr0JNaEnQCaKpWFweUlmVmOhgSlCqyrELTKcd7fOe3ghmd7XtloB9qnaPGBkTrYuFU6OkoN%2F%2FEB1jz9MV3XzlTGqyDMTI0%2FMEn0KGb%2BrM8nGY54S1YnlMHtavNnCq89FGK%2BW3s7te96uDmHqIz9zW3kGOahszxTC5ISsxjPzUOlQ2x5ePZmJgciXVRFFnOYleLvdK6CGmxeonbZXFwnSV7bqLoPkGL%2BSaLIWuzJJIWHL86gOwH2HSXzg8%2BtWS872AYgB71B0TPRXyEvS1BWEBubGrknUavL6Xl%2B1uXCxqiPLaMIHx4Y%2B7veBvKHCIVES0U9rr1xZI9CisRweAv0Hn3KNo67wN0LyJDBzi6TL5xyJkUpob6A1gzD9K4RXpCcFTopODfztVlY7qC6TLgqED1eBbdT7g1OQ8XzVgN6Q04WA%2FTcz%2BxaPvwqfkHbvSHSAzmsNlGDMLbmLodu4n3lwqLluCQHFOO865bNt3SYJo15NcZ2gx184iAjR7tiJU6G8AZf%2FpWptNo%2F7rmqLBSFWlIK39v%2Brvu2kG%2FQz%2BmON%2F7sJBmIfofpHfG2arND%2BwVJFcI1dMqS0WphpcuGrAk9dbTnoRJNLYq74eqYqN7mQjX5DVMy%2FPbwt5GP9N6luck8cZEnYcG98GCc576AHV4fyM%2Fjjsl51LRh%2BmP32N6My%2ByiGRBmPWJcObvoF7QvzlGEsB35CKDqFUKCDlbnNH%2F%2Bz6AioK5Cj5gNr0lSa3ttZk3WRRMHNwGYf5K%2BPRV5kfTZ2TUwfNUooKB1RuqsW4BnwsSi9q5VznmaWvxuHLbWrGjNtwmuaVqC2TIbT%2FdLw3WDxr7isC3bMz8B08NNzVRbJlO0UgSFUWuupMXMiKQD7CIddx3MEMp8PW%2F%2Bbu5VshbFDpiDtmBTQTnsKPRVE88kPvUl2isjHplH8%2BGYMgkDJVqV2TWTyyeib0bFvwk3fF34yhLXi%2BOqmUHjz4iZKZlR54eNVyEGOwqSU7AukUnWTmh%2F3l%2BkH8AlbS4QDtJjxbIk%2FC4A6%2F7h9wc%2Fr3oIORSXjKmv6xq3KdXqmZWPK7rjfhTjK%2F7wvB7AnKb4TsHjjWa68VKxHO3cqkGZlivMGUC3B%2BQHDsAukBpDhVbIb32MhouWoWatxDOFM0Nx0t%2BOLBd62mt%2F3nckg1DTejPip1K9F%2FgtDKxTtk6vSCPOB0Jraa9nN%2FOjr6fquH5iI7Sd75a%2Fi2neUf9LmNLx7cW8hsQA%2BOWA2WXJwDIAnPlljnJM34ASxQ%2BMeDllFqAOfya%2F3yMGwKq%2Bu5AHmj8xz6crMx%2F5oLYNKiWnUyHbqWQ1jqZhfPWkuzRxLI%2F8dSluv2gCx5bNv7cTLdBlh%2FYGZ9JDAWw1b5qZcgkK0JkzJx6bfJ71ZRzYYGoghi%2BHbFXCLH6SYQCVhwzYgSLNrbhhjhcG2fYjR2OqlqyCu8pNpmerKB%2B7NksJsSr1bhFa6MsxSR5WsNTfeIZI5bdscnj6e8mSlRWT4aaQy%2Fd%2B%2F7UHSo4Q4%2FV%2BvVd4uSudCAGaGIywuGVsYK48DUGXcSJviezr2uHUs753SvTZfjbI%2F0iNlUWqvb0vsEs3JQh4DV80I7%2FsxkGJ7cYzjLO2RJJbVm4ozkjGJ42GwuSuRch8liAGe2eJlDYuUAMZli4kwlsLKOGrItuzMtDSl6tHBsxeDhBUi5e%2FtSTdhd0w0YHLvDWZPFLqsMvVG29hhtJFcMFZRkI1RkuQoX5XYnotliZL9cvnSE10vaGtLVZuYOR8JldKZm0yABpEmYirqCrn0I4cWoBfAbHdnDDKg2cM9T26H%2B8EuRIMEyxIm43Y3MWn5wSZLs3c%2FAVR3szkuGnh8pUwVlzo%2FGr%2BFAi4JF9pJnRNsXsFRtD50liGTzdcfPOTc2YROMiVVW78ceaejIaPFhOXFEvt8JUI7b1iLDNW6mxcAA68ZcDYOiYt2mhnRdKLfInZLfsbwy8pWbSIYWi7UNt4CbGnxBAc5Qef47qEOqIp9P3A6wybzj53J58K%2BdoGo%2Bv173UCf2vFJjR91nAnp%2FTBvp4P0u7R8US2Zfkn9UxLS6X9rD3Qc4D22uG4Y%2BcPc3ZQwA8VP4gUcLIqgJkev4XzRQyMb%2FI0xdy506VDJdSgn%2BPpjGpqkDzkL86QT4EaYACgYYYQPYyoycDIaUtHBFKsXM75hErQC9SK2Z%2FAHkJELJJQQBXO4ytOPg6w6JLU2ruIbz5Ks7nRgpDNXgL9B6mp2lpxhjPjm3O6%2Fyv%2Fr4UGBwpShqFCZ%2FUOOeX2wyz6nv6v484ZW%2BxNANyRK24x0cMrojvVXgGLynL4UHdMt7ce3WU%2B3aLXOAJsV0KSUaec0BSnMpTJULWLiUA7s1ffr0U%2FSImmdlWmOYUkUw6fpyPHXupqoSzNaH0Uedjg6Ps8esXcwJqv4WDJQCD1jOfuLjNVGu%2Bo2%2FbGMT9N7l9B0dW2UvClQ1dBP4HHHSkJEjGpsGB3ECyhfVLEANB6tRmrm1U%2BgKc4N7CTgi2YTYRIOVXWJLzUhbOzZwG1J%2BOONWFtvGAzxcsPOR8oA7q9232lvVZyslpdq7eA%2BDpSpmc85crjuZBspZFV5xF7Q3Y7g83tQz2D1jIzKgKKbqRbx52SjdAIjxKda9l8si2PYoW9Jvjbg65PnQOsa8Pr8bkUDAIawzkTyh0AxHVP3Luw6JKeyIfn2jKgWwakurRrLOikF8SNdWbvSz%2BIcblMHb24QQPbWR8KeW21v1COWGDkiPckUV2TOT4hsBogddd1yLt9aY3jRqRSM0Shw7IRyyof26N3se3fnv9nGT1Lr5YxGFsy8%2FSOfD338YHVQ9JZah3j59zFJ6zjAFXTbz7G8E8clcoLe24%2BGRe48ffA4XDZZQZegy6xclBYQbAC%2F%2FAA3NjSnQH4x5ZFNZFSyxdj2GaK3zsmQiZaOF4vyoBvEypONkYSb%2FFaJmwzpHwgSeBu%2BKenKt0QjvCEC%2F3xtPYsTTJFpddS3iV3DAff3G5M83FuIB3RiWFrv8ZsJgZLG8NvNBDTGN61wQsKR6yPjw1tA7lg07EDl1PD5G3nD1rQ%2B%2BC8kltQIMqKu6P4gTeycpT62PbLlHm9Tacp0qKQaErysETYWQatPZqO%2BHfSBGcQCjug8JHMP%2BkTryvfbAnG5UcxKq6e%2FSZPZLQxFOqgyam%2BTS37LBv97tEKbP2VHSdKjBQO4LoaNz4%2FPvgWfJMX7ASZSWQ461ZHipN3GRf7a428F%2FEDaCEt34CXRuVIZMT5cc4X9ErA%2FpPRDQEJqhqUf7B8cfyA7yjmOZGiWwP1rz3v5FyN%2FKiDswEWeSKAx2%2FmAUsMcN%2BfRgsStIuxFoKeCIY98iWaISYdMuAN%2BtM%2FLQETdF07hY%2FnYGzs1MD5S%2BTXnlnPCIzfgHDgt9ivcurIBfleTif2Q%2FZoO%2BRi%2FrEh%2Bu%2B0LSSONQjA4EsWJcxxZwN3gx0VmJIbwlmq1XF79tRldHxidQDeIubmWD2DlIh5H0z4NVZVBKlJLFFNYUdJIJ7CZKc8QWUMjXoAJ9ssTDoV3HhqvWHms5RlxILCJHgYXkpYOpCkIVM8DmcCUXyYHM%2Fn%2B7gtklW3LrO%2FQug%2Bk8sHYzKC1tFlx6xZ9LwDJEciOquFZO3Hbc2p41xyBttlkkYTiyr4aqaagpzTfQ2y8JLR%2F05ADmws0g1jpnYdl2jhBPthr%2FjV%2F5BOhECXtkRX9cXIe1UgTqi%2FR%2BooM35Sarh%2F9A7zq2ztHvDsFDAkP%2FYISRyfqZT7fQ30HWQi6NgJRd5DZaJ84Zp%2BrrmBvn2xRp%2BCLjRQo8z3yplwF%2BYhi7jK94TNV0NCbIub7SY4zBPtgnu2f9bDPv9JgBzJWv4cy50YgNW4XcFJHjNv9iTMqJ%2B4Qr2GLllJcIlehEVu44D73kDjq3kLa66xIV7TXcnB4jFrMgTRjX4RhUshnxdUAtVL9Jn1YdWtEYPBm2WGLEu5%2BxuGVF6BQnmx1vuvlDeDqHwXBdjf%2BPrLX%2BZbYTUU%2B7c4eUAr8HYDKwfS03AylefUmplHHvXQRzRDrpOibPTKd7xV%2BEYVPj%2B%2BZHVNCLjluJgXqrcIgLXyIaRhi7sRSnnknJJ7Lm0fz0x1hoX7cf%2BWCRuQp8dq69QueT%2FL%2FIHh5GioN7CAILEKfy4r%2Fl9OH7mR6aI39ftZfpktXWGNcTs7KWd9D3IPP%2BHrtu6sn9jvazJMQIZV1eTNKrqFgIQWaA73zqRVltz3nPpVwBknK9lw2sOG%2FFo9ruwD8HGeeBbPjQ%2FQGAAbmSKtFNqERCZtl8tycbF7trG0BaaHob%2Fj5l%2F1c5Soiy74eZHMoHjRN8wiGJfCUvL46PXFuPEty%2BesPSaksYhegwv8g%2BLqSbJn4WUaNDph4cgoEQIxHTLrou9qUA%2FH5wt42WS4Adi0Hj%2BJlJ9IXDyVtXPupzfgBdEYE3XNMU7Fcx9gHmhZ%2F9fveu4oZar2yAkoXsX%2BKM%2BcDAHGcugQz4DZ7fyFIDlBTJjpxrJQit7%2Bmy%2BxafBkmZq%2FVwHbrOVnhP%2FPgR%2FWCt3oEigEWRf8%2F02EqkGV6XDxiE7ZSktZKregpGP730P14dD8y5HN4UoI3TOoGCR%2BuHjvLcjuuP3MuVJpBfYyDLAApecBu7jEswbrR0iq2W265%2BWi4Q7%2B6cEL03qoWHlyWHOs9oCwGzr61cOjiQ5Ev24yvxNAvWh46idf8xIQV5MvpWF4ROsOT6JFxqsiPR3Gt9LuXCH528JOioie4HXVBeJWXG2GpmpQNnDLPFYDFyw8fQShi%2BNqVmXEA5S8gr24oH4dQHPaLq8M7T6cEC09woag9pOnw%3D%3D&__VIEWSTATEGENERATOR=E50C1FF0&__EVENTVALIDATION=vZpjP3B%2BHqUDpRtmKWZVIhHHcpufnKE3OhJ1Vpnj9egNMy65U3yB4XHhVcDYbbg9l8N9w8aYlRq6e0QoCUk3zJvH0vDTUfSCgulk8XpqWa%2B0JQm8TGXivTA2iUDsO35tqgaZO3FmDt98AqS7ljEU5W574UfMzgYtnADYAh0ASeIoMCPmLe%2FqQl2uwLhE6iK4zeQQ0VtW5lNpBLXE1g1fPlkWpi1P1FjBgwM3YvqUyg6gXLfCVDH6Y8koZeTjCOSg71idpA%3D%3D&VMFormRicerca5CurrentViewID=FindView&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24FormSC1HiddenNew=None&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24Fld118015088=&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24Fld111989176Nested1=&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24Fld111989176=&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24Fld111989210Nested1=&VMFormRicerca5%24FindView%24FormRicerca%24FormSC1%24Fld111989210=&VMFormRicerca5%24FindView%24FormRicerca%24SCViewFindHiddenNew=None&VM7CurrentViewID=TableView&ReportGrid117465463=&VM7%24TableView%24SCViewReport%24FormSC2%24FormSC2HiddenNew=None&VM7%24TableView%24SCViewReport%24HdnQueryString=&VM7%24TableView%24SCViewReport%24SCViewReportHiddenNew=None&VM7%24TableView%24SCViewReport%24ctl03={0}'''.format(web))

    data=req.text.encode("utf-8")
    sl.WR = ["virtual:{0}".format(data)]
    sl.step(stp)
    sl.WR = ["https://candidatimodulogroup.altamiraweb.com{0}".format(url) for url in sl.WR]

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
        ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", ""))
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
