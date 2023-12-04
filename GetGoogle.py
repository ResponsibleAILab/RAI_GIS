from bs4 import BeautifulSoup
from urllib.request import Request, build_opener, HTTPCookieProcessor, ProxyHandler
from urllib.parse import urlencode
from requests.exceptions import RequestException
from http.cookiejar import MozillaCookieJar
import re, time, sys, urllib
from fp.fp import FreeProxy
import requests
import random
import matplotlib.pyplot as plt
from lxml.html import fromstring
import csv
from semanticscholar import SemanticScholar

def GetResultsGoogle(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    query_params = {'q': search_term, 'as_ylo': start_date, 'as_yhi': end_date}
    url = "https://www.google.com/search?" + urlencode(query_params, doseq=True)
    proxy_handler = ProxyHandler(proxyy)
    opener = build_opener()
    request = Request(url=url, headers={'User-Agent': user_agent,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find("div", {"id": "result-stats"})
    if not div_results:
        return 0, False

    if div_results:
        res = re.findall(r'(\d[\d,]*)\sresults', div_results.text)
        if res:
            num_results = ''.join(res[0])
            success = True
        else:
            num_results = '0'
            success = True
    else:
        success = False
        num_results = '0'

    return num_results, success