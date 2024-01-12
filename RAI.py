from bs4 import BeautifulSoup
from urllib.request import Request, build_opener, HTTPCookieProcessor, ProxyHandler
from urllib.parse import urlencode
import re, time, urllib
from fp.fp import FreeProxy
import random
import matplotlib.pyplot as plt
import csv
from semanticscholar import SemanticScholar
import pandas as pd
import plotly.graph_objects as go
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import tenacity


#####################################################################################################
###--------------------------------------- To Get IP ---------------------------------------------###
#####################################################################################################

global username
username = "rai_user1"
global password
password = "RaiDummy#123"
global proxy
proxy = "pr.oxylabs.io:7777"

sleep_time = random.uniform(0.6, 2)

#####################################################################################################
###---------------------------- Get User agent for Google search ---------------------------------###
#####################################################################################################

def GetRandomUser_Agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    ]
    return random.choice(user_agents)

#####################################################################################################
###------------------------------- Get User agent for Requests -----------------------------------###
#####################################################################################################

def GetRandomUserAgent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
        'Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/79.0.4143.34',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:91.0) Gecko/20100101 Thunderbird/91.7.0',
    ]
    return random.choice(user_agents)
  
Data = {'Arix': {}, 'Google': {},'Google Scholar':{},'Sematic Scholar':{}}
#####################################################################################################
###------------------------------- Getting Data from the Arix -----------------------------------####
#####################################################################################################

