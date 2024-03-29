# data processing
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


# data visualization
import plotly.graph_objs as go
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False 

# change text color
import colorama
from colorama import Fore, Style

def GET_csse_covid_19_time_series():


    print('getiing data')
    repo = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

    ts_confirmed_us = pd.read_csv(repo+'time_series_covid19_confirmed_US.csv')
    ts_confirmed_global = pd.read_csv(repo+'time_series_covid19_confirmed_global.csv')

    ts_deaths_us = pd.read_csv(repo+'time_series_covid19_deaths_US.csv')
    ts_deaths_global = pd.read_csv(repo+'time_series_covid19_deaths_global.csv')

    ts_recovered_global = pd.read_csv(repo+'time_series_covid19_recovered_global.csv')


    print('finsh')
    return ts_confirmed_us,ts_confirmed_global,ts_deaths_us,ts_deaths_global,ts_recovered_global



def GET_csse_covid_19_daily_reports():

    print('geting daily reports')

    # global
    ts_confirmed_us = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

    latest = pd.to_datetime(ts_confirmed_us.columns[-1]).strftime('%m-%d-%Y')
    prev = (pd.to_datetime(ts_confirmed_us.columns[-1])+timedelta(-1)).strftime('%m-%d-%Y')

    url_latest_global = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{latest}.csv'
    latest_data_global = pd.read_csv(url_latest_global)

    url_prev_global = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{prev}.csv'
    prev_data_global = pd.read_csv(url_prev_global)

    url_latest_us = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{latest}.csv'
    latest_data_us = pd.read_csv(url_latest_us)

    url_prev_us = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{prev}.csv'
    prev_data_us = pd.read_csv(url_prev_us)


    print('finish')
    return latest_data_global,prev_data_global,latest_data_us,prev_data_us

def GET_shanghai_data(plot = True, encoding = "UTF-8"):

    '''
    data_name:'ts_shanghai_covid', 'latest_shanghai_covid'，'ts_shanghai_covid'
    '''
    import re
    print('getting data from shanghai......')
    url = f'https://raw.githubusercontent.com/datoujinggzj/WhalePkg/master/DATA/ts_shanghai_covid.csv'
    data = pd.read_csv(url,encoding = encoding)['detail']
    print('finish')

    data = data[data.apply(lambda x: x.startswith('上海202'))].sort_values()
    data = data.apply(lambda x: re.sub(r'\（.*?\）', '', x))
    data = data.apply(lambda x: x.replace('无新增','0'))

    df_all = pd.DataFrame(map(np.ravel,data.apply(lambda x: re.findall(r"\d+",x)))).rename({
        0: 'Year',
        1: 'Month',
        2: 'Day',
        3: 'New Local Confirmed Cases',
        4: 'New Local Asymptomatic Cases'
    },axis=1).iloc[:,:5]
    df_all['Date'] = df_all['Year'].map(str) + "/" + df_all['Month'].map(str) + "/" + df_all['Day'].map(str)
    df_all['Date'] = pd.to_datetime(df_all['Date'])

    df_all = df_all.set_index('Date').sort_index()
    df_all = df_all.astype('int32')
    df = df_all.iloc[:,3:5]

    if plot:
        fig, axes = plt.subplots(nrows=2, ncols=1,figsize = [10,5*2])
        df_2022 = df[df.index>'2022-01-01']
        for col,ax in zip(df_2022.columns,axes):
            ax.step(df_2022.index, df_2022[col], color = '#202124',linewidth = 2)
            ax.bar(df_2022.index, df_2022[col],alpha = .8)
            ax.vlines(x=pd.to_datetime("2022-04-01"), ymin=0, ymax=df[col].max(), linewidth=2, color = '#4b7ffc', linestyle = '--')
            ax.vlines(x=pd.to_datetime("2022-06-01"), ymin=0, ymax=df[col].max(), linewidth=2, color = '#4b7ffc', linestyle = '--')

            ax.hlines(y=df[col].max(), xmin=df_2022.index[0], xmax=df_2022.index[-1], linewidth=1, color = '#ff0000')
            ax.text(x = df_2022.index[0], s=df[col].max(),y = df[col].max(), color = 'black', fontsize = 14)
            ax.text(x=df_2022.index[0], y=df[col].max()/2, s=f"Peak: Date: {str(df.index[df[col].argmax()])} \nNew: {df[col].max()} cases", color='#ff0000', fontsize=18)
            ax.text(x=df_2022.index[0], y=df[col].max()/4, s=f"Today: Date: {str(df.index[-1])} \nNew: {df[col][-1]} cases", color='#ff0000', fontsize=18)

            ax.text(x=pd.to_datetime("2022-03-15"), y=df[col].max()*2/3, s="Started as a joke\nApril 1, 2022", color='black', fontsize=12)
            ax.text(x=pd.to_datetime("2022-05-15"), y=df[col].max()*2/3, s="Ended in play\nJune 1, 2022", color='black', fontsize=12)

            ax.set_xlabel('Date')
            ax.set_ylabel(f'Number of {col}')
            ax.set_title(f'Time Series Trend of {col}', fontsize=16)

        plt.tight_layout()
