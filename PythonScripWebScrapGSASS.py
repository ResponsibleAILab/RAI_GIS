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


# def GetIP():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = fromstring(response.text)
#     proxies = set()
#     for i in parser.xpath('//tbody/tr')[:10]:
#         if i.xpath('.//td[7][contains(text(),"yes")]'):
#             proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#             proxies.add(proxy)
#     return proxies
def GetIP():
    proxies = FreeProxy().get()
    return proxies
    

sleep_time = random.uniform(1, 5)
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

Data = {'a': {}, 's': {}, 'g': {},'ss':{}}

# ---------------------------------------------------------------------------------------------------------- 
# ------------------------------------| Getting Data from the Arix |----------------------------------------
# ---------------------------------------------------------------------------------------------------------- 

def GetResultsArix(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    query_params = {
        'advanced': '',
        'terms-0-operator': 'AND',
        'terms-0-term': search_term,
        'terms-0-field': 'all',  # Update 'title' to 'all' to match the URL
        'terms-1-operator': 'AND',
        'terms-1-term': '',
        'terms-1-field': 'title',
        'classification-physics_archives': 'all',
        'classification-include_cross_list': 'include',
        'date-year': '',
        'date-filter_by': 'date_range',
        'date-from_date': start_date,
        'date-to_date': end_date,
        'date-date_type': 'submitted_date',
        'abstracts': 'show',
        'size': '50',
        'order': '-announced_date_first',
    }
    url = "https://arxiv.org/search/advanced?" + urlencode(query_params, doseq=True)
    proxy_handler = ProxyHandler(proxyy)
    opener = build_opener()
    # opener = build_opener(proxy_handler, HTTPCookieProcessor())
    request = Request(url=url, headers={'User-Agent': user_agent})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find('h1', class_='title is-clearfix')

    if div_results:
        res = re.findall(r"of (\d+) results", div_results.text)
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
    
# ---------------------------------------------------------------------------------------------------------- 
# ------------------------------| Getting Data from the Semantic Scholar |----------------------------------
# ---------------------------------------------------------------------------------------------------------- 

def GetResultsSemanticScholar(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    sch = SemanticScholar()
    sd = start_date
    ed = end_date
    print(sd,ed)
    results = sch.search_paper(search_term,year=f'{sd}-{ed}')
    if results:
        num_results = results.total
        success = True
    else:
        success = False
        num_results = '0'

    return num_results, success
# ---------------------------------------------------------------------------------------------------------- 
# --------------------------------| Getting Data from the ScienceDirect |----------------------------------- 
# ---------------------------------------------------------------------------------------------------------- 
# def GetResultsScienceDirect(search_term, start_date, end_date, proxyy):
#     user_agent = GetRandomUserAgent()

#     query_params = {
#         'term': search_term,
#         'filter': 'years.{}-{}'.format(start_date, end_date),
#     }

#     # Construct the URL
#     url = "https://pubmed.ncbi.nlm.nih.gov/?" + urlencode(query_params, doseq=True)
#     proxy_handler = ProxyHandler(proxyy)
#     opener = build_opener()
#     # opener = build_opener(proxy_handler, HTTPCookieProcessor())
    
#     request = Request(url=url, headers={'User-Agent': user_agent})
#     handler = opener.open(request)
#     html = handler.read()
#     # print(handler.getcode())
#     soup = BeautifulSoup(html, 'html.parser')
#     with open('output.html', 'w', encoding='utf-8') as file:
#         file.write(str(soup))
#     span_results = soup.find("span", {"class": "value"})
#     # print(div_results,'googlre')

#     if span_results:
#         # Use regex to extract the number from the text inside the span
#         res = span_results.text.strip().replace(',', '')
#         # print(res,'ss')
#         if res:
#             num_results = ''.join(res[0])
#             success = True
#         else:
#             num_results = '0'
#             success = False
#     else:
#         success = False
#         num_results = '0'

#     return num_results, success

# ---------------------------------------------------------------------------------------------------------- 
# -----------------------------------| Getting Data from the Google |--------------------------------------- 
# ---------------------------------------------------------------------------------------------------------- 
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

# ---------------------------------------------------------------------------------------------------------- 
# -------------------------------| Getting Data from the Google Scholar |-----------------------------------
# ---------------------------------------------------------------------------------------------------------- 

def GetResultsGoogleScholar(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    query_params = {'q': search_term, 'as_ylo': start_date, 'as_yhi': end_date}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.parse.urlencode(query_params)
    proxy_handler = ProxyHandler(proxyy)
    # opener = build_opener()
    opener = build_opener(proxy_handler, HTTPCookieProcessor())
    request = Request(url=url, headers={'User-Agent': user_agent})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find("div", {"id": "gs_ab_md"})

    if div_results:
        res = re.findall(r'About (\d{1,3}(?:,\d{3})*(?:\.\d+)?) results', div_results.text)
        # print(res,'gs')
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

def plot_data(data, title):
    for category, terms in data.items():
        # print(terms)
        for term, results_dict in terms.items():
            years = []
            results = []
            years.append(term)
            results.append(results_dict)
            plt.plot(years, results, label=f"{category} - {term}")

    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Number of Results')
    plt.legend()
    plt.show()


def get_range_and_plot(search_term, start_date, end_date):
    fp = open("out.csv", 'w')
    fp.write("year,results\n")
    ip = GetIP()
    proxies = {'http': ip, 'https': ip}
    for q in search_term:
        Data['g'][q] = {}
        Data['s'][q] = {}
        Data['a'][q] = {}
        Data['ss'][q] = {}
        years = []
        results = []
        for date in range(start_date, end_date + 1):
            google_num_results, google_success = GetResultsGoogle(q, date, date, proxies)
            Scholar_num_results, Scholar_success = GetResultsGoogleScholar(q, date, date, proxies)
            Arixv_num_results, Arixv_success = GetResultsArix(q, date, date, proxies)
            SDirect_num_results, SDirect_success = GetResultsSemanticScholar(q, date, date, proxies)

            if not google_success and google_success:
                print("Too many requests passed to Google. Try again after some time.")
                break
            if not Scholar_success and Scholar_success:
                print("Too many requests passed to Google Scholar. Try again after some time.")
                break
            if not Arixv_success and Arixv_success:
                print("Too many requests passed to Arix. Try again after some time.")
                break
            if not SDirect_success and SDirect_success:
                print("Too many requests passed to Arix. Try again after some time.")
                break

            google_year_results = "{0},{1}".format(date, google_num_results)
            Scholar_year_results = "{0},{1}".format(date, Scholar_num_results)
            Arixv_year_results = "{0},{1}".format(date, Arixv_num_results)
            SDirect_year_results = "{0},{1}".format(date, SDirect_num_results)
            Data['g'][q][date] = google_num_results
            Data['s'][q][date] = Scholar_num_results
            Data['a'][q][date] = Arixv_num_results
            Data['ss'][q][date] = SDirect_num_results
            # years.append(date)
            # results.append(int(num_results))
            
            
            fp.write(google_year_results + '\n')
            fp.write(Scholar_year_results + '\n')
            fp.write(Arixv_year_results + '\n')
    
            time.sleep(sleep_time)

        plt.plot(years, results, label=q)
    print(Data)
    csv_file_path = 'output.csv'


    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["Category", "Subcategory", "Year", "Value"])

        for category, subcategories in Data.items():
            for subcategory, values in subcategories.items():
                for year, value in values.items():
                    writer.writerow([category, subcategory, year, value])
    # plot_data(Data['g'], 'Google Search Results')
    # plot_data(Data['s'], 'Google Scholar Results')
    # plot_data(Data['a'], 'Arix Results')
    # plot_data(Data['ss'], 'ScienceDirect Results')

    # plt.xlabel('Year')
    # plt.ylabel('Number of Results')
    # plt.legend()
    # plt.show()
    fp.close()

if __name__ == "__main__":
    search_term = ['Responsible AI', 'Responsible GIS','GIS']
    start_date = 2019
    end_date = 2023
    get_range_and_plot(search_term, start_date, end_date)