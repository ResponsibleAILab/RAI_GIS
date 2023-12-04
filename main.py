from flask import Flask, render_template, request, jsonify
from pytrends.request import TrendReq
app = Flask(__name__)
import requests
import datetime
import json

from bs4 import BeautifulSoup
from urllib.request import Request, build_opener, HTTPCookieProcessor, ProxyHandler, FancyURLopener
from urllib.parse import urlencode
import re, time, urllib
from fp.fp import FreeProxy
import random
import matplotlib.pyplot as plt
import csv
from semanticscholar import SemanticScholar
import pandas as pd
import plotly.graph_objects as go


app = Flask(__name__)

# Initialize the pytrends object
pytrends = TrendReq()


#--------------------------------Function to get the Trends----------------------------
@app.route('/api/Rai_Trend', methods=['POST'])
def scrape_google_scholar(query, start_date, end_date, step_days=7):
    # base_url = "https://scholar.google.com"
    for query in queries:
    # Build the payload for the current query
        pytrends.build_payload(kw_list=[query], cat=0, timeframe=f"{start_date} {end_date}", geo='US', gprop='')

    # Get Google Trends data for the current query
    interest_over_time_df = pytrends.interest_over_time()

    # Rename the query column to the current query name
    column_name = f'{query}_interest'
    interest_over_time_df = interest_over_time_df.rename(columns={query: column_name})

    # Combine the data into the main DataFrame
    if combined_interest_df.empty:
        combined_interest_df = interest_over_time_df[[column_name]]
    else:
        combined_interest_df = pd.concat([combined_interest_df, interest_over_time_df[[column_name]]], axis=1)

    # converts the  DataFrame to long-form
    melted_df = combined_interest_df.melt(ignore_index=False, var_name='Query', value_name='Interest')
    return search_results


#--------------------------- To webscrapping the google scholar--------------------

# @app.route('/api/google_scholar_web', methods=['POST'])
# def scrape_google_scholar(query):
#     response_htmlcontent = GetHtmlCon(query)
#     # Create a BeautifulSoup object
#     soup = BeautifulSoup(response_htmlcontent, 'html.parser')
#     # Extract information (for example, the publication titles and years)
#     publications = []
#     results = soup.find_all('div', class_='gs_ri')
#     for result in results:
#         title = result.find('h3', class_='gs_rt').get_text()
#         year_match = re.search(r'\d{4}', result.get_text())  # Assuming years are in the format 'YYYY'
#         year = year_match.group() if year_match else 'Year not found'
#         publications.append((title, year))
#     return publications

def GetHtmlCon(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }
    htmlcontent = ''  # Initialize the variable to store HTML content
    for i in range(0, 100):
        base_url = f'https://scholar.google.com/scholar?start={i * 10}&q={query}&hl=en&as_ylo={2010}&as_yhi={2023}'
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            htmlcontent = htmlcontent + response.text
        else:
            print(f"Failed to retrieve data for query: {query},{response.status_code}")
            break
    html_content = htmlcontent
    return html_content
 
    for query in queries:
        publications = scrape_google_scholar(query)

    # Create a dictionary to store the count of publications per year for each query
    year_count = {}
    for title, year in publications:
        if year in year_count:
            year_count[year] += 1
        else:
            year_count[year] = 1
    data[query] = year_count

# Example queries:
# queries = ['Responsible AI using Geographic Instruction', 'C-programming using gaming']  # Change this to your desired search queries
# data = {}
# # Combine data for all queries into a DataFrame
# combined_data = {'Year': sorted(set(year for year_count in data.values() for year in year_count.keys()))}
# for query in queries:
#     combined_data[query] = [data[query].get(year, 0) for year in combined_data['Year']]

# df = pd.DataFrame(combined_data)

# # Create a line chart using Plotly Express
# fig = px.line(df, x='Year', y=queries, labels={'Year': 'Year', 'value': 'Number of Publications'},
#              title=f'Year-wise Trend of Publications for -  {", ".join(queries)}')

# # Show the interactive chart
# fig.show()
   
#----------------------------To get the value from the user------------------------

@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    data = request.json 
    #To convert into a json format string
    trends_dict = json.dumps(data)  
    # json.loads is used to parse the JSON string
    parsed_data = json.loads(trends_dict)
    # Extract the values from the parsed JSON data
    values = list(parsed_data.values())
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    result1= scrape_google_scholar_web(values)
    results = scrape_google_scholar(values, start_date, end_date, step_days=7)
    #print(results)
    # You can now use userInput in your Python code
    return jsonify({'message': 'Data received successfully'})
#----------------------------Python Flask Application-------------------------------
@app.route('/')
def home():
    return render_template('index.html')


#-----------------------------------------------------------------------------------
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
