# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 08:40:16 2021

@author: pooja
"""

import streamlit as st
import warnings
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as plty
import plotly.graph_objs as go 
from plotly import tools
from plotly.offline import init_notebook_mode, iplot, plot 

import pyttsx3

def data_prep(data_file):
    data_file.drop(["Unnamed: 0"],inplace=True,axis=1)
    data_file['totals.sessionQualityDim'].fillna(0, inplace=True)
    data_file['totals.timeOnSite'].fillna(0, inplace=True)
    data_file['trafficSource.keyword'].replace(['nan','NaN','(not provided)'], 'others',inplace=True)
    data_file['trafficSource.keyword'].fillna('others', inplace=True)
    data_file['totals.transactions'].fillna(0, inplace=True)
    data_file['totals.transactionRevenue'].fillna(0, inplace=True)
    data_file.replace(to_replace=" None", value=0,inplace=True)
    return data_file

def explore_revenue(df_train):
    fig = plt.figure(figsize=(20,5))
    plt.suptitle('Distribuition of Revenue', fontsize=30)

    ax1 = fig.add_subplot(121)
    _ = sns.distplot(np.log(df_train[df_train['totals.transactionRevenue'] > 0]["totals.transactionRevenue"]), bins=40,color='#e56b6f', ax=ax1)
    _ = ax1.set_ylabel('Distribution', fontsize=20)
    _ = ax1.set_xlabel('Transaction Revenue Log', fontsize=20)


    ax2 = fig.add_subplot(122)
    _ = plt.scatter(range(df_train.shape[0]),np.sort(df_train['totals.transactionRevenue'].values))
    _ = ax2.set_ylabel('Distribution', fontsize=20)
    _ = ax2.set_xlabel('Revenue', fontsize=20)
    st.pyplot()
    observations = pyttsx3.init()
    observations.say("The above graph shows that only a small percentage of customers produce most of the revenue.")
    observations.runAndWait()
    
def horizontal_bar_chart(cnt_srs, color):
    trace = go.Bar(
        y=cnt_srs.index[::-1],
        x=cnt_srs.values[::-1],
        showlegend=False,
        orientation = 'h',
        marker=dict(
            color=color,
        ),
    )
    return trace


def device_revenue(df_train):
    df_train['device.browser'].value_counts()[:10].reset_index()
    
    # Device Browser
    cnt_srs = df_train.groupby('device.browser')['totals.transactionRevenue'].agg(['size', 'sum', 'mean'])
    cnt_srs.columns = ["count", "total revenue", "mean"]
    cnt_srs = cnt_srs.sort_values(by="count", ascending=False)
    trace1 = horizontal_bar_chart(cnt_srs["count"].head(10), '#073b4c')
    trace2 = horizontal_bar_chart(cnt_srs["total revenue"].head(10), '#073b4c')
    trace3 = horizontal_bar_chart(cnt_srs["mean"].head(10), '#073b4c')

    # Device Category
    cnt_srs = df_train.groupby('device.deviceCategory')['totals.transactionRevenue'].agg(['size', 'sum', 'mean'])
    cnt_srs.columns = ["count", "total revenue", "mean"]
    cnt_srs = cnt_srs.sort_values(by="count", ascending=False)
    trace4 = horizontal_bar_chart(cnt_srs["count"].head(10), '#118ab2')
    trace5 = horizontal_bar_chart(cnt_srs["total revenue"].head(10), '#118ab2')
    trace6 = horizontal_bar_chart(cnt_srs["mean"].head(10), '#118ab2')
    
    # Operating system
    cnt_srs = df_train.groupby('device.operatingSystem')['totals.transactionRevenue'].agg(['size', 'sum', 'mean'])
    cnt_srs.columns = ["count", "total revenue", "mean"]
    cnt_srs = cnt_srs.sort_values(by="count", ascending=False)
    trace7 = horizontal_bar_chart(cnt_srs["count"].head(10), '#ef476f')
    trace8 = horizontal_bar_chart(cnt_srs["total revenue"].head(10),'#ef476f')
    trace9 = horizontal_bar_chart(cnt_srs["mean"].head(10),'#ef476f')

    # Creating two subplots
    fig = tools.make_subplots(rows=3, cols=3, vertical_spacing=0.04, 
                          subplot_titles=["Device Browser - Count", "Device Browser - Total Revenue", "Device Browser - Mean Revenue",
                                          "Device Category - Count",  "Device Category - Total Revenue ", "Device Category - Mean Revenue", 
                                          "Device OS - Count", "Device OS - Total Revenue", "Device OS - Mean Revenue"])

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 3)
    fig.append_trace(trace4, 2, 1)
    fig.append_trace(trace5, 2, 2)
    fig.append_trace(trace6, 2, 3)
    fig.append_trace(trace7, 3, 1)
    fig.append_trace(trace8, 3, 2)
    fig.append_trace(trace9, 3, 3)

    fig['layout'].update(height=1200, width=1500, template='plotly_white',paper_bgcolor='#ffffff', title="Device Plots")
    #plty.iplot(fig, filename='device-plots')
    fig.show()
    
    observations = pyttsx3.init()
    observations.say("The above graph shows that customers with desktop, operating with windows and using chrome are genrating highest revenue.")
    observations.runAndWait()
    
def channel_revenue(df_train):
    group = df_train.groupby('channelGrouping')['totals.transactionRevenue'].agg(['count','sum','mean']).reset_index()

    color = ["#ffa69e","#faf3dd","#b8f2e6","#aed9e0","#5e6472",'#f6bd60','#84a59d','#f8edeb']
    customPalette = sns.set_palette(sns.color_palette(color))

    fig = plt.figure(figsize=(10,10))

    ax1 = fig.add_subplot(311)
    _ = sns.barplot(data=group, x='channelGrouping', y='count', palette= customPalette, ax=ax1)
    xlabels = group['channelGrouping'].to_list()
    ylabels = group['count']
    _ = ax1.set_title('Number of Users', fontsize=20)
    _ = ax1.set_ylabel('Number of Users', fontsize=14)
    _ = ax1.set_xlabel('')
    _ = ax1.set_xticklabels(xlabels, rotation=30, fontsize=10)

    ax2 = fig.add_subplot(312)
    _ = sns.barplot(data=group, x='channelGrouping', y='sum', palette= customPalette, ax=ax2)
    xlabels = group['channelGrouping'].to_list()
    ylabels = group['sum']
    _ = ax2.set_title('Total Revenue', fontsize=20)
    _ = ax2.set_ylabel('Total Revenue', fontsize=14)
    _ = ax2.set_xlabel('')
    _ = ax2.set_xticklabels(xlabels, rotation=30, fontsize=10)
    
    ax3 = fig.add_subplot(313)
    _ = sns.barplot(data=group, x='channelGrouping', y='mean', palette= customPalette, ax=ax3)
    xlabels = group['channelGrouping'].to_list()
    ylabels = group['mean']    
    
    _ = ax3.set_title('Average Revenue', fontsize=20)
    _ = ax3.set_ylabel('Average Revenue', fontsize=14)
    _ = ax3.set_xlabel('')
    _ = ax3.set_xticklabels(xlabels, rotation=30, fontsize=10)
    
    fig.tight_layout(pad=0.5)
    st.pyplot()
    
    observations = pyttsx3.init()
    observations.say("These plots tells us that most people are doing their search via organic search whereas highest revenue is generated by referral.")
    observations.runAndWait()
    
def browser_devices(df_train):
    st.image("img.png", use_column_width = True)
    observations = pyttsx3.init()
    observations.say("The above plot shows that Chrome is quite popular in most of the devices and Safari is mostly used on Mac OS and IOS devices")
    observations.runAndWait()

def os_revenue(df_train):
    group = df_train[(df_train['device.operatingSystem'].isin\
         (df_train[df_train['totals.transactionRevenue'] > 0]['device.operatingSystem'].value_counts().reset_index()[:6]['index']))
        & (df_train['totals.transactionRevenue'] > 0)]

    _ = sns.FacetGrid(group,
                      hue='device.operatingSystem', height=3, aspect=1)\
        .map(sns.kdeplot, 'totals.transactionRevenue', shade=True)\
                .add_legend()
                
    st.pyplot()
    
    observations = pyttsx3.init()
    observations.say("Windows has the highest widespread of transaction revenue whereas linux has the highest peak of transaction revenue.")
    observations.runAndWait()
    
def device_dist(df_train):
    color = ['#14213d','#fca311','#d90429']

    customPalette = sns.set_palette(sns.color_palette(color))
    
    _ = sns.FacetGrid(df_train[df_train['totals.transactionRevenue'] > 0],
                         hue='device.deviceCategory', height=3, aspect=1, palette=customPalette)\
        .map(sns.kdeplot, 'totals.transactionRevenue', shade=True)\
            .add_legend()
    st.pyplot()
    
    observations = pyttsx3.init()
    observations.say("Desktop has the highest widespread of transaction revenue whereas Tablet has the highest peak of transaction revenue.")
    observations.runAndWait()
    
def day_info(df_train):
    #seting some static color options
    color_op = ['#5527A0', '#BB93D7', '#834CF7', '#6C941E', '#93EAEA', '#7425FF', '#F2098A', '#7E87AC', 
            '#EBE36F', '#7FD394', '#49C35D', '#3058EE', '#44FDCF', '#A38F85', '#C4CEE0', '#B63A05', 
            '#4856BF', '#F0DB1B', '#9FDBD9', '#B123AC']

    # Visits by time train

    # couting all entries by date to get number of visits by each date
    dates_temp = df_train['date'].value_counts().reset_index().sort_values('index') 
    # renaming the columns to apropriate names
    dates_temp.columns = ['date','visits'] 

    # creating the first trace with the necessary parameters
    trace = go.Scatter(x=dates_temp.date.astype(str), y=dates_temp.visits,
                       opacity = 0.8, line = dict(color = '#38C788'), name= 'Visits by day')

    # Below we will get the total values by Transaction Revenue Log by date
    dates_temp_sum = df_train.groupby('date')['totals.transactionRevenue'].sum().reset_index()

    # using the new dates_temp_sum we will create the second trace
    trace1 = go.Scatter(x=dates_temp_sum.date.astype(str), line = dict(color = '#C73877'), name="RevenueLog by day",
                        y=dates_temp_sum['totals.transactionRevenue'], opacity = 0.8)

    # Getting the total values by Transactions by each date
    dates_temp_count = df_train[df_train['totals.transactionRevenue'] > 0].groupby('date')['totals.transactionRevenue'].count().reset_index()

    # using the new dates_temp_count we will create the third trace
    trace2 = go.Scatter(x=dates_temp_count.date.astype(str), line = dict(color = color_op[5]), name="Sellings by day",
                        y=dates_temp_count['totals.transactionRevenue'], opacity = 0.8)

    #creating the layout the will allow us to give an title and 
    # give us some interesting options to handle with the outputs of graphs
    layout = dict(
    title= "Informations by Date",
    paper_bgcolor='#ffffff',
    template='plotly_white',
    xaxis=dict(
        rangeselector=dict(buttons=list([
                dict(count=1, label='1m', step='month', stepmode='backward'),
                dict(count=3, label='3m', step='month', stepmode='backward'),
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(visible = True),
        type='date'
    )
)

    # creating figure with the both traces and layout
    fig = dict(data= [trace, trace1, trace2], layout=layout)

    #rendering the graphs
    iplot(fig) #it's an equivalent to plt.show()
    st.pyplot()

    
def country_visits(df_train):
    countMaps = pd.DataFrame(df_train['geoNetwork.country'].value_counts()).reset_index()
    countMaps.columns=['country', 'counts'] #renaming columns
    countMaps = countMaps.reset_index().drop('index', axis=1) #reseting index and droping the column

    data = [ dict(
        type = 'choropleth',
        locations = countMaps['country'],
        locationmode = 'country names',
        z = countMaps['counts'],
        text = countMaps['country'],
        colorscale = 'YlGnBu',
        autocolorscale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '',
            title = 'Number of Visits'),
      ) ]
    layout = dict(
    title = 'Couting Visits Per Country',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'natural earth'
        )
    )
)

    figure = dict( data=data, layout=layout )
    iplot(figure, validate=False, filename='map-countrys-count')
    st.pyplot()

    
def viz(df):
    if(st.checkbox("Revenue Exploration")):
        explore_revenue(df)
    elif(st.checkbox("Revenue based on Browsers/Device/Operating System")):
        device_revenue(df)
    elif(st.checkbox("Channel Groups and their Revenue")):
        channel_revenue(df)
    elif(st.checkbox("Browsers used on Different Devices")):
        browser_devices(df)
    elif(st.checkbox("Distribution of transaction Revenue of OS's")):
        os_revenue(df)
    elif(st.checkbox("Distribution of transaction Revenue of Device Category")):
        device_dist(df)
    elif(st.checkbox("Vistis/Revenue/Sellings by Day")):
        day_info(df)
    elif(st.checkbox("Counting Visits Per Country")):
        country_visits(df)
        
        
        
def main():
    st.title("Multichannel Marketing")
    data_file = st.file_uploader("Upload CSV",type=["csv"])
    if data_file is not None:
        st.write(type(data_file))
        file_details ={"filename":data_file.name, "filetype":data_file.type, "filesize":data_file.size}
        st.write(file_details)
        data_file = pd.read_csv(data_file)
        data_file = data_prep(data_file)
        
    add_selectbox = st.selectbox('',('Choose an option', 'Data Description', 'Plots'))
    if(add_selectbox == 'Data Description'):
        pass
    elif(add_selectbox == 'Plots'):
        viz(data_file)

    
if __name__ == '__main__':
    main()