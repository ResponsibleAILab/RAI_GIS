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


from RAI_GOOGLE_SCHOLAR import get_results_parallel, GetResultsGoogle


app = Flask(__name__)



#--------------------------------Function to get the Trends----------------------------
@app.route('/api/GetData', methods=['POST'])
def GetDataFromDataSource(query, start_date, end_date):
    start_time = time.time()
    Data = get_results_parallel(queryquery,start_date,end_date)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")
# To Print the results
    Tempdata = Data['Google']
    plot_trend_chart({'Google':Tempdata}, 'Google Search Results')
    Tempdata = Data['Google Scholar']
    plot_trend_chart({'Google Scholar':Tempdata}, 'Google Scholar Results')
    Tempdata = Data['Arix']
    plot_trend_chart({'Arix':Tempdata}, 'Arix Results')
    Tempdata = Data['Semantic Scholar']
    plot_trend_chart({'Semantic Scholar':Tempdata}, 'Semantic Scholar Results')


#--------------------------- To webscrapping the google scholar--------------------


#----------------------------To get the value from the user------------------------

@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    start_time = time.time()
    data = request.json 
    ResData = get_results_parallel(data['trends'],data['startDate'],data['endDate'])
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time} seconds")
    print(ResData)

    Tempdata = ResData['Google']
    plot_trend_chart({'Google':Tempdata}, 'Google Search Results')
    # Tempdata = ResData['Google Scholar']
    # plot_trend_chart({'Google Scholar':Tempdata}, 'Google Scholar Results')
    Tempdata = ResData['Arix']
    plot_trend_chart({'Arix':Tempdata}, 'Google Search Results')
    Tempdata = ResData['Semantic Scholar']
    plot_trend_chart({'Semantic Scholar':Tempdata}, 'Google Search Results')

    return jsonify({'message': 'Data received successfully'})

#----------------------------Python Flask Application-------------------------------
@app.route('/')
def home():
    return render_template('index.html')
#-----------------------------------------------------------------------------------
def print_hi(name):
    print(f'Hi, {name}')
if __name__ == '__main__':
    app.run(debug=True)
