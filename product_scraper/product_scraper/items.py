import pandas as pd
from pytrends.request import TrendReq
import plotly.express as px

# Define the search parameters
start_date = '2023-01-01'
end_date = '2023-12-31'
queries = ['Javascript', 'Python']​
# This create a pytrends client
pytrends = TrendReq(hl='en-US', tz=360)

# Create an empty DataFrame to store Google Trends data
combined_interest_df = pd.DataFrame()

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

# Create an interactive line chart with Plotly
fig = px.line(melted_df, x=melted_df.index, y='Interest', color='Query', title='Google Trends - Interest Over Time')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='Interest Score')
fig.show()