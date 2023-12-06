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


#####################################################################################################
###--------------------------------------- To Get IP ---------------------------------------------###
#####################################################################################################

def GetIP():
    proxies = FreeProxy().get()
    return proxies

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
# Data = {'Arix': {}, 'Google': {},'Sematic Scholar':{}}
# Data = {'Arix': {}, 'Google': {},'Google Scholar':{}}

#####################################################################################################
###------------------------------- Getting Data from the Arix -----------------------------------###
#####################################################################################################

def GetResultsArix(search_term, start_date, end_date, proxyy):
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
    proxy_handler = ProxyHandler(proxyy)
    opener = build_opener()
    # opener = build_opener(proxy_handler, HTTPCookieProcessor())
    request = Request(url=url, headers={'User-Agent': user_agent})
    handler = opener.open(request)
    html = handler.read()
    soup = BeautifulSoup(html, 'html.parser')
    div_results = soup.find('h1', class_='title is-clearfix')
    # print(div_results)

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
    
#####################################################################################################
###-------------------------- Getting Data from the Semantic Scholar -----------------------------###
#####################################################################################################

def GetResultsSemanticScholar(search_term, start_date, end_date, proxyy):
    sch = SemanticScholar()
    sd = start_date
    ed = end_date
    # print(sd,ed)
    results = sch.search_paper(search_term,year=f'{sd}-{ed}')
    if results:
        num_results = str(results.total)
        success = True
    else:
        success = False
        num_results = '0'
    # print(num_results)
    return num_results, success

#####################################################################################################
###----------------------------- Getting Data from the Google ------------------------------------###
#####################################################################################################
 
