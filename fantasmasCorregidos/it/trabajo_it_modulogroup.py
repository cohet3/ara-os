# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from urlparse import parse_qs
from urllib import urlencode
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'modulogroup.sites.altamiraweb.com'

xtr = '''city
"addressLocality": "
"
title
data-title="Titolo">
</span>
description
data-title="Testo">
</table>'''

xtr_view = '''viewstate
id="__VIEWSTATE" value="
"
generator
id="__VIEWSTATEGENERATOR" value="
"
validation
id="__EVENTVALIDATION" value="
"'''


stp = 'Annunci/J'
page_ads = 10 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 5))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'http://modulogroup.sites.altamiraweb.com/!__VIEWSTATE=%2FwEPDwUBMA9kFgICAg9kFgICAQ9kFgICDQ9kFgJmD2QWAgIDD2QWAgIBD2QWAgIDD2QWAgIBD2QWAgIBD2QWAgIDD2QWBGYPZBYEAgEPZBYCZg8WAh4ZVk1Gb3JtUmljZXJjYTM6UGFyYW1ldGVyczKrDAABAAAA%2F%2F%2F%2F%2FwEAAAAAAAAADAIAAABQQWx0YW1pcmEuV2ViLlVJLCBWZXJzaW9uPTIwMTcuMy42NzE4LjI1MTY5LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAACBBbHRhbWlyYS5XZWIuRGF0YS5EYXRhQ29sbGVjdGlvbgIAAAAKbV9PcGVyYXRvchNDb2xsZWN0aW9uQmFzZStsaXN0BAMcQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgIAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAIAAAAF%2Ff%2F%2F%2FxxBbHRhbWlyYS5XZWIuVUkuVHlwZU9wZXJhdG9yAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAkEAAAABAQAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAMAAAAGX2l0ZW1zBV9zaXplCF92ZXJzaW9uBQAACAgJBQAAAAYAAAAHAAAAEAUAAAAIAAAACQYAAAAJBwAAAAkIAAAACQkAAAAJCgAAAAkLAAAADQIFBgAAABxBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0CgAAAAdtX1RhYmxlC21fRmllbGROYW1lDW1fQ29udHJvbE5hbWUHbV9WYWx1ZQ9tX1ZhbHVlRXh0ZW5kZWQMbV9Db21wYXJpc29uBm1fVHlwZRBtX011bHRpcGxlVmFsdWVzC21fRGF0YUJvdW5kEG1fU3Vic3RpdHV0ZVBpcGUBAQECAgQEAAABK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0CAAAAGEFsdGFtaXJhLldlYi5VSS5UeXBlRW51bQIAAAABAQIAAAAKBgwAAAACSUQJDAAAAAYNAAAAC0Zvcm1SaWNlcmNhCgXy%2F%2F%2F%2FK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0BAAAAB3ZhbHVlX18ACAIAAAABAAAABfH%2F%2F%2F8YQWx0YW1pcmEuV2ViLlVJLlR5cGVFbnVtAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAABBhAAAAAHJSMxMjQjJQEHAAAABgAAAAoGEQAAABNTdWJtaXRPbkVudGVyQnV0dG9uCREAAAAGEgAAAAdjbWRGaW5kCgHt%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB7P%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEIAAAABgAAAAoGFgAAAAhDc3NDbGFzcwkWAAAABhcAAAAACgHo%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB5%2F%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEJAAAABgAAAAoGGwAAAARuYW1lCRsAAAAGHAAAABxGcm9udG9mZmljZTogUmljZXJjYSBBbm51bmNpCgHj%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB4v%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEKAAAABgAAAAoGIAAAAAlIdG1sSW5wdXQJIAAAAAYhAAAAygINCg0KCTxkaXYgY2xhc3M9ImJveCI%2BUGFyb2xlIGNoaWF2ZSA8L2Rpdj4NCgk8ZGl2IGNsYXNzPSJib3giPjxjbXM6ZmllbGQgVGFnTmFtZT0iSm9icy5GcmVlU2VhcmNoIiAvPjwvZGl2Pg0KCTxkaXYgY2xhc3M9ImJveCI%2BU2VkaSA8L2Rpdj4NCgk8ZGl2IGNsYXNzPSJib3giPjxjbXM6ZmllbGQgVGFnTmFtZT0iTG9jYXRpb25zLlByZWZlcnJlZExvY2F0aW9ucyIgLz4gPC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij5CdXNpbmVzcyB1bml0PC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij48Y21zOmZpZWxkIFRhZ05hbWU9IlZhY2FuY3kuQnVzaW5lc3NVbml0cyIgLz48L2Rpdj4gDQoKAd7%2F%2F%2F%2Fy%2F%2F%2F%2FAQAAAAHd%2F%2F%2F%2F8f%2F%2F%2FwAAAAAAAQkQAAAAAQsAAAAGAAAACgYlAAAAElJlc291cmNlRG9jdW1lbnRJRAklAAAACAiVerwGCgHa%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB2f%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAsWAmYPFgIeIlZNRm9ybVJpY2VyY2EzJEZpbmRWaWV3OlBhcmFtZXRlcnMyqwwAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAwCAAAAUEFsdGFtaXJhLldlYi5VSSwgVmVyc2lvbj0yMDE3LjMuNjcxOC4yNTE2OSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAgQWx0YW1pcmEuV2ViLkRhdGEuRGF0YUNvbGxlY3Rpb24CAAAACm1fT3BlcmF0b3ITQ29sbGVjdGlvbkJhc2UrbGlzdAQDHEFsdGFtaXJhLldlYi5VSS5UeXBlT3BlcmF0b3ICAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QCAAAABf3%2F%2F%2F8cQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgEAAAAHdmFsdWVfXwAIAgAAAAAAAAAJBAAAAAQEAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QDAAAABl9pdGVtcwVfc2l6ZQhfdmVyc2lvbgUAAAgICQUAAAAGAAAABwAAABAFAAAACAAAAAkGAAAACQcAAAAJCAAAAAkJAAAACQoAAAAJCwAAAA0CBQYAAAAcQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdAoAAAAHbV9UYWJsZQttX0ZpZWxkTmFtZQ1tX0NvbnRyb2xOYW1lB21fVmFsdWUPbV9WYWx1ZUV4dGVuZGVkDG1fQ29tcGFyaXNvbgZtX1R5cGUQbV9NdWx0aXBsZVZhbHVlcwttX0RhdGFCb3VuZBBtX1N1YnN0aXR1dGVQaXBlAQEBAgIEBAAAAStBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0K0NvbXBhcmlzb25FbnVtAgAAABhBbHRhbWlyYS5XZWIuVUkuVHlwZUVudW0CAAAAAQECAAAACgYMAAAAAklECQwAAAAGDQAAAAtGb3JtUmljZXJjYQoF8v%2F%2F%2FytBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0K0NvbXBhcmlzb25FbnVtAQAAAAd2YWx1ZV9fAAgCAAAAAQAAAAXx%2F%2F%2F%2FGEFsdGFtaXJhLldlYi5VSS5UeXBlRW51bQEAAAAHdmFsdWVfXwAIAgAAAAAAAAAAAQYQAAAAByUjMTI0IyUBBwAAAAYAAAAKBhEAAAATU3VibWl0T25FbnRlckJ1dHRvbgkRAAAABhIAAAAHY21kRmluZAoB7f%2F%2F%2F%2FL%2F%2F%2F8BAAAAAez%2F%2F%2F%2Fx%2F%2F%2F%2FAAAAAAABCRAAAAABCAAAAAYAAAAKBhYAAAAIQ3NzQ2xhc3MJFgAAAAYXAAAAAAoB6P%2F%2F%2F%2FL%2F%2F%2F8BAAAAAef%2F%2F%2F%2Fx%2F%2F%2F%2FAAAAAAABCRAAAAABCQAAAAYAAAAKBhsAAAAEbmFtZQkbAAAABhwAAAAcRnJvbnRvZmZpY2U6IFJpY2VyY2EgQW5udW5jaQoB4%2F%2F%2F%2F%2FL%2F%2F%2F8BAAAAAeL%2F%2F%2F%2Fx%2F%2F%2F%2FAAAAAAABCRAAAAABCgAAAAYAAAAKBiAAAAAJSHRtbElucHV0CSAAAAAGIQAAAMoCDQoNCgk8ZGl2IGNsYXNzPSJib3giPlBhcm9sZSBjaGlhdmUgPC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij48Y21zOmZpZWxkIFRhZ05hbWU9IkpvYnMuRnJlZVNlYXJjaCIgLz48L2Rpdj4NCgk8ZGl2IGNsYXNzPSJib3giPlNlZGkgPC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij48Y21zOmZpZWxkIFRhZ05hbWU9IkxvY2F0aW9ucy5QcmVmZXJyZWRMb2NhdGlvbnMiIC8%2BIDwvZGl2Pg0KCTxkaXYgY2xhc3M9ImJveCI%2BQnVzaW5lc3MgdW5pdDwvZGl2Pg0KCTxkaXYgY2xhc3M9ImJveCI%2BPGNtczpmaWVsZCBUYWdOYW1lPSJWYWNhbmN5LkJ1c2luZXNzVW5pdHMiIC8%2BPC9kaXY%2BIA0KCgHe%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB3f%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAELAAAABgAAAAoGJQAAABJSZXNvdXJjZURvY3VtZW50SUQJJQAAAAgIlXq8BgoB2v%2F%2F%2F%2FL%2F%2F%2F8BAAAAAdn%2F%2F%2F%2Fx%2F%2F%2F%2FAAAAAAABCRAAAAALFgJmDw8WAh4uVk1Gb3JtUmljZXJjYTMkRmluZFZpZXckRm9ybVJpY2VyY2E6UGFyYW1ldGVyczKrDAABAAAA%2F%2F%2F%2F%2FwEAAAAAAAAADAIAAABQQWx0YW1pcmEuV2ViLlVJLCBWZXJzaW9uPTIwMTcuMy42NzE4LjI1MTY5LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAACBBbHRhbWlyYS5XZWIuRGF0YS5EYXRhQ29sbGVjdGlvbgIAAAAKbV9PcGVyYXRvchNDb2xsZWN0aW9uQmFzZStsaXN0BAMcQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgIAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAIAAAAF%2Ff%2F%2F%2FxxBbHRhbWlyYS5XZWIuVUkuVHlwZU9wZXJhdG9yAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAkEAAAABAQAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAMAAAAGX2l0ZW1zBV9zaXplCF92ZXJzaW9uBQAACAgJBQAAAAYAAAAHAAAAEAUAAAAIAAAACQYAAAAJBwAAAAkIAAAACQkAAAAJCgAAAAkLAAAADQIFBgAAABxBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0CgAAAAdtX1RhYmxlC21fRmllbGROYW1lDW1fQ29udHJvbE5hbWUHbV9WYWx1ZQ9tX1ZhbHVlRXh0ZW5kZWQMbV9Db21wYXJpc29uBm1fVHlwZRBtX011bHRpcGxlVmFsdWVzC21fRGF0YUJvdW5kEG1fU3Vic3RpdHV0ZVBpcGUBAQECAgQEAAABK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0CAAAAGEFsdGFtaXJhLldlYi5VSS5UeXBlRW51bQIAAAABAQIAAAAKBgwAAAACSUQJDAAAAAYNAAAAC0Zvcm1SaWNlcmNhCgXy%2F%2F%2F%2FK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0BAAAAB3ZhbHVlX18ACAIAAAABAAAABfH%2F%2F%2F8YQWx0YW1pcmEuV2ViLlVJLlR5cGVFbnVtAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAABBhAAAAAHJSMxMjQjJQEHAAAABgAAAAoGEQAAABNTdWJtaXRPbkVudGVyQnV0dG9uCREAAAAGEgAAAAdjbWRGaW5kCgHt%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB7P%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEIAAAABgAAAAoGFgAAAAhDc3NDbGFzcwkWAAAABhcAAAAACgHo%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB5%2F%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEJAAAABgAAAAoGGwAAAARuYW1lCRsAAAAGHAAAABxGcm9udG9mZmljZTogUmljZXJjYSBBbm51bmNpCgHj%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB4v%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAEKAAAABgAAAAoGIAAAAAlIdG1sSW5wdXQJIAAAAAYhAAAAygINCg0KCTxkaXYgY2xhc3M9ImJveCI%2BUGFyb2xlIGNoaWF2ZSA8L2Rpdj4NCgk8ZGl2IGNsYXNzPSJib3giPjxjbXM6ZmllbGQgVGFnTmFtZT0iSm9icy5GcmVlU2VhcmNoIiAvPjwvZGl2Pg0KCTxkaXYgY2xhc3M9ImJveCI%2BU2VkaSA8L2Rpdj4NCgk8ZGl2IGNsYXNzPSJib3giPjxjbXM6ZmllbGQgVGFnTmFtZT0iTG9jYXRpb25zLlByZWZlcnJlZExvY2F0aW9ucyIgLz4gPC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij5CdXNpbmVzcyB1bml0PC9kaXY%2BDQoJPGRpdiBjbGFzcz0iYm94Ij48Y21zOmZpZWxkIFRhZ05hbWU9IlZhY2FuY3kuQnVzaW5lc3NVbml0cyIgLz48L2Rpdj4gDQoKAd7%2F%2F%2F%2Fy%2F%2F%2F%2FAQAAAAHd%2F%2F%2F%2F8f%2F%2F%2FwAAAAAAAQkQAAAAAQsAAAAGAAAACgYlAAAAElJlc291cmNlRG9jdW1lbnRJRAklAAAACAiVerwGCgHa%2F%2F%2F%2F8v%2F%2F%2FwEAAAAB2f%2F%2F%2F%2FH%2F%2F%2F8AAAAAAAEJEAAAAAtkFgJmD2QWAgIDD2QWBgIED2QWBGYPDxYCHgRUZXh0ZWRkAgEPDxYKHgxFcnJvck1lc3NhZ2UFZklsIGNhbXBvICJSaWNlcmNhIGxpYmVyYSIgZGV2ZSBlc3NlcmUgZGkgdGlwbyAiVGVzdG8iIChmb3JtYXQ6ICIlJXR5cGVfdGV4dCUlIiBmb3IgIiUlZXhhbXBsZV90ZXh0JSUiKR4HRGlzcGxheQsqKlN5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuVmFsaWRhdG9yRGlzcGxheQIeDFJlcXVpcmVkVHlwZQspekFsdGFtaXJhLldlYi5WYWxpZGF0aW9uLlJlcXVpcmVkVHlwZUVudW0sIEFsdGFtaXJhLldlYi5VSSwgVmVyc2lvbj0yMDE3LjMuNjcxOC4yNTE2OSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsAB4RQ29udHJvbFRvVmFsaWRhdGUFDEZsZDExODAxNTA4OB4MQ29udHJvbExhYmVsBQ5SaWNlcmNhIGxpYmVyYWRkAggPZBYCAgEPFgIeBVZhbHVlZWQCDA9kFgICAQ8WAh8JZWQCAw9kFgICAQ9kFgJmDxYCHgVjbGFzcwUGYnV0dG9uZAICD2QWCAIDD2QWAgIBD2QWAmYPFgIeDlZNNjpQYXJhbWV0ZXJzMsQIAAEAAAD%2F%2F%2F%2F%2FAQAAAAAAAAAMAgAAAFBBbHRhbWlyYS5XZWIuVUksIFZlcnNpb249MjAxNy4zLjY3MTguMjUxNjksIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAIEFsdGFtaXJhLldlYi5EYXRhLkRhdGFDb2xsZWN0aW9uAgAAAAptX09wZXJhdG9yE0NvbGxlY3Rpb25CYXNlK2xpc3QEAxxBbHRhbWlyYS5XZWIuVUkuVHlwZU9wZXJhdG9yAgAAABxTeXN0ZW0uQ29sbGVjdGlvbnMuQXJyYXlMaXN0AgAAAAX9%2F%2F%2F%2FHEFsdGFtaXJhLldlYi5VSS5UeXBlT3BlcmF0b3IBAAAAB3ZhbHVlX18ACAIAAAAAAAAACQQAAAAEBAAAABxTeXN0ZW0uQ29sbGVjdGlvbnMuQXJyYXlMaXN0AwAAAAZfaXRlbXMFX3NpemUIX3ZlcnNpb24FAAAICAkFAAAABAAAAAUAAAAQBQAAAAQAAAAJBgAAAAkHAAAACQgAAAAJCQAAAAUGAAAAHEFsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QKAAAAB21fVGFibGULbV9GaWVsZE5hbWUNbV9Db250cm9sTmFtZQdtX1ZhbHVlD21fVmFsdWVFeHRlbmRlZAxtX0NvbXBhcmlzb24GbV9UeXBlEG1fTXVsdGlwbGVWYWx1ZXMLbV9EYXRhQm91bmQQbV9TdWJzdGl0dXRlUGlwZQEBAQICBAQAAAErQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdCtDb21wYXJpc29uRW51bQIAAAAYQWx0YW1pcmEuV2ViLlVJLlR5cGVFbnVtAgAAAAEBAgAAAAoGCgAAAAdUYWdOYW1lCQoAAAAGCwAAABlOdW1lcm8uYW5udW5jaS5wdWJibGljYXRpCgX0%2F%2F%2F%2FK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0BAAAAB3ZhbHVlX18ACAIAAAABAAAABfP%2F%2F%2F8YQWx0YW1pcmEuV2ViLlVJLlR5cGVFbnVtAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAABBg4AAAAHJSMxMjQjJQEHAAAABgAAAAoGDwAAAA1IaWRkZW5Db2x1bW5zCQ8AAAAGEAAAAAxKb2JzLlN0YXRlSUQKAe%2F%2F%2F%2F%2F0%2F%2F%2F%2FAQAAAAHu%2F%2F%2F%2F8%2F%2F%2F%2FwAAAAAAAQkOAAAAAQgAAAAGAAAACgYUAAAACUh0bWxJbnB1dAkUAAAABhUAAAAACgHq%2F%2F%2F%2F9P%2F%2F%2FwEAAAAB6f%2F%2F%2F%2FP%2F%2F%2F8AAAAAAAEJDgAAAAEJAAAABgAAAAoGGQAAABJSZXNvdXJjZURvY3VtZW50SUQJGQAAAAgIlXq8BgoB5v%2F%2F%2F%2FT%2F%2F%2F8BAAAAAeX%2F%2F%2F%2Fz%2F%2F%2F%2FAAAAAAABCQ4AAAALFgJmDxYCHhhWTTYkVGFibGVWaWV3OlBhcmFtZXRlcnMyxAgAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAwCAAAAUEFsdGFtaXJhLldlYi5VSSwgVmVyc2lvbj0yMDE3LjMuNjcxOC4yNTE2OSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAgQWx0YW1pcmEuV2ViLkRhdGEuRGF0YUNvbGxlY3Rpb24CAAAACm1fT3BlcmF0b3ITQ29sbGVjdGlvbkJhc2UrbGlzdAQDHEFsdGFtaXJhLldlYi5VSS5UeXBlT3BlcmF0b3ICAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QCAAAABf3%2F%2F%2F8cQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgEAAAAHdmFsdWVfXwAIAgAAAAAAAAAJBAAAAAQEAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QDAAAABl9pdGVtcwVfc2l6ZQhfdmVyc2lvbgUAAAgICQUAAAAEAAAABQAAABAFAAAABAAAAAkGAAAACQcAAAAJCAAAAAkJAAAABQYAAAAcQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdAoAAAAHbV9UYWJsZQttX0ZpZWxkTmFtZQ1tX0NvbnRyb2xOYW1lB21fVmFsdWUPbV9WYWx1ZUV4dGVuZGVkDG1fQ29tcGFyaXNvbgZtX1R5cGUQbV9NdWx0aXBsZVZhbHVlcwttX0RhdGFCb3VuZBBtX1N1YnN0aXR1dGVQaXBlAQEBAgIEBAAAAStBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0K0NvbXBhcmlzb25FbnVtAgAAABhBbHRhbWlyYS5XZWIuVUkuVHlwZUVudW0CAAAAAQECAAAACgYKAAAAB1RhZ05hbWUJCgAAAAYLAAAAGU51bWVyby5hbm51bmNpLnB1YmJsaWNhdGkKBfT%2F%2F%2F8rQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdCtDb21wYXJpc29uRW51bQEAAAAHdmFsdWVfXwAIAgAAAAEAAAAF8%2F%2F%2F%2FxhBbHRhbWlyYS5XZWIuVUkuVHlwZUVudW0BAAAAB3ZhbHVlX18ACAIAAAAAAAAAAAEGDgAAAAclIzEyNCMlAQcAAAAGAAAACgYPAAAADUhpZGRlbkNvbHVtbnMJDwAAAAYQAAAADEpvYnMuU3RhdGVJRAoB7%2F%2F%2F%2F%2FT%2F%2F%2F8BAAAAAe7%2F%2F%2F%2Fz%2F%2F%2F%2FAAAAAAABCQ4AAAABCAAAAAYAAAAKBhQAAAAJSHRtbElucHV0CRQAAAAGFQAAAAAKAer%2F%2F%2F%2F0%2F%2F%2F%2FAQAAAAHp%2F%2F%2F%2F8%2F%2F%2F%2FwAAAAAAAQkOAAAAAQkAAAAGAAAACgYZAAAAElJlc291cmNlRG9jdW1lbnRJRAkZAAAACAiVerwGCgHm%2F%2F%2F%2F9P%2F%2F%2FwEAAAAB5f%2F%2F%2F%2FP%2F%2F%2F8AAAAAAAEJDgAAAAsWAmYPZBYCZg9kFgRmDw8WAh4HVmlzaWJsZWhkZAIBDw8WAh8NaGRkAgUPZBYCAgEPZBYCZg8WBB8KBQZidXR0b24eAmlkBQ5Qb3J0bGV0QnV0dG9uN2QCCQ9kFgJmDxYCHg5WTTg6UGFyYW1ldGVyczLrDAABAAAA%2F%2F%2F%2F%2FwEAAAAAAAAADAIAAABQQWx0YW1pcmEuV2ViLlVJLCBWZXJzaW9uPTIwMTcuMy42NzE4LjI1MTY5LCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPW51bGwFAQAAACBBbHRhbWlyYS5XZWIuRGF0YS5EYXRhQ29sbGVjdGlvbgIAAAAKbV9PcGVyYXRvchNDb2xsZWN0aW9uQmFzZStsaXN0BAMcQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgIAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAIAAAAF%2Ff%2F%2F%2FxxBbHRhbWlyYS5XZWIuVUkuVHlwZU9wZXJhdG9yAQAAAAd2YWx1ZV9fAAgCAAAAAAAAAAkEAAAABAQAAAAcU3lzdGVtLkNvbGxlY3Rpb25zLkFycmF5TGlzdAMAAAAGX2l0ZW1zBV9zaXplCF92ZXJzaW9uBQAACAgJBQAAAAoAAAALAAAAEAUAAAAQAAAACQYAAAAJBwAAAAkIAAAACQkAAAAJCgAAAAkLAAAACQwAAAAJDQAAAAkOAAAACQ8AAAANBgUGAAAAHEFsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QKAAAAB21fVGFibGULbV9GaWVsZE5hbWUNbV9Db250cm9sTmFtZQdtX1ZhbHVlD21fVmFsdWVFeHRlbmRlZAxtX0NvbXBhcmlzb24GbV9UeXBlEG1fTXVsdGlwbGVWYWx1ZXMLbV9EYXRhQm91bmQQbV9TdWJzdGl0dXRlUGlwZQEBAQICBAQAAAErQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdCtDb21wYXJpc29uRW51bQIAAAAYQWx0YW1pcmEuV2ViLlVJLlR5cGVFbnVtAgAAAAEBAgAAAAoGEAAAAARuYW1lCRAAAAAGEQAAABpGcm9udG9mZmljZTogTGlzdGEgQW5udW5jaQoF7v%2F%2F%2FytBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0K0NvbXBhcmlzb25FbnVtAQAAAAd2YWx1ZV9fAAgCAAAAAQAAAAXt%2F%2F%2F%2FGEFsdGFtaXJhLldlYi5VSS5UeXBlRW51bQEAAAAHdmFsdWVfXwAIAgAAAAAAAAAAAQYUAAAAByUjMTI0IyUBBwAAAAYAAAAKBhUAAAAOT3JkZXJCeUNvbHVtbnMJFQAAAAYWAAAAF0pvYnMuRGF0ZVB1Ymxpc2hlZCBERVNDCgHp%2F%2F%2F%2F7v%2F%2F%2FwEAAAAB6P%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAEIAAAABgAAAAoGGgAAAA9DbGljY2FibGVDb2x1bW4JGgAAAAYbAAAACkpvYnMuVGl0bGUKAeT%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHj%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQkAAAAGAAAACgYfAAAAA3VybAkfAAAABiAAAAAKJSVKT0JVUkwlJQoB3%2F%2F%2F%2F%2B7%2F%2F%2F8BAAAAAd7%2F%2F%2F%2Ft%2F%2F%2F%2FAAAAAAABCRQAAAABCgAAAAYAAAAKBiQAAAAQTm9SZWNvcmRzTWVzc2FnZQkkAAAABiUAAAAXTmVzc3VuIGFubnVuY2lvIHRyb3ZhdG8KAdr%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHZ%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQsAAAAGAAAACgYpAAAADUhpZGRlbkNvbHVtbnMJKQAAAAYqAAAACkpvYnMuSm9iSUQKAdX%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHU%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQwAAAAGAAAACgYuAAAAC1Jvd3NQZXJQYWdlCS4AAAAGLwAAAAIxMAoB0P%2F%2F%2F%2B7%2F%2F%2F8BAAAAAc%2F%2F%2F%2F%2Ft%2F%2F%2F%2FAAAAAAABCRQAAAABDQAAAAYAAAAKBjMAAAAaVXBkYXRlSW1wcmVzc2lvblN0YXRpc3RpY3MJMwAAAAY0AAAABHRydWUKAcv%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHK%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQ4AAAAGAAAACgY4AAAACUh0bWxJbnB1dAk4AAAABjkAAAAACgHG%2F%2F%2F%2F7v%2F%2F%2FwEAAAABxf%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAEPAAAABgAAAAoGPQAAABJSZXNvdXJjZURvY3VtZW50SUQJPQAAAAgIlXq8BgoBwv%2F%2F%2F%2B7%2F%2F%2F8BAAAAAcH%2F%2F%2F%2Ft%2F%2F%2F%2FAAAAAAABCRQAAAALFgJmDxYCHhhWTTgkVGFibGVWaWV3OlBhcmFtZXRlcnMy6wwAAQAAAP%2F%2F%2F%2F8BAAAAAAAAAAwCAAAAUEFsdGFtaXJhLldlYi5VSSwgVmVyc2lvbj0yMDE3LjMuNjcxOC4yNTE2OSwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsBQEAAAAgQWx0YW1pcmEuV2ViLkRhdGEuRGF0YUNvbGxlY3Rpb24CAAAACm1fT3BlcmF0b3ITQ29sbGVjdGlvbkJhc2UrbGlzdAQDHEFsdGFtaXJhLldlYi5VSS5UeXBlT3BlcmF0b3ICAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QCAAAABf3%2F%2F%2F8cQWx0YW1pcmEuV2ViLlVJLlR5cGVPcGVyYXRvcgEAAAAHdmFsdWVfXwAIAgAAAAAAAAAJBAAAAAQEAAAAHFN5c3RlbS5Db2xsZWN0aW9ucy5BcnJheUxpc3QDAAAABl9pdGVtcwVfc2l6ZQhfdmVyc2lvbgUAAAgICQUAAAAKAAAACwAAABAFAAAAEAAAAAkGAAAACQcAAAAJCAAAAAkJAAAACQoAAAAJCwAAAAkMAAAACQ0AAAAJDgAAAAkPAAAADQYFBgAAABxBbHRhbWlyYS5XZWIuRGF0YS5EYXRhT2JqZWN0CgAAAAdtX1RhYmxlC21fRmllbGROYW1lDW1fQ29udHJvbE5hbWUHbV9WYWx1ZQ9tX1ZhbHVlRXh0ZW5kZWQMbV9Db21wYXJpc29uBm1fVHlwZRBtX011bHRpcGxlVmFsdWVzC21fRGF0YUJvdW5kEG1fU3Vic3RpdHV0ZVBpcGUBAQECAgQEAAABK0FsdGFtaXJhLldlYi5EYXRhLkRhdGFPYmplY3QrQ29tcGFyaXNvbkVudW0CAAAAGEFsdGFtaXJhLldlYi5VSS5UeXBlRW51bQIAAAABAQIAAAAKBhAAAAAEbmFtZQkQAAAABhEAAAAaRnJvbnRvZmZpY2U6IExpc3RhIEFubnVuY2kKBe7%2F%2F%2F8rQWx0YW1pcmEuV2ViLkRhdGEuRGF0YU9iamVjdCtDb21wYXJpc29uRW51bQEAAAAHdmFsdWVfXwAIAgAAAAEAAAAF7f%2F%2F%2FxhBbHRhbWlyYS5XZWIuVUkuVHlwZUVudW0BAAAAB3ZhbHVlX18ACAIAAAAAAAAAAAEGFAAAAAclIzEyNCMlAQcAAAAGAAAACgYVAAAADk9yZGVyQnlDb2x1bW5zCRUAAAAGFgAAABdKb2JzLkRhdGVQdWJsaXNoZWQgREVTQwoB6f%2F%2F%2F%2B7%2F%2F%2F8BAAAAAej%2F%2F%2F%2Ft%2F%2F%2F%2FAAAAAAABCRQAAAABCAAAAAYAAAAKBhoAAAAPQ2xpY2NhYmxlQ29sdW1uCRoAAAAGGwAAAApKb2JzLlRpdGxlCgHk%2F%2F%2F%2F7v%2F%2F%2FwEAAAAB4%2F%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAEJAAAABgAAAAoGHwAAAAN1cmwJHwAAAAYgAAAACiUlSk9CVVJMJSUKAd%2F%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHe%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQoAAAAGAAAACgYkAAAAEE5vUmVjb3Jkc01lc3NhZ2UJJAAAAAYlAAAAF05lc3N1biBhbm51bmNpbyB0cm92YXRvCgHa%2F%2F%2F%2F7v%2F%2F%2FwEAAAAB2f%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAELAAAABgAAAAoGKQAAAA1IaWRkZW5Db2x1bW5zCSkAAAAGKgAAAApKb2JzLkpvYklECgHV%2F%2F%2F%2F7v%2F%2F%2FwEAAAAB1P%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAEMAAAABgAAAAoGLgAAAAtSb3dzUGVyUGFnZQkuAAAABi8AAAACMTAKAdD%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHP%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAAAQ0AAAAGAAAACgYzAAAAGlVwZGF0ZUltcHJlc3Npb25TdGF0aXN0aWNzCTMAAAAGNAAAAAR0cnVlCgHL%2F%2F%2F%2F7v%2F%2F%2FwEAAAAByv%2F%2F%2F%2B3%2F%2F%2F8AAAAAAAEJFAAAAAEOAAAABgAAAAoGOAAAAAlIdG1sSW5wdXQJOAAAAAY5AAAAAAoBxv%2F%2F%2F%2B7%2F%2F%2F8BAAAAAcX%2F%2F%2F%2Ft%2F%2F%2F%2FAAAAAAABCRQAAAABDwAAAAYAAAAKBj0AAAASUmVzb3VyY2VEb2N1bWVudElECT0AAAAICJV6vAYKAcL%2F%2F%2F%2Fu%2F%2F%2F%2FAQAAAAHB%2F%2F%2F%2F7f%2F%2F%2FwAAAAAAAQkUAAAACxYCZg9kFgJmD2QWBGYPDxYCHw1oZGQCAQ8PFgIfDWhkZAILD2QWBAIBD2QWAmYPFgYeBXRpdGxlBSNTYWx2YSBxdWVzdGEgcmljZXJjYSBjb21lIEpvYiBBbGVydB4DYWx0BSNTYWx2YSBxdWVzdGEgcmljZXJjYSBjb21lIEpvYiBBbGVydB8KBQdzYXZlam9iZAIDD2QWAmYPFgYfEQUIRmVlZCBSU1MfEgUIRmVlZCBSU1MfCgUJcnNzYnV0dG9uZGQ9Ew4dmnHlDBmLDW6qtwIX2t6HiCnbfgYFjF3InUbdqA%3D%3D&__VIEWSTATEGENERATOR=E50C1FF0&__EVENTVALIDATION=%2FwEdAAwjNFzleperliOmopM8kKZMwuKYtW6mGzz6ovydw%2FUZYYsbM9IQVeez7WJdCPhX7zN8N%2FLxHO9YC%2B5zfDlPMEWfooyk4ayuP8C2gUtpug0zPBelGhBcdABwOXZAA7AKiNHxCJscFpf6jII7kBQc5bPq94nXSZeoqnkrhjsMcyw1mm2kTDqkVS8s05n%2B3t6uJtatLt9dJCpErVycv4BOqqu%2Bai3Vmt5PasdPcc88OHoGJo1EXtxP5Fvnh5XP3I4jjAyn%2FMP6WwyBAHpS8NAUyU3X6F609pbHewS6DDIEc7hkEQ%3D%3D&VMFormRicerca3CurrentViewID=FindView&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24FormSC1HiddenNew=None&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24Fld118015088=&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24Fld111989176Nested1=&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24Fld111989176=&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24Fld111989210Nested1=&VMFormRicerca3%24FindView%24FormRicerca%24FormSC1%24Fld111989210=&VMFormRicerca3%24FindView%24FormRicerca%24SCViewFindHiddenNew=None&VM6CurrentViewID=TableView&ReportGrid116271478=&VM6%24TableView%24SCViewReport%24FormSC2%24FormSC2HiddenNew=None&VM6%24TableView%24SCViewReport%24HdnQueryString=&VM6%24TableView%24SCViewReport%24SCViewReportHiddenNew=None&VM8CurrentViewID=TableView&ReportGrid117465463=&VM8%24TableView%24SCViewReport%24FormSC2%24FormSC2HiddenNew=None&VM8%24TableView%24SCViewReport%24HdnQueryString=&VM8%24TableView%24SCViewReport%24SCViewReportHiddenNew=None&SaveJobAlert=AND%7C&companyid=31391009&VM8%24TableView%24SCViewReport%24ctl03={page}',
        )
    }
     ),
)


def crawl(web):
    
    sl = slavy.slavy()
    sl.start('http://modulogroup.sites.altamiraweb.com')
    sl.metaExtract = True
    sl.extract(xtr_view)

    sl.WR = [web]
    
    if len(web.split("!")) > 1:
        data2 = parse_qs(web.split("!")[1])
        data2["__VIEWSTATE"] = sl.M[0].get("viewstate")
        data2["__VIEWSTATEGENERATOR"] = sl.M[0].get("generator")
        data2["__EVENTVALIDATION"] = sl.M[0].get("validation")
    
    #~ webPersonalizada = web.split("!")[0] + "!" + urlencode(data2)
    #~ sl.start(webPersonalizada)

    #### En caso de hacerlo por requests en vez de slavy
    var1 = requests.post(url=web.split("!")[0], data=data2)
    #~ print var1.text
    sl.WR = [u"virtual:{0}".format(var1.text).encode('utf-8')]

    sl.step(stp)
    sl.WR = ["http://modulogroup.sites.altamiraweb.com{0}".format(y) for y in sl.WR]
    #~ sl.printWR()
    #~ exit(0)

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