def GetResultsArix(search_term, start_date, end_date):
    user_agent = GetRandomUserAgent()
    query_params = {
        'advanced': '',
        'terms-0-operator': 'AND',
        'terms-0-term': search_term,
        'terms-0-field': 'all',
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
    opener = build_opener()
    request = Request(url=url, headers={'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find('h1', class_='title is-clearfix')
    # print(div_results)

    if div_results:
        res = re.findall(r"of (\d+) results", div_results.text)
        if res:
            num_results = int(''.join(res[0]).replace(',', ''))
            success = True
        else:
            num_results = 0  # Initialize as an integer
            success = True
    else:
        success = False
        num_results = 0  # Initialize as an integer

    return num_results, success
   

#####################################################################################################
###-------------------------- Getting Data from the Semantic Scholar -----------------------------###
#####################################################################################################
def search_paper_with_retry(sch, search_term, start_date):
    return sch.search_paper(search_term, year=start_date)

def GetResultsSemanticScholar(search_term, start_date, end_date):
    sch = SemanticScholar()
    sd = start_date
    ed = end_date

    try:
        results = search_paper_with_retry(sch, search_term, sd)

        if results:
            num_results = results.total
            success = True
        else:
            success = False
            num_results = 0

    except tenacity.RetryError as e:
        print(f"Failed after multiple retries: {e}")
        success = False
        num_results = 0

    return num_results, success

# def GetResultsSemanticScholar(search_term, start_date, end_date):
#     sch = SemanticScholar()
#     sd = start_date
#     ed = end_date
#     results = sch.search_paper(search_term,year=f'{sd}')
#     if results:
#         num_results = results.total
#         success = True
#     else:
#         success = False
#         num_results = '0'
#     return num_results, success

#####################################################################################################
###----------------------------- Getting Data from the Google ------------------------------------###
#####################################################################################################


def GetResultsGoogle(search_term, start_date, end_date):
    total_results = 0
    success_count = 0
    user_agent = GetRandomUser_Agent()
    query_params = {'q': search_term, 'tbs': f'cdr:1,cd_min:{start_date},cd_max:{end_date}', 'tbm': ''}
    url = "https://www.google.com/search?" + urlencode(query_params, doseq=True)
    # proxy_url = 'http://customer-%s-cc-%s:%s@pr.oxylabs.io:7777' % (username, 'US',password)
    # proxies = {'http': proxy_url, 'https': proxy_url}
    # proxy_handler = ProxyHandler(proxies)
    # opener = build_opener(proxy_handler, HTTPCookieProcessor())
    opener = build_opener()    
    # request = Request(url=url, headers={'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    # handler = opener.open(request)
    # html = handler.read()
    # soup = BeautifulSoup(html, 'html.parser')
    # div_results = soup.find("div", {"id": "result-stats"})

    # if not div_results:
    #     print("No results found.")
    #     return total_results, False

    # res = re.findall(r'(\d[\d,]*)\sresults', div_results.text)
    # if res:
    #     num_results = int(''.join(res[0]).replace(',', ''))
    #     total_results += num_results
    #     success_count += 1
    #     success = True
    # else:
    #     print("Unable to extract number of results.")
    #     num_results = 0
    #     success = False

    # sleep_time = random.uniform(0.6, 2)
    # time.sleep(sleep_time)

    # return total_results, success_count
    for _ in range(10):
        request = Request(url=url, headers={'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
        handler = opener.open(request)
        html = handler.read()
        soup = BeautifulSoup(html, 'html.parser')
        div_results = soup.find("div", {"id": "result-stats"})

        if not div_results:
            print("No results found.")
            Continur

        res = re.findall(r'(\d[\d,]*)\sresults', div_results.text)
        if res:
            num_results = int(''.join(res[0]).replace(',', ''))
            print(_ + 1, "-", num_results)
            total_results += num_results
            success_count += 1
            success = True
        else:
            print("Unable to extract number of results.")
            num_results = 0
            success = False

        sleep_time = random.uniform(0.6, 2)
        # print(sleep_time)
        time.sleep(sleep_time)

    return total_results, success_count

#####################################################################################################
###------------------------ Getting Data from the Google Scholar ---------------------------------###
#####################################################################################################

def GetResultsGoogleScholar(search_term, start_date, end_date):
    total_results = 0
    success_count = 0
    user_agent = GetRandomUserAgent()
    query_params = {'q': search_term, 'as_ylo': start_date, 'as_yhi': end_date}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urlencode(query_params)
    proxy_url = 'http://customer-%s-cc-%s:%s@pr.oxylabs.io:7777' % (username, 'US',password)
    proxies = {'http': proxy_url, 'https': proxy_url}
    proxy_handler = ProxyHandler(proxies)
    opener = build_opener(proxy_handler, HTTPCookieProcessor())

    # Make the request
    request = Request(url=url, headers={'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find("div", {"id": "gs_ab_md"})

    if div_results:
        res = re.findall(r'About (\d{1,3}(?:,\d{3})*(?:\.\d+)?) results', div_results.text)
        if res:
            num_results = int(''.join(res[0]).replace(',', ''))
            success = True
        else:
            num_results = 0
            success = True
    else:
        success = False
        num_results = 0
    print(total_results,success_count)
    return num_results, success


#####################################################################################################
###------------------------------------- To plot the Data---- ------------------------------------###
#####################################################################################################

def plot_interactive_graph(data, title):
    labels = list(data.keys())
    years = list(data[labels[0]]['Responsible AI'].keys())

    marker_symbols = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'triangle-down', 'star', 'hexagram', 'pentagon']

    traces = []

    for i, label in enumerate(labels):
        cnt = i  # Move cnt assignment inside the loop to reset it for each label
        for category, values in data[label].items():
            if category:
                cnt = (cnt + 1) % len(marker_symbols)  # Use modulo to cycle through the symbols
            max_value = max(values.values())
            if max_value != 0:
                scaled_values = [value / max_value * 100 for value in values.values()]
            else:
                scaled_values = [0] * len(values)
            trace = go.Scatter(x=years, y=scaled_values, mode='lines+markers', name=f'{category}', marker=dict(symbol=marker_symbols[cnt]))
            traces.append(trace)

    layout = go.Layout(title=title, xaxis=dict(title='Year'), yaxis=dict(title='Percentage of Max Value'))
    fig = go.Figure(data=traces, layout=layout)

    fig.show()



#####################################################################################################
###-------------------------------- Store the Data in the xlsx file ------------------------------###
#####################################################################################################

def save_results_to_csv(data, csv_path):
    grouped_rows = {}
    
    # Iterate through the data and create rows for each source
    for source, queries in data.items():
        for query, results in queries.items():
            for date, num_results in results.items():
                key = (query, date)
                if key not in grouped_rows:
                    grouped_rows[key] = {'Query': query, 'Date': date}
                grouped_rows[key][source] = num_results

    # Write the rows to the CSV file
    with open(csv_path, mode='w', newline='') as csv_file:
        fieldnames = ['Query', 'Date'] + list(data.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in grouped_rows.values():
            writer.writerow(row)

    print(f"Results saved to {csv_path}")

#####################################################################################################
## Main function calls each method iterates each Query between the range
## and Store them in the Excel file also they are ploted in the Trend Graph
#####################################################################################################

def get_range_and_plot(search_term, start_date, end_date):
    fp = open("out.csv", 'w')
    fp.write("year,results\n")
    for q in search_term:
        Data['Google'][q] = {}
        Data['Google Scholar'][q] = {}
        Data['Arix'][q] = {}
        Data['Sematic Scholar'][q] = {}
        years = []
        results = []
        for date in range(start_date, end_date + 1):
            google_num_results, google_success = GetResultsGoogle(q, date, date)
            Scholar_num_results, Scholar_success = GetResultsGoogleScholar(q, date, date)
            Arixv_num_results, Arixv_success = GetResultsArix(q, date, date)
            SDirect_num_results, SDirect_success = GetResultsSemanticScholar(q, date, date)
            if not google_success and google_success:
                print("Too many requests passed to Google. Try again after some time.")
                google_year_results = "{0},{1}".format(date, google_num_results)
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
            print(q)
            print(google_year_results)
            print(Scholar_year_results)
            print(Arixv_year_results)
            print(SDirect_year_results)
            Data['Google'][q][date] = google_num_results
            Data['Google Scholar'][q][date] = Scholar_num_results
            Data['Arix'][q][date] = Arixv_num_results
            Data['Sematic Scholar'][q][date] = SDirect_num_results            
            fp.write(google_year_results + '\n')
            fp.write(Scholar_year_results + '\n')
            fp.write(Arixv_year_results + '\n')
            fp.write(SDirect_year_results + '\n')
            time.sleep(sleep_time)
        plt.plot(years, results, label=q)
    
    print(Data)
    # list_years = list(Data['Arix']['Responsible AI'].keys())
    csv_file_path = 'output.csv'
    save_results_to_csv(Data, csv_file_path)
    fp.close()



def get_results_parallel(search_term, start_date, end_date, max_workers=8):
    results = []
    formatted_results = {source: {q: {date: 0 for date in range(start_date, end_date + 1)} for q in search_term} for source in ["Google", "Google Scholar", "Arix", "Semantic Scholar"]}

    def update_results(q, date, source, num_results, success):
        results.append((q, date, source, num_results, success))
        formatted_results[source][q][date] += num_results  # Update the count

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_query = {
            executor.submit(GetResultsGoogle, q, date, date): (q, date, "Google")
            for q in search_term for date in range(start_date, end_date + 1)
        }
        future_to_query.update({
            executor.submit(GetResultsGoogleScholar, q, date, date): (q, date, "Google Scholar")
            for q in search_term for date in range(start_date, end_date + 1)
        })
        future_to_query.update({
            executor.submit(GetResultsArix, q, date, date): (q, date, "Arix")
            for q in search_term for date in range(start_date, end_date + 1)
        })
        future_to_query.update({
            executor.submit(GetResultsSemanticScholar, q, date, date): (q, date, "Semantic Scholar")
            for q in search_term for date in range(start_date, end_date + 1)
        })

        for future in as_completed(future_to_query):
            q, date, source = future_to_query[future]
            try:
                num_results, success = future.result()
                update_results(q, date, source, num_results, success)
            except Exception as e:
                print(f"Exception for {q} - {date} - {source}: {e}")

    # Process the results as needed
    for q, date, source, num_results, success in results:
        if not success:
            print(f"Failed to get results for {q} - {date} - {source}")

    # Save results to CSV
    csv_file_path = 'output.csv'
    save_results_to_csv(results, csv_file_path)
    print(formatted_results)

    return formatted_results

if __name__ == "__main__":
    start_time = time.time()
    search_term = ['Responsible AI','RAI','Ethical AI','AI Governance','AI Accountability','AI Privacy', 'Responsible Geographic Information Systems','Geographic Information Systems','Spatial Analysis','Cartography','GIS Mapping','Fair GIS Applications']
    start_date = 2013
    end_date = 2023

    # Data = get_range_and_plot(search_term, start_date, end_date)
    # Data = get_results_parallel(search_term, start_date, end_date)
    Data = {'Arix': {'Responsible AI': {2013: 5, 2014: 5, 2015: 2, 2016: 9, 2017: 18, 2018: 24, 2019: 55, 2020: 128, 2021: 180, 2022: 189, 2023: 664}, 'RAI': {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0}, 'Ethical AI': {2013: 0, 2014: 1, 2015: 2, 2016: 4, 2017: 12, 2018: 21, 2019: 54, 2020: 100, 2021: 154, 2022: 160, 2023: 413}, 'AI Governance': {2013: 0, 2014: 2, 2015: 4, 2016: 6, 2017: 3, 2018: 19, 2019: 23, 2020: 56, 2021: 95, 2022: 99, 2023: 174}, 'AI Accountability': {2013: 7, 2014: 1, 2015: 5, 2016: 2, 2017: 7, 2018: 13, 2019: 43, 2020: 61, 2021: 92, 2022: 130, 2023: 238}, 'AI Privacy': {2013: 0, 2014: 1, 2015: 1, 2016: 0, 2017: 5, 2018: 16, 2019: 42, 2020: 73, 2021: 104, 2022: 144, 2023: 362}, 'Responsible Geographic Information Systems': {2013: 1, 2014: 1, 2015: 1, 2016: 0, 2017: 2, 2018: 0, 2019: 0, 2020: 4, 2021: 5, 2022: 2, 2023: 9}, 'Geographic Information Systems': {2013: 25, 2014: 27, 2015: 38, 2016: 32, 2017: 34, 2018: 39, 2019: 64, 2020: 64, 2021: 66, 2022: 81, 2023: 100}, 'Spatial Analysis': {2013: 763, 2014: 830, 2015: 992, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0}, 'Cartography': {2013: 6, 2014: 4, 2015: 11, 2016: 10, 2017: 7, 2018: 12, 2019: 19, 2020: 22, 2021: 16, 2022: 27, 2023: 21}, 'GIS Mapping': {2013: 6, 2014: 10, 2015: 7, 2016: 9, 2017: 10, 2018: 9, 2019: 14, 2020: 14, 2021: 12, 2022: 9, 2023: 13}, 'Fair GIS Applications': {2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0}},
          'Google': {'Responsible AI': {2013: 7570000, 2014: 11300000, 2015: 25900000, 2016: 38800000, 2017: 32500000, 2018: 80800000, 2019: 86100000, 2020: 106000000, 2021: 78000000, 2022: 113000000, 2023: 418000000}, 'RAI': {2013: 10100000, 2014: 12600000, 2015: 17600000, 2016: 24700000, 2017: 35300000, 2018: 35500000, 2019: 43000000, 2020: 78700000, 2021: 78000000, 2022: 77100000, 2023: 240000000}, 'Ethical AI': {2013: 188000, 2014: 1870000, 2015: 3020000, 2016: 3560000, 2017: 6440000, 2018: 11000000, 2019: 22300000, 2020: 39100000, 2021: 30400000, 2022: 35900000, 2023: 74800000}, 'AI Governance': {2013: 3200000, 2014: 5490000, 2015: 7220000, 2016: 6760000, 2017: 13200000, 2018: 16700000, 2019: 31600000, 2020: 34000000, 2021: 54800000, 2022: 82600000, 2023: 160000000}, 'AI Accountability': {2013: 63000, 2014: 118000, 2015: 219000, 2016: 227000, 2017: 196000, 2018: 324000, 2019: 1550000, 2020: 5100000, 2021: 5540000, 2022: 8520000, 2023: 19200000}, 'AI Privacy': {2013: 95500000, 2014: 205000000, 2015: 293000000, 2016: 199000000, 2017: 341000000, 2018: 562000000, 2019: 448000000, 2020: 619000000, 2021: 643000000, 2022: 1020000000, 2023: 2640000000}, 'Responsible Geographic Information Systems': {2013: 417000, 2014: 394000, 2015: 8350000, 2016: 12100000, 2017: 12900000, 2018: 27900000, 2019: 30900000, 2020: 38700000, 2021: 40800000, 2022: 48700000, 2023: 42500000}, 'Geographic Information Systems': {2013: 1850000, 2014: 3650000, 2015: 8650000, 2016: 8270000, 2017: 15700000, 2018: 17000000, 2019: 28300000, 2020: 32700000, 2021: 26500000, 2022: 26700000, 2023: 61400000}, 'Spatial Analysis': {2013: 4570000, 2014: 5860000, 2015: 13800000, 2016: 16600000, 2017: 19200000, 2018: 31600000, 2019: 64800000, 2020: 65700000, 2021: 54400000, 2022: 59500000, 2023: 67400000}, 'Cartography': {2013: 1800000, 2014: 1840000, 2015: 2170000, 2016: 2590000, 2017: 3650000, 2018: 4580000, 2019: 6050000, 2020: 7110000, 2021: 6570000, 2022: 6260000, 2023: 9530000}, 'GIS Mapping': {2013: 3190000, 2014: 4070000, 2015: 6740000, 2016: 22000000, 2017: 11400000, 2018: 18600000, 2019: 21200000, 2020: 24600000, 2021: 20700000, 2022: 32800000, 2023: 43000000}, 'Fair GIS Applications': {2013: 27200, 2014: 25600, 2015: 32800, 2016: 55000, 2017: 62200, 2018: 71300, 2019: 103000, 2020: 133000, 2021: 96200, 2022: 163000, 2023: 379000}}, 
  'Google Scholar': {'Responsible AI': {2013: 256000, 2014: 220000, 2015: 231000, 2016: 211000, 2017: 231000, 2018: 221000, 2019: 216000, 2020: 200000, 2021: 153000, 2022: 127000, 2023: 110000}, 'RAI': {2013: 76900, 2014: 83000, 2015: 89700, 2016: 95500, 2017: 103000, 2018: 108000, 2019: 110000, 2020: 114000, 2021: 99400, 2022: 77300, 2023: 64400}, 'Ethical AI': {2013: 125000, 2014: 117000, 2015: 141000, 2016: 151000, 2017: 161000, 2018: 165000, 2019: 167000, 2020: 168000, 2021: 152000, 2022: 99800, 2023: 119000}, 'AI Governance': {2013: 58100, 2014: 60400, 2015: 65000, 2016: 65800, 2017: 80000, 2018: 89100, 2019: 96000, 2020: 102000, 2021: 97400, 2022: 73200, 2023: 77700}, 'AI Accountability': {2013: 20900, 2014: 21900, 2015: 23300, 2016: 23400, 2017: 29000, 2018: 36000, 2019: 43500, 2020: 53300, 2021: 57700, 2022: 47300, 2023: 38800}, 'AI Privacy': {2013: 356000, 2014: 343000, 2015: 330000, 2016: 336000, 2017: 333000, 2018: 347000, 2019: 339000, 2020: 328000, 2021: 243000, 2022: 151000, 2023: 203000}, 'Responsible Geographic Information Systems': {2013: 143000, 2014: 134000, 2015: 23700, 2016: 136000, 2017: 133000, 2018: 36000, 2019: 125000, 2020: 119000, 2021: 108000, 2022: 83200, 2023: 70900}, 'Geographic Information Systems': {2013: 461000, 2014: 472000, 2015: 466000, 2016: 469000, 2017: 440000, 2018: 418000, 2019: 364000, 2020: 341000, 2021: 232000, 2022: 181000, 2023: 138000}, 'Spatial Analysis': {2013: 2350000, 2014: 2280000, 2015: 2260000, 2016: 2080000, 2017: 1790000, 2018: 1840000, 2019: 1570000, 2020: 1240000, 2021: 771000, 2022: 371000, 2023: 237000}, 'Cartography': {2013: 28700, 2014: 30400, 2015: 32800, 2016: 35700, 2017: 29300, 2018: 37200, 2019: 36700, 2020: 39400, 2021: 36400, 2022: 30700, 2023: 25100}, 'GIS Mapping': {2013: 57200, 2014: 62700, 2015: 64600, 2016: 68900, 2017: 71800, 2018: 68600, 2019: 75700, 2020: 72200, 2021: 73600, 2022: 61700, 2023: 46800}, 'Fair GIS Applications': {2013: 7370, 2014: 7480, 2015: 7960, 2016: 8140, 2017: 8400, 2018: 8930, 2019: 9390, 2020: 10600, 2021: 12200, 2022: 10700, 2023: 8970}}, 
 'Sematic Scholar': {'Responsible AI': {2013: 62327, 2014: 65620, 2015: 66987, 2016: 67872, 2017: 67632, 2018: 73010, 2019: 79200, 2020: 87421, 2021: 83562, 2022: 77942, 2023: 85701}, 'RAI': {2013: 1000, 2014: 1000, 2015: 1167, 2016: 1180, 2017: 1289, 2018: 1237, 2019: 1195, 2020: 1304, 2021: 1155, 2022: 1042, 2023: 1057}, 'Ethical AI': {2013: 30581, 2014: 32003, 2015: 33461, 2016: 34397, 2017: 35647, 2018: 40457, 2019: 47075, 2020: 55518, 2021: 55381, 2022: 52528, 2023: 62307}, 'AI Governance': {2013: 35980, 2014: 38032, 2015: 39740, 2016: 40062, 2017: 40883, 2018: 47276, 2019: 52362, 2020: 57915, 2021: 57806, 2022: 55110, 2023: 64654}, 'AI Accountability': {2013: 18979, 2014: 19638, 2015: 20254, 2016: 21343, 2017: 22038, 2018: 26173, 2019: 31343, 2020: 36974, 2021: 38743, 2022: 39221, 2023: 49885}, 'AI Privacy': {2013: 22348, 2014: 24412, 2015: 25192, 2016: 26410, 2017: 28301, 2018: 32851, 2019: 38807, 2020: 46387, 2021: 49014, 2022: 50672, 2023: 61775}, 'Responsible Geographic Information Systems': {2013: 9138, 2014: 9196, 2015: 9432, 2016: 8923, 2017: 8575, 2018: 8891, 2019: 8860, 2020: 9006, 2021: 8200, 2022: 6757, 2023: 6015}, 'Geographic Information Systems': {2013: 133223, 2014: 135395, 2015: 134020, 2016: 125569, 2017: 125639, 2018: 130946, 2019: 135014, 2020: 138492, 2021: 130796, 2022: 115222, 2023: 100614}, 'Spatial Analysis': {2013: 964205, 2014: 1003674, 2015: 1011110, 2016: 996857, 2017: 1014438, 2018: 1091182, 2019: 1124847, 2020: 1228434, 2021: 1179453, 2022: 1079683, 2023: 1006700}, 'Cartography': {2013: 2379, 2014: 2471, 2015: 2703, 2016: 2628, 2017: 2790, 2018: 2868, 2019: 3025, 2020: 2913, 2021: 2637, 2022: 1874, 2023: 1646}, 'GIS Mapping': {2013: 55829, 2014: 57273, 2015: 58063, 2016: 56833, 2017: 57350, 2018: 60293, 2019: 60863, 2020: 63189, 2021: 59581, 2022: 53790, 2023: 49933}, 'Fair GIS Applications': {2013: 4030, 2014: 3895, 2015: 3851, 2016: 3552, 2017: 3450, 2018: 3596, 2019: 3890, 2020: 3959, 2021: 3847, 2022: 3483, 2023: 3170}}}
    # csv_file_path = 'output.csv'
    # save_results_to_csv(Data, csv_file_path)

    Tempdata = Data['Google']
    plot_interactive_graph({'Google':Tempdata}, 'Google Search Results')
    Tempdata = Data['Google Scholar']
    plot_interactive_graph({'Google Scholar':Tempdata}, 'Google Scholar Results')
    Tempdata = Data['Arix']
    plot_interactive_graph({'Arix':Tempdata}, 'Arxiv Results')
    Tempdata = Data['Sematic Scholar']
    plot_interactive_graph({'Sematic Scholar':Tempdata}, 'Sematic Scholar Results')
    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total execution time: {total_time} seconds")