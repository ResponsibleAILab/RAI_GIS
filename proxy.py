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

def GetIP():
    proxy = FreeProxy().get()
    return proxy

def GetRandomUserAgent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/79.0.4143.34',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:91.0) Gecko/20100101 Thunderbird/91.7.0',
    ]

    return random.choice(user_agents)

Data = {}

def GetNumResult(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    query_params = {'q': search_term, 'as_ylo': start_date, 'as_yhi': end_date}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.parse.urlencode(query_params)
    proxy_handler = ProxyHandler(proxyy)
    opener = build_opener(proxy_handler, HTTPCookieProcessor())
    request = Request(url=url, headers={'User-Agent': user_agent})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find("div", {"id": "gs_ab_md"})

    if div_results:
        res = re.findall(r'(\d+).?(\d+)?.?(\d+)?\s', div_results.text)
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

def get_range_and_plot(search_term, start_date, end_date):
    fp = open("out.csv", 'w')
    fp.write("year,results\n")
    print("year,results")
    ip = GetIP()
    proxies = {'http': ip, 'https': ip}

    for q in search_term:
        Data[q] = {}
        years = []
        results = []

        for date in range(start_date, end_date + 1):
            num_results, success = GetNumResult(q, date, date, proxies)
            
            if not success:
                print("Too many requests passed to Google Scholar. Try again after some time.")
                break
            
            year_results = "{0},{1}".format(date, num_results)
            print(year_results)
            Data[q][date] = num_results

            years.append(date)
            results.append(int(num_results))

            print(year_results)
            fp.write(year_results + '\n')
            time.sleep(0.8)

        plt.plot(years, results, label=q)
    print(Data)
    plt.xlabel('Year')
    plt.ylabel('Number of Results')
    plt.legend()
    plt.show()
    fp.close()

if __name__ == "__main__":
    search_term = ['Responsible AI', 'Machine Learning']
    start_date = 2021
    end_date = 2023
    get_range_and_plot(search_term, start_date, end_date)