#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:57:58 2020
COVID-19 Time Series
@author: jacob
"""

import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce


confirmed = pd.read_csv('3-22-20-time_series-ncov-Confirmed.csv')
deaths = pd.read_csv('3-22-20-time_series-ncov-Deaths.csv')
recovered = pd.read_csv('3-22-20-time_series-ncov-Recovered.csv')

dfs =  [confirmed, deaths, recovered]
combined = reduce(lambda left,right: pd.merge(left,right,on=['Date','Country/Region','Province/State']), dfs)
combined ['Date']= pd.to_datetime(combined ['Date'])
combined = combined.rename(columns={'Value_x': 'confirmed', 'Value_y': 'deaths', 'Value': 'recovered'})
combined = combined.set_index('Date')

# #https://plotly.com/python/time-series/
# import plotly.graph_objects as go
# fig = go.Figure([go.Scatter(x=combined['Date'], y=combined['confirmed'])])
# fig.show()
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=combined.Date, y=combined['confirmed'], name="Number of confirmed cases",
#                          line_color='deepskyblue'))
# fig.add_trace(go.Scatter(x=combined.Date, y=combined['deaths'], name="Number of deaths",
#                          line_color='dimgray'))
# fig.add_trace(go.Scatter(x=combined.Date, y=combined['recovered'], name="Number ercovered",
#                          line_color='red'))
# fig.show()


# import plotly.express as px
# fig = px.line(combined, x='Date', y='confirmed')
# fig.show()

# Using Matplotlib
def make_time_series_plot(country = 'Afghanistan', logscale = False):
# Check if there are multiple regions in the country
    plot_data = combined[combined['Country/Region'].str.lower() == country.lower()]
    if (plot_data['Province/State'].nunique() > 1):
        confirmed = plot_data.groupby('Date').confirmed.sum()
        deaths = plot_data.groupby('Date').deaths.sum()
        recovered = plot_data.groupby('Date').recovered.sum()
    else:
        confirmed = plot_data.confirmed
        deaths = plot_data.deaths
        recovered = plot_data.recovered
        
    if logscale:
        confirmed = np.log(confirmed+1)
        deaths = np.log(deaths+1)
        recovered = np.log(recovered+1)

    plt.figure(figsize=(20,10))
    plt.plot(confirmed, color = 'red', label = 'Number of confirmed cases')
    plt.plot(deaths, color = 'blue', label = 'Number of deaths')
    plt.plot(recovered, color = 'green', label = 'Number recovered')
    plt.title('COVID-19 Cases in '+str(country))
    plt.xlabel('Time')
    plt.xticks(rotation=90)
    plt.ylabel('Number')
    plt.legend()
    plt.show()






