import pandas as pd
import plotly.express as px
from scholarly import scholarly

def Search_Publications_Year(query):
    search_query = scholarly.search_pubs(query)

    # Created a directory to store the values 
    publication_years = {}
    #iterate each publications and check the count for each year
    for i, result in enumerate(search_query):
        publication_year = result['bib'].get('pub_year', 'N/A')
        #Not aviable years contion is added
        if publication_year != 'N/A':
            publication_years[publication_year] = publication_years.get(publication_year, 0) + 1

    combined_data = {'Year': sorted(set(publication_years.keys()))}
    combined_data[query] = [publication_years.get(year, 0) for year in combined_data['Year']]

# line chart using plotly express
    df = pd.DataFrame(combined_data)
    df = df.fillna(0)
    fig = px.line(df, x='Year', y=query, labels={'Year': 'Year', 'value': 'Number of Publications'},title=f'Year-wise Trend of Publications for - {query}')
    fig.update_xaxes(range=[min(df['Year']), max(df['Year'])])
    fig.show()
Search_Publications_Year("Responsible AI")