def GetResultsGoogle(search_term, start_date, end_date, proxyy):
     user_agent = GetRandomUser_Agent()
     query_params = {'q': search_term, 'tbs': f'cdr:1,cd_min:{start_date},cd_max:{end_date}', 'tbm': ''}
     url = "https://www.google.com/search?" + urlencode(query_params, doseq=True)
    #  print(url)
     opener = build_opener()
     request = Request(url=url, headers={'User-Agent': user_agent,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"})
     handler = opener.open(request)
     html = handler.read()
     soup = BeautifulSoup(html, 'html.parser')
     div_results = soup.find("div", {"id": "result-stats"})
    #  print(div_results)
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

#####################################################################################################
###------------------------ Getting Data from the Google Scholar ---------------------------------###
#####################################################################################################

def GetResultsGoogleScholar(search_term, start_date, end_date, proxyy):
    user_agent = GetRandomUserAgent()
    query_params = {'q': search_term, 'as_ylo': start_date, 'as_yhi': end_date}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.parse.urlencode(query_params)
    proxy_handler = ProxyHandler(proxyy)
    opener = build_opener()
    # opener = build_opener(proxy_handler, HTTPCookieProcessor())
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

#####################################################################################################
###------------------------------------- To plot the Data---- ------------------------------------###
#####################################################################################################

def plot_trend_chart(data, chart_title):
    # Convert data to a format suitable for plotting
    plot_data = []
    for source, terms in data.items():
        for term, values in terms.items():
            for year, value in values.items():
                try:
                    plot_data.append({'Source': source, 'Term': term, 'Year': int(year), 'Value': int(value.replace(',', ''))})
                except ValueError:
                    # Handle cases where the value is not a valid integer
                    pass

    # Create a DataFrame
    df = pd.DataFrame(plot_data)

    # Create traces for each category
    traces = []
    for term in df['Term'].unique():
        term_data = df[df['Term'] == term]
        for source in term_data['Source'].unique():
            source_data = term_data[term_data['Source'] == source]
            trace = go.Scatter(x=source_data['Year'], y=source_data['Value'], mode='lines+markers', name=f'{source} - {term}')
            traces.append(trace)

    # Create layout
    layout = go.Layout(title=chart_title, xaxis=dict(title='Year'), yaxis=dict(title='Value'))

    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    # Show interactive graph
    fig.show()



#####################################################################################################
###-------------------------------- Store the Data in the xlsx file ------------------------------###
#####################################################################################################

def save_to_excel(data, excel_path):
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['Query', 'Date', 'Source', 'Num_Results', 'Success']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for q, date, source, num_results, success in results:
            writer.writerow({'Query': q, 'Date': date, 'Source': source, 'Num_Results': num_results, 'Success': success})

    print(f"Results saved to {csv_file_path}")

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
            google_num_results, google_success = GetResultsGoogle(q, date, date, proxies)
            Scholar_num_results, Scholar_success = GetResultsGoogleScholar(q, date, date, proxies)
            Arixv_num_results, Arixv_success = GetResultsArix(q, date, date, proxies)
            SDirect_num_results, SDirect_success = GetResultsSemanticScholar(q, date, date, proxies)
            if not google_success and google_success:
                print("Too many requests passed to Google. Try again after some time.")
                print(Data)
                break
            if not Scholar_success and Scholar_success:
                print("Too many requests passed to Google Scholar. Try again after some time.")
                print(Data)
                break
            if not Arixv_success and Arixv_success:
                print("Too many requests passed to Arix. Try again after some time.")
                print(Data)
                break
            if not SDirect_success and SDirect_success:
                print("Too many requests passed to Arix. Try again after some time.")
                print(Data)
                break
            google_year_results = "{0},{1}".format(date, google_num_results)
            Scholar_year_results = "{0},{1}".format(date, Scholar_num_results)
            Arixv_year_results = "{0},{1}".format(date, Arixv_num_results)
            SDirect_year_results = "{0},{1}".format(date, SDirect_num_results)
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
    
    # Data = {'Arix': {'Responsible AI': {2013: '5', 2014: '5', 2015: '2', 2016: '9', 2017: '18', 2018: '24', 2019: '55', 2020: '128', 2021: '180', 2022: '189', 2023: '613'}, 'RAI': {2013: '0', 2014: '0', 2015: '0', 2016: '0', 2017: '0', 2018: '0', 2019: '0', 2020: '0', 2021: '0', 2022: '0', 2023: '0'}, 'Ethical AI': {2013: '0', 2014: '1', 2015: '2', 2016: '4', 2017: '12', 2018: '21', 2019: '54', 2020: '100', 2021: '154', 2022: '160', 2023: '378'}, 'AI Governance': {2013: '0', 2014: '2', 2015: '4', 2016: '6', 2017: '3', 2018: '19', 2019: '23', 2020: '56', 2021: '95', 2022: '99', 2023: '161'}, 'AI Accountability': {2013: '7', 2014: '1', 2015: '5', 2016: '2', 2017: '7', 2018: '13', 2019: '43', 2020: '61', 2021: '92', 2022: '130', 2023: '222'}, 'AI Privacy': {2013: '0', 2014: '1', 2015: '1', 2016: '0', 2017: '5', 2018: '16', 2019: '42', 2020: '73', 2021: '104', 2022: '145', 2023: '331'}, 'Responsible Geographic Information Systems': {2013: '1', 2014: '1', 2015: '1', 2016: '0', 2017: '2', 2018: '0', 2019: '0', 2020: '4', 2021: '5', 2022: '2', 2023: '8'}, 'Geographic Information Systems': {2013: '25', 2014: '27', 2015: '38', 2016: '32', 2017: '34', 2018: '39', 2019: '64', 2020: '64', 2021: '66', 2022: '81', 2023: '95'}, 'Spatial Analysis': {2013: '763', 2014: '830', 2015: '992', 2016: '0', 2017: '0', 2018: '0', 2019: '0', 2020: '0', 2021: '0', 2022: '0', 2023: '0'}, 'Cartography': {2013: '6', 2014: '4', 2015: '11', 2016: '10', 2017: '7', 2018: '12', 2019: '19', 2020: '23', 2021: '16', 2022: '27', 2023: '19'}, 'GIS Mapping': {2013: '6', 2014: '10', 2015: '7', 2016: '9', 2017: '10', 2018: '9', 2019: '14', 2020: '14', 2021: '12', 2022: '9', 2023: '12'}, 'GIS Privacy': {2013: '0', 2014: '0', 2015: '0', 2016: '0', 2017: '0', 2018: '0', 2019: '1', 2020: '0', 2021: '1', 2022: '0', 2023: '3'}, 'Fair GIS Applications': {2013: '0', 2014: '0', 2015: '0', 2016: '0', 2017: '0', 2018: '0', 2019: '0', 2020: '0', 2021: '0', 2022: '0', 2023: '0'}, 'GIS Impact Assessment': {2013: '0', 2014: '0', 2015: '1', 2016: '1', 2017: '1', 2018: '1', 2019: '2', 2020: '3', 2021: '2', 2022: '1', 2023: '1'}, 'Responsible Geospatial Technology': {2013: '0', 2014: '0', 2015: '0', 2016: '0', 2017: '0', 2018: '0', 2019: '0', 2020: '2', 2021: '0', 2022: '1', 2023: '2'}, 'Ethical Cartography': {2013: '0', 2014: '0', 2015: '0', 2016: '0', 2017: '0', 2018: '0', 2019: '0', 2020: '0', 2021: '0', 2022: '0', 2023: '1'}}, 'Google': {'Responsible AI': {2013: '9,420,000', 2014: '11,700,000', 2015: '24,900,000', 2016: '39,900,000', 2017: '51,400,000', 2018: '72,200,000', 2019: '89,300,000', 2020: '85,700,000', 2021: '97,700,000', 2022: '149,000,000', 2023: '354,000,000'}, 'RAI': {2013: '10,400,000', 2014: '18,500,000', 2015: '22,300,000', 2016: '17,600,000', 2017: '26,300,000', 2018: '54,300,000', 2019: '60,700,000', 2020: '80,000,000', 2021: '90,500,000', 2022: '118,000,000', 2023: '217,000,000'}, 'Ethical AI': {2013: '11,400,000', 2014: '14,400,000', 2015: '17,500,000', 2016: '29,200,000', 2017: '30,000,000', 2018: '56,100,000', 2019: '90,500,000', 2020: '123,000,000', 2021: '135,000,000', 2022: '214,000,000', 2023: '317,000,000'}, 'AI Governance': {2013: '2,350,000', 2014: '5,960,000', 2015: '6,100,000', 2016: '9,150,000', 2017: '15,800,000', 2018: '18,400,000', 2019: '37,400,000', 2020: '54,300,000', 2021: '57,400,000', 2022: '70,100,000', 2023: '164,000,000'}, 'AI Accountability': {2013: '85,200', 2014: '123,000', 2015: '188,000', 2016: '186,000', 2017: '219,000', 2018: '325,000', 2019: '3,060,000', 2020: '5,020,000', 2021: '7,530,000', 2022: '11,500,000', 2023: '16,200,000'}, 'AI Privacy': {2013: '122,000,000', 2014: '176,000,000', 2015: '300,000,000', 2016: '314,000,000', 2017: '436,000,000', 2018: '520,000,000', 2019: '562,000,000', 2020: '805,000,000', 2021: '658,000,000', 2022: '926,000,000', 2023: '2,350,000,000'}, 'Responsible Geographic Information Systems': {2013: '296,000', 2014: '360,000', 2015: '9,830,000', 2016: '10,200,000', 2017: '11,700,000', 2018: '21,500,000', 2019: '40,900,000', 2020: '58,000,000', 2021: '32,500,000', 2022: '39,100,000', 2023: '41,800,000'}, 'Geographic Information Systems': {2013: '2,520,000', 2014: '4,330,000', 2015: '7,230,000', 2016: '14,000,000', 2017: '12,900,000', 2018: '26,800,000', 2019: '44,400,000', 2020: '36,400,000', 2021: '31,800,000', 2022: '42,300,000', 2023: '73,100,000'}, 'Spatial Analysis': {2013: '5,920,000', 2014: '6,520,000', 2015: '10,800,000', 2016: '18,700,000', 2017: '27,600,000', 2018: '46,400,000', 2019: '105,000,000', 2020: '73,100,000', 2021: '68,100,000', 2022: '65,100,000', 2023: '70,000,000'}, 'Cartography': {2013: '2,260,000', 2014: '2,270,000', 2015: '2,680,000', 2016: '5,250,000', 2017: '3,990,000', 2018: '6,370,000', 2019: '8,230,000', 2020: '7,200,000', 2021: '6,460,000', 2022: '7,510,000', 2023: '7,960'}, 'GIS Mapping': {2013: '3,350,000', 2014: '3,480,000', 2015: '10,200,000', 2016: '10,100,000', 2017: '14,100,000', 2018: '27,400,000', 2019: '22,100,000', 2020: '27,000,000', 2021: '29,000,000', 2022: '34,400,000', 2023: '57,200,000'}, 'GIS Privacy': {2013: '149,000', 2014: '272,000', 2015: '310,000', 2016: '404,000', 2017: '428,000', 2018: '7,550,000', 2019: '11,500,000', 2020: '10,700,000', 2021: '13,700,000', 2022: '15,300,000', 2023: '19,500,000'}, 'Fair GIS Applications': {2013: '28,700', 2014: '29,900', 2015: '45,400', 2016: '44,300', 2017: '57,000', 2018: '74,100', 2019: '96,600', 2020: '148,000', 2021: '119,000', 2022: '160,000', 2023: '4,420,000'}, 'GIS Impact Assessment': {2013: '40,700', 2014: '42,800', 2015: '49,400', 2016: '72,000', 2017: '78,200', 2018: '164,000', 2019: '277,000', 2020: '220,000', 2021: '7,850,000', 2022: '6,620,000', 2023: '6,090,000'}, 'Responsible Geospatial Technology': {2013: '17,300', 2014: '14,600', 2015: '22,200', 2016: '22,200', 2017: '32,200', 2018: '45,300', 2019: '67,300', 2020: '96,200', 2021: '129,000', 2022: '137,000', 2023: '384,000'}, 'Ethical Cartography': {2013: '3,890', 2014: '3,390', 2015: '5,070', 2016: '4,290', 2017: '6,050', 2018: '8,760', 2019: '16,000', 2020: '13,400', 2021: '14,300', 2022: '15,600', 2023: '106,000'}}, 'Sematic Scholar': {'Responsible AI': {2013: '62387', 2014: '65669', 2015: '67049', 2016: '67928', 2017: '67626', 2018: '73024', 2019: '79157', 2020: '87422', 2021: '83520', 2022: '77652', 2023: '77469'}, 'RAI': {2013: '1000', 2014: '1000', 2015: '1167', 2016: '1176', 2017: '1287', 2018: '1238', 2019: '1191', 2020: '1305', 2021: '1153', 2022: '1035', 2023: '1000'}, 'Ethical AI': {2013: '30606', 2014: '32042', 2015: '33468', 2016: '34418', 2017: '35635', 2018: '40434', 2019: '46957', 2020: '55458', 2021: '55319', 2022: '52260', 2023: '55617'}, 'AI Governance': {2013: '36025', 2014: '38035', 2015: '39753', 2016: '40106', 2017: '40834', 2018: '47281', 2019: '52290', 2020: '57910', 2021: '57766', 2022: '54870', 2023: '57829'}, 'AI Accountability': {2013: '19000', 2014: '19646', 2015: '20253', 2016: '21354', 2017: '22027', 2018: '26155', 2019: '31304', 2020: '36966', 2021: '38708', 2022: '39019', 2023: '44518'}, 'AI Privacy': {2013: '22246', 2014: '24347', 2015: '25204', 2016: '26286', 216: '8920', 2017: '8559', 2018: '8898', 2019: '8870', 2020: '8999', 2021: '8194', 2022: '6732', 2023: '5454'}, 'Geographic Information Systems': {2013: '133077', 2014: '135248', 2015: '134028', 2016: '125611', 2017: '124912', 2018: '130914', 2019: '134926', 2020: '138425', 2021: '130658', 2022: '114875', 2023: '91284'}, 'Spatial Analysis': {2013: '964901', 2014: '1004498', 2015: '1011844', 2016: '997534', 2017: '1014689', 2018: '1091323', 2019: '1124241', 2020: '1228050', 2021: '1178395', 2022: '1076757', 2023: '913233'}, 'Cartography': {2013: '2381', 2014: '2476', 2015: '2701', 2016: '2626', 2017: '2789', 2018: '2863', 2019: '3019', 2020: '2913', 2021: '2635', 2022: '1860', 2023: '1476'}, 'GIS Mapping': {2013: '55883', 2014: '57294', 2015: '58124', 2016: '56855', 2017: '57387', 2018: '60278', 2019: '60840', 2020: '63206', 2021: '59554', 2022: '53697', 2023: '45502'}, 'GIS Privacy': {2013: '25749', 2014: '27843', 2015: '28345', 2016: '27523', 2017: '27758', 2018: '29228', 2019: '29970', 2020: '32172', 2021: '30443', 2022: '28217', 2023: '25711'}, 'Fair GIS Applications': {2013: '4030', 2014: '3895', 2015: '3853', 2016: '3560', 2017: '3450', 2018: '3592', 2019: '3894', 2020: '3963', 2021: '3842', 2022: '3469', 2023: '2881'}, 'GIS Impact Assessment': {2013: '24525', 2014: '26503', 2015: '28345', 2016: '28909', 2017: '29373', 2018: '32650', 2019: '33990', 2020: '39430', 2021: '39492', 2022: '35434', 2023: '32039'}, 'Responsible Geospatial Technology': {2013: '3607', 2014: '3778', 2015: '4056', 2016: '4061', 2017: '4077', 2018: '4356', 2019: '4643', 2020: '4603', 2021: '4226', 2022: '3821', 2023: '3543'}, 'Ethical Cartography': {2013: '24371', 2014: '25866', 2015: '27236', 2016: '27407', 2017: '27891', 2018: '29465', 2019: '31259', 2020: '34321', 2021: '30503', 2022: '24585', 2023: '21792'}}}
    print(Data)
    list_years = list(Data['Arix']['Responsible AI'].keys())
    csv_file_path = 'output.csv'


    excel_path = 'trends_data.xlsx'
    save_to_excel(Data, excel_path)
    # PlotData(Data['Google'], 'Google Search Results')
    # PlotData(Data['Google Scholar'], 'Google Scholar Results')
    # PlotData(Data['Arix'], 'Arix Results')
    # PlotData(Data['Sematic Scholar'], 'Sematic Scholar Results')


    fp.close()




def get_results_parallel(search_term, start_date, end_date):
    results = []
    formatted_results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_query = {executor.submit(GetResultsGoogle, q, date, date, proxies): (q, date, "Google") for q in search_term for date in range(start_date, end_date + 1)}
        future_to_query.update({executor.submit(GetResultsGoogleScholar, q, date, date, proxies): (q, date, "Google Scholar") for q in search_term for date in range(start_date, end_date + 1)})
        future_to_query.update({executor.submit(GetResultsArix, q, date, date, proxies): (q, date, "Arix") for q in search_term for date in range(start_date, end_date + 1)})
        future_to_query.update({executor.submit(GetResultsSemanticScholar, q, date, date, proxies): (q, date, "Semantic Scholar") for q in search_term for date in range(start_date, end_date + 1)})
        
        # Iterate over completed futures
        for future in as_completed(future_to_query):
            q, date, source = future_to_query[future]
            try:
                num_results, success = future.result()
                results.append((q, date, source, num_results, success))

                # Update formatted_results dictionary
                if source not in formatted_results:
                    formatted_results[source] = {}
                if q not in formatted_results[source]:
                    formatted_results[source][q] = {}
                formatted_results[source][q][date] = num_results
                
            except Exception as e:
                print(f"Exception for {q} - {date} - {source}: {e}")

    # Process the results as needed
    for q, date, source, num_results, success in results:
        if not success:
            print(f"Failed to get results for {q} - {date} - {source}")
    print(formatted_results)
    return formatted_results

if __name__ == "__main__":
    start_time = time.time()
    search_term = ['Responsible AI','RAI','Ethical AI','AI Governance','AI Accountability','Responsible AI','AI Privacy', 'Responsible Geographic Information Systems','Geographic Information Systems','Spatial Analysis','Cartography','GIS Mapping','GIS Privacy','Fair GIS Applications','GIS Impact Assessment','Responsible Geospatial Technology','Ethical Cartography']
    start_date = 2013
    end_date = 2023
    ip = GetIP()
    proxies = {'http': ip, 'https': ip}
    Data = get_results_parallel(search_term, start_date, end_date)
    
    print(Data)
    Tempdata = Data['Google']
    plot_trend_chart({'Google':Tempdata}, 'Google Search Results')
    Tempdata = Data['Google Scholar']
    plot_trend_chart({'Google Scholar':Tempdata}, 'Google Scholar Results')
    Tempdata = Data['Arix']
    plot_trend_chart({'Arix':Tempdata}, 'Google Search Results')
    Tempdata = Data['Semantic Scholar']
    plot_trend_chart({'Semantic Scholar':Tempdata}, 'Google Search Results')
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")