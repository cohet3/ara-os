# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from urlparse import parse_qs
from urllib import urlencode
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'lavorareinatm.it'

xtr = '''city
"addressLocality": "
"
title
data-title="Titolo">
</span>
description
data-title="Testo">
</table>'''

xtr_url = '''url
href="/jobs/
"'''

stp = '/Annunci/'
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 8))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{page}',
        )
      }
    ),
)

def crawl(web):    
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Length':'17430',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Cookie':'_pk_id.2.751b=18238f216147078f.1668601239.; AltamiraLanguageCookie=Culture=it-IT; ASP.NET_SessionId=knlnnmwwlv23tccmiouztofh; Altamira.Web.Security=; Altamira.Web.Security.JWT.Token=; Altamira.Web.Security.JWT.RefreshToken=; _pk_ses.2.751b=1',
        'Host':'www.lavorareinatm.it',
        'Origin':'https://www.lavorareinatm.it',
        'Referer':'https://www.lavorareinatm.it/elenco-annunci',
        'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'document',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-User':'?1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    data = '''__VIEWSTATE=u1QSi1OonSgFEJjCbW%2BJ3gcmojTq%2B4EJ06A573ym1OzEstgQEhOMVO2nFRjvwb%2FKEtO2aD2dPyEGV3yG8rOs6WDsqYtjt4lSNyN%2FgXrsRWcs2lnJXuUoOrSW%2BQWKvFVAvRP1uWonfq%2B167X27yH3oaOr6wmr3sWKUKZLmPxmNDQV6EHJzo70BYc7reCGYLHu6YerIllAfXcVCm3mW5JtL9qrUnfOUXiSdpe3JmozRm8%2BgqzFef4gxcjjV4yLsf7VkLJZRcOn3sXH4tEt51jL0bYjFA%2BmPT9qLa3vk7qwVfuSm15Dc8rE%2BYs6IlQx1PLhUkEsVg531ybTGdt1b6Tj%2B9b75E%2BdpJHGR50Y6%2FWUaK0ozL0eniL4sCfM2yiEWsMJ36bkKw6Jq6Hy4ogScxyT1LIDa6Jd8PevUH2JAvhgl6rxr2YFJeHuYiKyYhXveClC5esDSUHpjpMBCnhgwKp6h2Yk%2BIIXWnXomJj4d0cJjY%2FFSmlotSjxx2OHt%2BQNuILFb%2BlKeC4xrZDiM0cSbgsHSNGTmPIEMuT7j3cg%2FGuH%2BvDR4fsQGm8C9QsZeb2mjn33PEpMe64wcAn3wPcf6Ck7%2BAD9Lpb7Qgky1JS5SC2Ut8lVQZN%2Ba5HbIFIeV%2F8XSIuMgl3%2Bkn082IJmhxiq2S2WGLuaP7BgDmHPNQOcesewyqFdEnubHKKc9oSVBNf1Pc9fqlnaK2DQ1jlPqyhgAFBSVSjkpxmkeRlawPvKEBiwCBX4kiZDSWKgmGPMOj4gsjywd6V2wi0otbRTQ9Zvmw%2Ft9YLmWkyH7WQHgZSii7hAhFeR7iC%2FRBafhyPeMC4wS6XMfrN83PA73tPDh%2FpH1NUhMxP9P0yADVPLWQzoj4Z5BTd3Pg1cRJQCJo%2FTv%2B1RuKA5S4Wnss7bGHHrn2sWnPL9BJhozQmsWA9eOYhDUR%2Fk3hlNIecaZjEw%2BL44PsMABV0GX%2FHR2KhvInzedI4g3wZUaBIAV7ipHGS%2FkB4U89X5N6c00tjepwTpkNYbTmgVUZcQ0wmEEmiNE7Y6U69uDDko85X3er8cSvqY86pbl6eFFBsqHGQsoQKezTOSjZ5jrdNqJJo%2FgoqaMUuDh8x6S77DPX1Y%2B441FHasuB6u%2BLb6EmUC1%2FpB2aGQI9krldfVjgbe6IvdHc6Y5C71j70LYLT%2FVy5z4KusJ0Wyt%2FdYSRLKxdBY%2FwSl7evVauBOcIWid2%2BQpvYQ4xxggnNAK6TPtYuTURvBrVm9ltzy%2Fhyq6%2FaFL5JP36straYTy4tcedD5gJsuMRd%2F3pevZWyXVFHtmidLh8CMyYYbEYMkShVUi%2FVRjJmQklg3RkwI2bKYW9l2%2BnqwjjI4pWsNbBpJwabrPII8LP7gmMJEj6w7dLuuImyir6JYC%2Fs14X6nmGWkehB%2B%2Fnmqaj9B2DsN4Xt4mTTLOKGoILJDpuAK1zhIZP96PhxBXc59wyGU5i5bm9a8vbZ0hhKxbmIZ%2BawXryqpBo7ZboC1WLRWNVGxYbvbnjKNwQqB4p8oRdCJ1UrSzFFL6vcQBv9JS%2BiuxqDp6uaE8rGinseB4Ika8%2FEbZqCSs%2Fou0bg4fA%2FG6CxxkZZQRaLWxKWG8YihXhV73p7LbCp0JZJZizL7ZvF6gc9MpAvxznuhRrUaiENS%2FEzSCfWEv%2BIsolWMQBfoDnEpC9YdvTiJx4FJX4KhsxdvUzJoZpokvcNJQ8DeS73XVIVqvc23DKJ6KU%2BVRDo992ycA8ftTVDpEvV5XkAulphgkn2BrNEoIGOQ%2FKSfLekEDjVLhVJZUyeXp0qx78D2UIDnW6Ms%2Ba5O69C%2FZiv0Vu%2FRl4gL9CFvWwm%2BJfQ%2Bp2YtQIThqCmktkMkVUzkcyatOdJOg%2Fafav%2BQDs9C%2BCjPM8OMhDrIqgzclgou2%2FaBy6E4%2B2gU6OpznsfrynzAmCrmmnVA4JkgbbOGgs62AsdGEDATr2HH4oYP8fkiwpKioFuwcfAZ%2FD%2FJgCJ2D4pc1cssj9LquVLgW1julsGlydc1knZrcsMTw%2FcsIKhG8PeDWzu7EK1clPi5EFUHYPjzwnXCZL4FmC206m%2BsaCQAmKxX%2FJ19XLInzBCo5xIiB81S4Q4jwiNA1VrOBUhvbNaMWLCn%2Bo7WcwiEAwEElQSTzMkrj8eCHV6ZRPeVIlI6wnS6D%2F9Ir6IzcgzoygcnVTg7R7Oa87ERCr2A3CXb1ZFdtw9fted%2FmmBUaq6BbmhounoZAuqlyCATAeGrTiMfBvkq7873q%2BkA7eH31LJ4gIM7u2er7Bocm6XQRnXcpGQvCyF1m0LCjxaanrU79L976NRNtCq4UYpO%2FYLrktzlqCitpkR6ERv9GhF9qjjo4sP6jawFT2u431OmgNKW%2F79ZvHhQ3cfucjp5%2FWCWs981e2aGZjhhHY%2Btw9H35QFJGothykDV7%2B6VraUYRv0sheQ1BGJJsKeFZnwG07rU7ZfQ9I3irMq4kV%2B6z1Gs%2BaK1tGKLyD%2FmLz48GY0elhypeGdV1nnhPs599Of5vqFnzC84HkjoYbHzJ3OVfmo6k93tEnDgOIqxUCtfa7IGQ0BxOS4tzVd9I0Q0ZnJrDxxV%2FKLFkkLWO2sPn0KbOWEYhtfbb48g%2F6k8F%2BM0ata3QBeTcepRLBoZwz4Y61N2%2B8RmEcq75YJNh8A4y9%2FJP7ejckfHNfWICB71HVpGp65lyOO1E8f2%2B9w%2BcMLnxHZeVs%2BTzhUovHflxgtp1TBvFf35Q7nghSftNSYjUp29UlziizJxN5oBYVp0czg%2FRMCS6JXdwOxjDERRje10r%2FpZvci7nptrSvdHG8c%2BvWi4gtITzfW5YEpnsmIJXVIb9dC%2FcAD7Sd12SIHPUmFDnszJghmgU%2F09EYgy9G0b2%2BsSqQ7ELNR06pe6brUsVSObDtd2MnCkU8SctfuX4SpUafBFFLqhyW7%2Bxte7X93dqziEbi5V1B6MOFGCAbOMzlceCln%2BiGqYQagxR2EoNp6ebXgvsfM0HxLjvS2hO%2Bt%2BTFuPhgWeNNogG2p4Et7Q9iRR65VfpcUKPsxWGlyNEEcOyb%2B45IEyDX8n2DLFEua4h81bNBgKXXSf1jPWO51ZLdam0RPdrLND0Tflfu3V2QlYlygDvlDqP79MvhYhBTu6eMhHTSigo70Ri68O8ohAInhoEekzWB8VMpQZadcEbHmABdDnQWeEHiVmd5bRBF9F%2FjMpBudUyLClX2NVr%2F0zFzCUQet%2BH10uqhE0RIcyBsOyvpJZW7%2Br%2BeruXomJ%2Fw%2FtWujs0f5JqL9SIzJ2BHBi6xlYJYjifv3aGA8Xr7vPON%2F8HnVz9pKQnMg0ou%2BEKmqlHo5miPPoVKwK5O0b32b%2BxIMMVsWPMBoNwUjOxZ9kQ2TQR1qlNLAAst7hwGoH5%2BM5pgpBOMp4C8OaTBTZcGTOK4g8eMNzW9bycJsEfxQBEjKjh%2FQxOZLiNyJaSP%2Bf3yrssTRxqmt70hVbqVyBZrkLiSIpRe6JiYqX%2BkJHfjmwT%2FxLglXxY2t9CTbVbAFyf6YkqgtJdPW4vU8mw2QDmM05IprQFrX%2FWRbqpvwJ%2BMRuwNOnQIgnU%2B24f3UtXHOp60THxPnPktqQUbryVqPzLqxUdPrunp%2B11NOIRtp4aJWyCm4YPapEqsSiciV3BNxjirTOfZjoVN12yDBb8E7vKoIppEVKrrQDsF4jT5gBrkDTR1eGVJLr7P9YLjMQKvxti8EXBgw1Q3PcZXl4cdc4stOwQgio6z28aZ2fTBYkxyME2WODBjUv8yMWvdcSLZ9Y28iUfyIaC8xarN38rhFICu2tYxqAx6zH65W9khBKb%2BF3kDiXbwbyVW%2BsC8lhS9WnLEbu4BB431zMO8tf0uRZRaNCSNt2FB5Jvf99d%2BQZ%2BYiAhmwqJGeJPd5bn%2BpxLY%2BeG3Egtkwu9H6PPo84s%2BvnAuzu%2FMJuEWX%2F23lhNCwkv0zI5Z%2B6LEo6C4Bcd6GHhAvrpjpTzCS2WT64a%2FqfHyqgLCPvM1ad6MulK6ldDcgjz0WoKozq0RjtfqLXsyDWpBhC1c2UMBmkvxFOS%2Btfio8xrjtRqbxl4ccmPngcaEgrP0AkjkboaVc%2F87n0LW1CwDCuVCOtOgLECfJ9TPBqjKB%2BXDjyvo%2BA7OC%2B9F7Lc0mxTIcvodfT5fgrhYe6OBa7xcflE196QrglXZAbrHQvaJf%2BfC4au1rRWh9w7EW%2FtVPEpiQYDD6tdiOVkwcLE%2BQDHJiTpvaw63YLPFMeCGRRUsXzvqO0YsRZMJdi%2BTw3Enwd4Fh8gCB4JNwa9eVp1QFSuJl%2B9QTD2ITlWLAItBdjHhYfFhE7Pq4%2Bec83nDBwc8D%2BYiCga3zMTDdVKqxPL1o7C%2BkPCiFuQAZRxa7Nhc4bM1lFGSqK920YVJqdG%2F3CljHKIJN2GZAUHncZ8zWNF7eEWkwFY57znqxMAA%2FkvRanTC%2FZnQGg5o4y1HyNb8m6xRRXyh8kuxjFJqTw1OsJohpskSioRfJfIUmyP3K8OoYibBMCJUQG%2BUKM0E4iZ2ApAbUAlLbcRqe5WVgjNxGil01o2IiDcMrrJbyaKWxqVw3g%2BdQzntZOK16QITECanU%2FFjlWaAEXjM3K7ZwHpvDx8IQyCXr9cIGqDI%2FIfxchpy4eS7pqPXD5LH%2ByYXlhiprUIizW4uEz5WasroUj2VaF%2BPlRIxyvANmMSzkUPhk%2FX9DdfopyVO6sbDQtJyUoX7I7WrVvDZyflRuoz%2FMx60Ed79YeZJuvuebjjO1KXHCXzlCb%2FV0Ti4GJffby3Ym3MlKssTzCSJTqEOze6tqTJgigcgIbFzviIpAjkH48T%2FU%2BmweJniG2EtoDkwxO75xs57fhsfNuJG47sqc8%2Bh0ha5%2Bat9TgsWCYS7ekEs25kkF6qtk28c6MkxmwNZkiq81LIcNaxwu6H9XHG7ZrtU1yETxP3YgzkWirctV81CEGRQuOdxi99161QRnAT3brdnfI0%2FN%2BcnQzpiYlin%2FLl17GGZnlzfPwFF2PysDtQlV7DQ8dXK9AVpkMhG38aNJEqsUwqVQ6aIq2%2BC9sb%2FiB8xO4YTB8zBbWv03glheEJPYh3pvFoAbVTXxpR%2BtUN%2B2u0YDUD5xaIg6S8S7mwTWwWz8NxnwO2AXdkGjeBrMeHhdPNdJYvMdzXBRizP9qyafmSxYSJrvbrx9zCKyOj5LgC4tDSHSK3nJsHRgob1%2F4kp63esKqJbJhVJlkTB39qcAXREqKvwQnxpb1EHimx39nrxLbx9e64cOQTmJ7f3B%2F8c4KUOQ59aLruVit6QCq8iC48vtJi3whpGktbPsnOLnHh73hpCwqb9fItaJk54y77nzbxNCCa3Gk08Lq1ZbhOpL8P4aPiblX37491j4YAv7qkiPRpKYkchHlL%2BRYgaegmKIcsp2iteEXSOlvl8e847KUmHQBZGYnBeg2gDxcCVti6X%2FBYqO%2Fr36TOyYNiQjXb2EcPppLvonh%2F4DPY%2F2RBIKoTCMuUyZRFVczDgtL6A548qatjiNBO26mvUngZOSgomAKYwyf6IUGsgQeq3BbNowiDO7mrneIUF0KZUPeFPncF2UgoEAGwG4fw3hcppMksHXierDZoLdskH8E78BNawGSU%2BWTXHMqUEOWo7DAY1sQy%2FLqziat%2BHrsjnp%2BoGUXyMQI9%2Fes4QKPy8MZXs1K%2BxwZQOzbNEDig5uK4AJOo6sQXYVotelRqVC2E%2B9hhoDt9byWr0AZk0%2BsEd6NmC0%2FE%2BXNvX6DzrSAG4NOi%2BRCwEdANtJs0xd6%2BDg8t07hn1loxpZ2dMN3ek632YP%2BAQNineqV006bALeonfaBWaRlLdmc1nW91y%2B1bCTR%2B4XHxWd%2FG4k%2BD1X9r5Oqx3xiMgqQZuMZFmuZs6oZrXY%2BnY5xYXnXZx5HNk8cjNCtulZYC1wdOdu6BVU6Si9wpDZ5n%2F7cEx3WjoaO0jubGj5MF%2F9XD6X9LaziE06JGtZewMNCSWNS2mmeA8N85o6nW82w2aN4KOcHqJukUygIEm9VHubiGoFQEk8hqK%2Bhc5Uw61vrZFBddqCeWQGjWyMfFSFI0wCPn2ZpXJp8zM8jgUbViezfp9qGGt3yW1cR4FbojzlXLft3nLfpqUw%2B0Tyay6Nsim58E8o2Po1XdiARGqJGfAOfz6bj7Hv7SbFwjO%2BvclDbF%2FYnFCzq9fA6ICX0ZUQ%2Bso0FFksjTFDSIOMpcnPHcvKc0oyFkIea6K2YfSe7PnBOxYvCKTPyE50sv6AC4iCE2z2kTTJmt5TO0hO6EvHGdGAVXvYk8hZpTTVmc%2FIXdfbzSTlWiEP5owFYqHDDeh4gfS3s4m7xLgtohMHuLItIoGQFSUeplIrkdxKnEjJf7fqR%2BOTcUdsASnOkg3m2DDcH62OPrxbRVR%2B1efv2oqp7eMKkBn7nQBRwGWQzihZij%2BdAqx1rFqzz3bjC8lRp6Oi4K5jd91gbTGBL5qcTR1%2FqK8cTdkb5EBbRzOKv5iIhOLXW%2BLBuWwCthxX9rNQSrVjYbWdRRp6dIG5vaRRijJEpY56%2BrQosRFq4rB4HMMPONlj9%2FyXzpTJShVdy3xxAJq1xcO7VYp60tBjrIOg1yq%2FBw94LnccqzuZ1MFLhXv3VgtW3vM8ZQDcgRgqYGaNMhXLOfQzgivwfHwXj6JltLDVjHUgiFamr4dWI1pap%2BSMCMtt9YNhCQ0Veg31qAH2UAH587PZCobs%2FgwSzXsFd0LjPTyhLqmQId1xPp3eM8jPc7KQSSXZRPSNtmBvTeapJFHgF7lYDMCJjcDWlV6UqT5LiJQPA8fj9h7FA81KWL9sV9fy5bMepGRkntg6H2uydHJtipgL7IAfEQ5FyLTkmBcK%2FOPyVXZL8u8hRIZIAVcLTC25voDgsooHeQ%2FxC1GdUGOpve3s87NxFH4uZ4dfgW%2FYAJKPscRwKOXBBtJJoxVdehw%2FcfWOEKn5T79P4qHXI5VbDWScowUWRTRX%2FeKN7okjnuw0qyu114MPLN0h%2FcbHsL6Kj2T0HbZ2FILHdPmQzdldNncbGXKJjS%2FPezvF5Y6tlx6SU9UkaBZO0Cnl7u90Puakti4o9sW7%2Bv9eh69BwSlPfkNJnXSxMwHMqBOgaL9wVHzvSzsvn7GI%2Bbm2XIyoOFJu4aijhVgvoe0OhW0p2XhXK2XjgQh0f1PRnINQ7ks%2ByMi1ASfUsjjlnHIv5tQAAmOmCQar%2BoPCtDHkG4%2BlMAExlD5uslvbdl%2B6JEfNTdK0pnFw7iQdfM8oUn1JydG%2FsT2Qr0IBbJfDSp0CWWJt00he7KaWt4QPqm0YE8kHbUa%2FfgsluJSXz3zGWtj5GYypipDNTzRqgOYwjsX70BP3EB25ZJTxStbM12sfNPHuNbg2UkJyVpfCqqBe%2FQcW33PgFdCkygau%2F44MYKJ5Dc56iN0R5W6riJIxN38vtQv9WJAyLWXEHP9p8PyWbBtpj1e1ZyF%2FpRlyIe7a84Kad2czNi6THLoQ1%2Fqricl9GPzMaAfm6g5SCbnvvygnI8xfhqOS54D%2FbjWD2kRjmxAdWyGJhpPElV%2BlNsMO%2B%2BakuQsd2cmYqnS7PVWcBEVZVLiAqPBJVlY6mKHAnu8fBWXvw49bn8lwt4Dhsw4LpsRZz%2FLdfY5KotcbRuyyzEoHOSV41P6kM8jBIr6xdubUfk5%2Fe5j%2Bvwj0TVlYK3oP6t3%2BV9jdmrDz2AamJN7lf2wk2hBW301v3Myw%2BxKMf7VsvAe6aNJFaXUhSKUi%2BVhsXvAFQVAJ1A19MOYJxjW7eaO%2Bogx8wkIb%2Bs7%2BegtZNg%2BdNjRiaRyJD1hz%2BTwPQ1DThYtjQU0EHt7sXx6%2FszNwFXoUT1yclafW1pv7sKVaTcx%2FFPGhG%2BI3Zz3bKvx0o%2BNtKogcu0IeU99krDDP9NypPePeTHHIj82OI%2FwpLB4%2BdX0qmfQFRxsqDrDiu1WQ8KzSXUzznpP%2Bze7Y5rImgxknBSuLpB8CtzlL%2BTGkTTLw5ZZfru%2F%2FoG%2BBq0dQ0S6bg83RmQFy1LyKS4bBQusPOm5nwIN79d6HKVj8%2BVIv5iz%2FIuUgkpbJ%2B1Rhlo5n%2Bdzr7H32ElFqoxvK0zicnETGmrKs37BnOnFizotGWAyjS4zF3ovkviRX4DiSBTY3mtIXod%2BDH0lTWsDIcVcWl%2BBMsN4orB41z2VbMEbpGJegM65lL5xw2fyauVhvsKNOfgv5ScrcOPfCruj%2F0sETAv1WBmTiiMceD%2FOBLh5vql9gPIyFbIUO%2FF3v6E0LjeE7sr1loggXXg7IQgdav3FJIE0CmW2wjwlZq0%2FiJq0EBAZOpvfkyea3Qlo%2FVh5PqfOuvvxT%2FBcmY%2FPpcZGaabG4tun9WsTrbZXWIHtLnT45m7PY%2B9VyHp%2FN4hR%2BfJC8Kth6jZV7%2FuQ7IKGRTaWCZe91Wg%2BhIKlWsPhwEfiHJN41RyiiifzSoUdqG3%2Bu6tZDPupwzrenyWEFv8gsj4ZDDHTzOtofODq8eTYYk%2B32C7%2BXiFKKFewCq2H7gQERM62EQ1iOzYoJWDlraJhkpy7w3Y8h2rmrvEeklp2w45g50QW89gwK8JtQkcKqaRwIjdgu5FRnq3NGaZ%2BdeamoIkY%2FuzDCPKeJaD8mZBzzhgGrAqthPMDYhlo60DjWJ5mrsPu0mzVkH3ttosHplCVwF%2By0WdPQ3txA0LA1s5h7WLhDZb%2BL93ucYfRd9nOjA%2FSnEZBpki32Vbb2bQ7C%2FJfJyWxUN5v%2FEabmbgIw3pF6OJl3QrJJhQ1Zaz0pWdMiM70Q%2FH6pnYY%2Fu7LFeKacXXoGSWDZ7OmMfMUteQyTDrUWuR0XIa15ANBwT2Mt0bvW55C6xut0ng5nxQWE5kDJGV5f5owL0MFXB5W%2FaGr6kUSwRJFyE7ONGwePa%2FNWgVLVAhBK58MufqMeO3TRZMPhN1gV2hwXycm4eS4ah%2FbAD%2FFas0rLw0jFgUocHcPhV1I4QhuXuaUwUuZT%2B0CEI8eULypYyI8kBsiALzIHbfdSXE7o%2BgiV1HjrdZHfubBCkrCQ3C63vFXcjdLDa%2F1u6jdezdI88Re8pw5sugqgxbu9DF8ECjpg9okmK0qAIrl6zof11u6UlxDj%2BUtUMMZeakDDDM6T4QIKs1%2BPKwf0OCS02hAFK8FFi%2Bgqkyq8kGeYufs3pHKE1IjPWtGZjlh5aM%2FQVDH4MzuQqS8tOktVnKaW4YvJkCaaCgifNaCS5sKtU9hJJV6CeSiYyhQoo%2B0eYp44jiogiCwp0gNsxtX8aASM%2FZbztXFavcoNTt0vWUiqNmhHWFtxPGY8LYrwLHwTuGF0pgwePFyymOKt93UVTjBw9HgZ3sl9H1FprkyRytq2eg20cS2JVt%2BrQvsGZbUxlWUBm6awkLOhi9H8p99CJlTJI0%2FUiOLkf7lR7Fo47jXtk9fF4R9uBPHO8Azsb7T4qHPHnom7F7VzzHBm0ByZmYjI9tWbVwTozdd4oPDK5PBrfV0csS2WolvKSzRv%2B9oewppkdPHzJLbt%2BpNUKsoHK9n4hilmLEKyKjWFaHh88od8BIUQSnYCuLx4uLAojH81pocpSOstLtARd0I%2FJg1LHoSatlFPncjX0UoCCqXfb%2FNcZCUMZ3k1Eh5SVAFJjbIGsQ%2BsO7KzeqSoqJeXCxDsEmLGC6P6ERMzGVVaGvdhG8pl22pi5BO5fGIPIgOkT3piPkISDm2n39GNKzHCp7hVIDJIxjnjwlue2pP96U%2BfmuIGJo5%2B2r9zVEMyIWv5Xi1TK%2BUArr%2Bp39nLuaX0YmND%2B7x0edrsISYlu3cTLdHHgPI2DhBXCTZ4pb8O0sh16a43gK1ROxjzCLZH0XUpyTAR4LN%2BT9fiCdvJ3X3NkidP8LoMoFXRCEMuGFQ9VlntHH%2Box4m8cY8yt%2Ba6Uno2m%2F3M4NYevE%2By1rNy6ioCZtzi8xwK9nHG7z39tdDnatz164iNyOvEOVTNiqWmnXiOruAR%2BKi6B8FwIluKMtP70aYxpOmm8%2BzDx3hnXBsAUm%2BP6tHES%2B1PLfZyycmyu7%2BIzZ%2F3VAiLXyxs5z%2Bp6JcQK5a3o3XjzcygcHp11CIC01rIlrj6dtJVnEMwlLxtfJ%2FaBbDEdOcwuVARQ3uzCj8lRmEwgH9F3PAap5gkt%2Fen93nZILLM1qgspaIKUlUjqFFtlyC998viTljhCKr%2FA04qS1txfe3CEGMXYtwmEnz3J5ZpkCKRlXcKu38gg%2Be78LLlmzluagYn1Oy7rf5W40TdARX39CC6csYtVbXB4RVobmAy%2BTA8q1JBKFsaSpvw0ZEw%2Bwc7cv3mwUsZSx5K%2F2TcqLIK5%2BcrHyavKVm3%2BCH2ZLbUwVb8wJMP5Vq3EyRv%2FLU60KeFtCDwm2i9YlaBALzb8wg4rEn5BbCHIjMkiBGlKlqBZt7R4lGvYyvVzHSScARHiRb1ZvmJTvWy72hCsI8HmOBzWBiC9Om5ZPqnCuP%2BiHEVHwfGmumMIDtTM5G66KamEjyz7zORIVcABT%2FEFTyFC8w0LGS1rKdAmidaTjucN6nyjZvrG0%2BMLOTibXYJ4uz6gGFXn8L881kHjMS0kMco09u2ru5%2Fn286p%2BAegQXlix70weWdr8jmF6RIDh5IvJX91ydrFmhXQODdyqNgiM%2BhjSkySl%2BvcKZCKvW7BJpyEyV001iJzcFd715XB4U%2F7LPCYkt8vvLuaLVtIRrSOdjVRTUF1a7EyTO8m7UsmGk2wn3uRGuDf5aUX0gKvAIchoguM6wjmlImzGIccTfSJzvAjCe7RQzapenB309HqUVXxIJLekHN7hwidimfD7UJpXANrY79DiNym4lMx8j0ekb3evNm%2BsZS%2BiXi06tvcxtZ4qKSrAljJsTqgWJfvMcMfAcma1GtBCx7dNs9tMC7VCXte7wyQFOBGMueUmvPP%2BP1J7cI57bjfvoY%2FtSSVUGGE%2B32c1I4g15cl5zeDs%2FSSfjPJXUj22QCkZo3OcfuRQnHDb7PhmHvKm5Bqsjtsv2KGr8nLFGaVwCoG48qMV9FLEqegxSse%2BlcyEIeBLNSilm8Lqay7mnjD1uU8pNzRxJyA1inLzL4DdaDZ%2BaayZP1acYt2C4h5IvLJT2v89xgFOsTnZRyP7mKlavNfrwU5Dn8AWFA2KPC7jZBGlkcRW6%2B2kbWG5RBMB1h4uR%2FYWupmsGFk0oI7Sqq49WliU5vSJ3K9swMKWPJCEoJvcJC%2Fy1WU9tc0thED3Gj1LOLRgf9pBlQzUXCC0ugTNnjhcmxRR83EPV1mR6LSmVZCx0N9F4jNpHzsox12P9v%2BMs0Es04rautPZs1I9AcAxy8AArnmqK8AhxPUWST48jbl70S6rhzu79jTig83l4gNd%2FuqNFLsD7MMcbZ0rynBQvZlbgy3ZTdiHrdFWMZ%2FOJHmDuGvepjohIgSr2INo%2BtlUOvLpOjxlfBAN7G05iRCFe5dviEzK5MqD1rKuDGmR1MJdkr8m4mf0s2ngU3C0fswoTJSKDqhr2%2FI8H%2BVZtQ6Lk3SAql0lJsk4zvqacpPEHxBz5spX6msVDInE6ZfiiDYxjO8NgOfoQLQ6%2BirUyxWKwfQFM9l4zHjcS1Wn731z2Iwy2T20Y0G0Wn%2B7%2F99a%2FGYjS4E2u6fkrDaFyccnQY1h8TxMaMBHoxZP49g09oS66C6L5YhrYWV9YUegxRySPwvoRkrMVyJwjNOGlLpF3T9Kd36%2BfJIRJz3zr1bovSa2pX66rEb06ohX2CCRnu2kGUQOsRveyv2N3XTWLBXVSMVvOLNuUYz321rrIb8UBePbBCJud4qrTBd6%2BPbuwn0wxwGdPEr5AeARpUuAKMs17fkTAIkxz71IcMXi7wb5XvH97RcrovwmAurHFFKTmeqzsZFHNEWycnDr0tOgYkbaGDTHfZIi14hXAL%2Fy%2FJUuY0VJ30zTH5b36rrM7paT16bnXn143DyGWrDdRoGClgrIyDoDEngPoUVc14KfNkggknxfd6tj8B%2BAHjWpucNGY7Aq1GIW5VDyhBg1oKOcOMVGJyLUiv4E8RHFHL5JtLYbMqr9B%2FyVfxTcez5QzXEY3Q6qitrU2fCV8rRD9UGCrogWkJXwtNLlHL%2Bo%2BHwe1PDpXU5FUuOtPhZ4u3uwdVY5s%2B3SM3AYaFqUL0ULFcnYguF8KqlP6pbFKDB2FJw%2FbZrI4y3udWOaSpZYjQZqGPEsJvJpXAFGKXIQIxHtyMJ9fgudyhVSE6fz3Nymu4Vykg9LodsrIYPbReUkUE3GnwydzyPBNCBgumAgBwBck0HJLtt%2BxGf6B6hrBsiRftQ90C5zpxrGp%2Bs%2FzLnZp1ucpTPTUEK%2Bm%2FUaAjIA5PuS2cYnwG0MriYEkjxfsI2l8SassJDHDhTXHSXOcN4tMvE3LPTgb0pSWO3D82nrTZSO2AVWORoSbiKIC%2B0gpfiyPh6RknPB9TOOzRr4ID9QMyUpr4UNcACaVMJOY83ejLfEohkITM0DsMTBNpw1FKRB9jkoTop8oLuUjyJXXTz9d5fVBIlnVV%2Bfec9AqYIeIq%2BUKzFT%2FhUa%2BW9gLwDfmpff9qp3YCQT6dai0QEMWZY9xjRA4nrQ2AV2IrifPUkA0s13TQFvT3A4B4HJ9IC6TdoFwAMnzsDAYKkCl8GEAbp0KABbwxgXry3XcV%2FAa9OUOhx2FeENLMEmFP3aN33mWXNHcmT15gY6WYS%2BIf4BSwDQZ%2FCRgqobEcOqSvG1RrGJUudzMpp3PfcVPUHytQ%2BmSRG%2Bvq43%2BJ3a8q9rzkoIcTBcdTegNm80LNkUcvvQlJ%2BKNqFFaIhuFCkVcitb1GIexl4pTM6MrRw0myegdgcP1%2BZOGabyAWFWP83WcpelHNuZMamNSQB4%2FrPWbn063yOXtrTWDYL5D0gEKFq3fsQ3WEJYoxAS5EY9ckX0p8i5r%2BkoANh2OmGgZXS%2BLhdjDX4qJgdSauJfxxG%2F8ZC%2Fu%2FBgr3A5ob%2BteFPRg7bfPrx0W0%2FgQLgmtS2UMJyh6%2BMR6u5Y6TYV%2Fu5DQhrOuQ25KzRrEY9eakK9ssZXbOBxgZ6DPCFdwkZSVe2UOH831TUn9MsEAV8s21T87cj0yrZw%2Ffa3alHT2u6Z7Qd9lnCafgUjbrSSdSQmD47TzGLpsYptQybQDGD6kgqkoZo2Rp0JhhxCYMKkil5rxThlWl%2Fza1xFWyRGaOtft3xXLqDUvBrol83dyj7dNmLG2DQlWiuIVmk9qezxA%2BOEkYlItgo0dL0kVHPCxEVwDrnULOLRu7y0vvtqY9XwJxso6IvBO2h10CfhTpbk9r3FwNaDkj8l212MrCjKhPN3q0RKzWTRwgO73Gwphix4Ngh9ZOmurUx5%2BHD%2FPzpXpKzgKu1Z%2FyTh%2BXvc9iC2SAiOkydC%2FzL3sT%2F37KtvnFcgCmArBz3LHPhm2Z8P3nwhl9aISYjpy2jde5yhx%2BNKIPopdYGUCvd%2BfaSUEIYT8DdQiuaC7iWYc2cSVb6H5IHZwPCRe9%2FmnpfmCaNoEw9CgQVytM4gKOn3m3jiRBB5yW6svFVN5VL5ifB7%2F%2FYEeicvTBMX%2B2%2BepjIY5LgQHAjip7D6owKXPaMMF6iAtf0tdvyIqyWV64a854gCaj1vNj0VIdipbamBjUKUxFcl8bLihIy32hk9JW27uWp82ePogVyI9ggVO5tIHkrzdzAx9jzWWpM7MqYiOA3plvf214JLiT6cLuacjkUprs1oPltzw9TLJBz6lrSie%2B%2FPzk4tKXx9V2ToKQowYMmEN%2BU7q1DQWKzGFvzq10Q1PVZIvpXo3gf%2BDv2zwlSU7RdrngWuFvR7cuwSxNj7xyAmbAGv2ERy4CzrdfJvPpNDGY7qCho7K3%2BAVZYXqpbzIdUzWBqTx47%2BZlq8vjlYggHTewFpmKned%2B6FYP%2BoxwK3W7IesGD%2Fq9H3qnB5feG4PIZKrCdpmDPPpMXm3oTIibQpdRjE10n5cyf48WeIbBgWxJ63pjsxQB9jCfEOiXtPb8nwLVV2zyrpRoHJ%2F9vM%2BNxospTwPnGoHgQ6Xk9P47bloqSsZKpVLwyozWndWbS1A%2BonKyE85hoOydpSq9b%2FGj058Uz4mnSaKZA3bGshCnnDvPgd%2BfB1lOh9EwThaChgcns46znuT0IOxglPQUFBcIXGlyIH49pLFEsgU7dftmCdNSXbtdomXIuxpZWvz%2BuhdIpOOCIYH5%2BTy%2BR4KlsQp8VJBSgqBzfjIFT7lHwndPxyEaG9nWWTLq4YCCLiWbGYFiOY3uq%2Fkz5MvoxxWqGlHuqBPjHfH5ukEgC%2F%2BQQL7b%2Fdl9ZLEA1EpdsVud%2Btd0EOt6ejF%2Bc5B1P2IMDVM5z0V17SRidUuqQ2g3%2FK72WpliTZraE2072Z6U21BA%2FSs3Hg93AiHnMLJh7FPZJ6q4uzwMQV2nWU4N28v2HQWAeSBBkI%2Br%2BmMUD0OukDLGXirCT2U4n2vEELdyr3R%2FBGHOYGTCPO6O67Kgj6oS%2B2zLZTdpil36lyc%2BBMd8s6wwDPVeEJAMv%2BKkXpTOW6iSYRkxxbR4OYOHJkgEhqdpw5HVazLWgPuj%2FQ9xlq%2BPmHwMhEfje6ZkhRbl0NX5tOBrS%2B%2Fg%2F3vlVcTkHGttFP4vPzoB%2BLQr5QKw0ODx87C26hN5PKJMoVVKDJUqTu4%2BuCFK3Nm9HeKW5rcwGVDBdHKBkB535kECldQQSIyCJtbaRLZboV8O3%2BLHSOKdG7O2nYajG6A5g4rlG1JjQJXd0D2yqFAhstY9yFpIbXdI3KPtaQqiLJaPKE2Xw%2Blp45eUXt%2Fek%2FGlDzNC6ea0sQ%2F1dWXmZJ0Nyg4xLQT4p9OXCap%2Bi4Yr4nhgqe%2BCxyjVqGl4DOGqiShCNawfXsO9%2F1Za7SZoBWV8Us65kC2TiYR1xQi5HmYkU%2Fcv37L1jFFdGnMAl0KwshSx7eH9yzOcDYHPILNvN5i%2FN0VO3WWSN96ytoNPL1wetDgHytXMS1icniP3RKL5Bqd63uQrmMitWCvYnc3ncc8R3eT1guyY%2BFuC2uz4AbvjfUq8YCuig2%2F2SfbqtMYtzc9LcjR6HhfM%2FkUlBGX8PvtWvBj115p9u6AVRk0UCcOyI9XfgiLMcV5JVjY0667qdUFUwRI77f0APt1nDW25AqmVIVlZTnzHGGfSv2%2FN%2F%2B7P3spPbbciCM6csjVAehnwPeOCS21Oem2H8CpxDIWBxIJD%2FhyLtudwLdU0W43xJ9j6OTcTQ9tDdzqDKDvvgVbMkxca7WkO%2FL8ZPQjCrSpk6Mk8sceHi16wZ710MNsNkMX2SG%2Bw1%2FETuWb3V5w5zO7xHmg21HrHGAV7Ofp4ycGmXrT7euZvngNcf32ornbhQaw%3D%3D&__VIEWSTATEGENERATOR=E50C1FF0&__EVENTVALIDATION=kU%2FBWyRUFVyQyHVOnCYu9FLF3J6qu3rG8Ut%2BgVml07WtCaSMk3vJoggcwtI068Y2M7Z9kW5qsEVU0HF8qtN0aauzLsgK8Vk7pYdwhe701KoAKknjDK9DTGTq%2FyhN1Bh09rcJauQYFccI6V2ZMykx%2F7RdUkhqmNffnZ2WkOPKRoHQZthBsyvzKdHF889zjHWuJJ4gIGR4M%2F9ED5S1rpuEyO8v7OdgCpsqlLB3RwS1loftwcWXuh8JatZd2mkFSHAY%2Bxr4g5ywgQ4ahJdKN4UJGgO3nK8%3D&VMFormRicerca6CurrentViewID=FindView&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24FormSC1HiddenNew=None&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld183413226=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld107018220Nested1=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld107018220=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld107018255Nested1=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld107018255=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld183413227Nested1=&VMFormRicerca6%24FindView%24FormRicerca%24FormSC1%24Fld183413227=&VMFormRicerca6%24FindView%24FormRicerca%24SCViewFindHiddenNew=None&VM9CurrentViewID=TableView&ReportGrid183407671=&VM9%24TableView%24SCViewReport%24FormSC2%24FormSC2HiddenNew=None&VM9%24TableView%24SCViewReport%24HdnQueryString=&VM9%24TableView%24SCViewReport%24SCViewReportHiddenNew=None&companyid=14602723&VM9%24TableView%24SCViewReport%24ctl03={0}'''.format(web)

    req = requests.post(url = 'https://www.lavorareinatm.it/elenco-annunci', headers = headers, data = data)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://www.lavorareinatm.it/jobs/{0}".format(x.get("url", "")) for x in sl.M]

    #Para pruebas
    # sl.printWR()
    # exit(0)
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = re.sub("","",offer.get("title", ""))
        ad['description'] = re.sub("","",offer.get("description", ""))
        ad['url'] = re.sub("","",offer.get("@url", ""))
        ad['city'] = re.sub("","",offer.get("city", ""))
        ad['province'] = re.sub("","",offer.get("province", ""))
        ad['salary'] = re.sub("","",offer.get("salary",'0'))
        ad['company'] = re.sub("","",offer.get("company", ""))
        ad['contract'] = re.sub("","",offer.get("contract", ""))
        
        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$","",offer.get("title_aux",""))

        yield ad

#saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug=False)
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
