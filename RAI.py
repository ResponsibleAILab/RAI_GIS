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
    with open('useragents.json', 'r') as file:
        user_agents_data = json.load(file)

    randomize_data = user_agents_data.get('randomize', {})
    browsers_data = user_agents_data.get('browsers', {})

    agent_keys = list(randomize_data.keys())
    random_key = random.choice(agent_keys)
    selected_browser = randomize_data.get(random_key, 'chrome')

    user_agents = browsers_data.get(selected_browser, [])

    return random.choice(user_agents)   

#####################################################################################################
###------------------------------- Get User agent for Requests -----------------------------------###
#####################################################################################################

def GetRandomUserAgent():
    with open('useragents.json', 'r') as file:
        user_agents_data = json.load(file)

    randomize_data = user_agents_data.get('randomize', {})
    browsers_data = user_agents_data.get('browsers', {})

    agent_keys = list(randomize_data.keys())
    random_key = random.choice(agent_keys)
    selected_browser = randomize_data.get(random_key, 'chrome')

    user_agents = browsers_data.get(selected_browser, [])

    return random.choice(user_agents) 
  
Data = {'Arix': {}, 'Google': {},'Google Scholar':{},'Sematic Scholar':{}}

#####################################################################################################
###------------------------------- Getting Data from the Arxiv -----------------------------------####
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


#####################################################################################################
###----------------------------- Getting Data from the Google ------------------------------------###
#####################################################################################################


def GetResultsGoogle(search_term, start_date, end_date):
    total_results = 0
    success_count = 0
    user_agent = GetRandomUser_Agent()
    query_params = {'q': search_term, 'tbs': f'cdr:1,cd_min:{start_date},cd_max:{end_date}', 'tbm': ''}
    url = "https://www.google.com/search?" + urlencode(query_params, doseq=True)
    opener = build_opener()    
    for _ in range(10):
        request = Request(url=url, headers={'User-Agent': user_agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
        handler = opener.open(request)
        html = handler.read()
        soup = BeautifulSoup(html, 'html.parser')
        div_results = soup.find("div", {"id": "result-stats"})

        if not div_results:
            print("No results found.")
            continue

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

    Data = get_results_parallel(search_term, start_date, end_date)

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