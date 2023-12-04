import requests
from bs4 import BeautifulSoup
import re
import plotly.express as px
import pandas as pd


def scrape_google_scholar(query):
    response_htmlcontent = GetHtmlCon(query)
    soup = BeautifulSoup(response_htmlcontent, 'html.parser')
    publications = []
    results = soup.find_all('div', class_='gs_ri')
    for result in results:
        title = result.find('h3', class_='gs_rt').get_text()
        year_match = re.search(r'\d{4}', result.get_text()) 
        year = year_match.group() if year_match else 'Year not found'
        publications.append((title, year))
    return publications

def GetHtmlCon(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }
    htmlcontent = ''
    for i in range(0, 50):
        base_url = f'https://scholar.google.com/scholar?start={i * 10}&q={query}&hl=en&as_ylo={2010}&as_yhi={2023}'
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            htmlcontent = htmlcontent + response.text
        else:
            print(f"Failed to retrieve data for query: {query},{response.status_code}")
            break
    html_content = htmlcontent
    return html_content


queries = ['Responsible AI using Geographic Instruction', 'C-programming using gaming']  
data = {}

for query in queries:
    publications = scrape_google_scholar(query)

    year_count = {}
    for title, year in publications:
        if year in year_count:
            year_count[year] += 1
        else:
            year_count[year] = 1
    data[query] = year_count

# Combine data for all queries into a DataFrame
combined_data = {'Year': sorted(set(year for year_count in data.values() for year in year_count.keys()))}
for query in queries:
    combined_data[query] = [data[query].get(year, 0) for year in combined_data['Year']]

df = pd.DataFrame(combined_data)

# Create a line chart using Plotly Express
fig = px.line(df, x='Year', y=queries, labels={'Year': 'Year', 'value': 'Number of Publications'},
             title=f'Year-wise Trend of Publications for -  {", ".join(queries)}')

# Show the interactive chart
fig.show()
