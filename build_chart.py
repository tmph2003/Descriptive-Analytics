import plotly.express as px
import pandas as pd
from d3blocks import D3Blocks
from time import strftime

def pol_ind_by_month(df, df_column_dtype):
    df_plt1 = df[df_column_dtype + ['Month']].groupby(['Month']).mean().reset_index()
    fig = None
    fig = px.line(title=f'Line Plot for pollution indexes')
    for i in df_column_dtype:
        fig.add_scatter(x=df_plt1['Month'], y=df_plt1[i], mode='lines', name=f'{i}')
        fig.update_xaxes(title='Month')
        fig.update_yaxes(title='Pollution index')
    fig.show()

def pol_ind_by_station(df, df_column_dtype):
    df_plt2 = df[df_column_dtype + ['Station ID']].groupby('Station ID').mean().reset_index()
    df_plt2['Station ID'] = df_plt2['Station ID'].astype('string')
    
    index_info = {
        'AQI index': 151,
        'CO': 10,
        'NO2': 41,
        'O3': 51,
        'SO2': 21,
        'PM10': 51,
        'PM2.5': 26
    }
    for i in df_column_dtype:
        fig = px.bar(df_plt2, x='Station ID', y=f'{i}', title=f'{i}')
        
        if i in index_info:
            fig.add_scatter(x=df_plt2['Station ID'], y=[index_info[i]] * len(df_plt2), mode='lines', line=dict(color="red", dash='dash'), name='Dangerous')
        
        fig.update_xaxes(title='Station ID')
        fig.update_yaxes(title=f'{i} mean')
        fig.show()

def pol_ind_by_month_station(df, df_column_dtype):
    df_plt3 = df[df_column_dtype + ['Month', 'Station ID']].groupby(['Month', 'Station ID']).mean().reset_index()
    index_info = {
        'AQI index': 151,
        'CO': 10,
        'NO2': 41,
        'O3': 51,
        'SO2': 21,
        'PM10': 51,
        'PM2.5': 26
    }
    
    for i in df_column_dtype:
        fig = px.line(title=f'Line Plot for {i}')  # Initialize the figure with a title
        
        if i in index_info:
            fig.add_scatter(x=df_plt3['Month'], y=[index_info[i]] * len(df_plt3), mode='lines', line=dict(color="red", dash='dash'), name='Dangerous')
        
        for j in df_plt3['Station ID'].unique():
            df_station = df_plt3[df_plt3['Station ID'] == j]
            fig.add_scatter(x=df_station['Month'], y=df_station[i], mode='lines', name=f'Station ID {j}')
        
        fig.show()

def moving_bubbles_plot(df):
    df_plt4 = df[['Station ID', 'Data Time S', 'Status']]
    df_plt4.rename(columns={"Station ID": "sample_id", "Data Time S": "datetime", "Status": "state"}, inplace=True)
    df_plt4['datetime'] = pd.to_datetime(df_plt4['datetime'])
    df_plt4['datetime'] = df_plt4['datetime'].dt.strftime("%d-%m-%Y %H:%M:%S")
    d3 = D3Blocks()
    d3.movingbubbles(df_plt4, datetime="datetime", sample_id="sample_id", state="state", filepath="./moving_point.html",
                    note="Vietnam's AQI index in 2021 for each day", cmap="hsv", center="Good", figsize=(780, 800), size=10, speed=1000000000)

def heatmap_plot(df, df_column_dtype):
    df_plt = df[df_column_dtype]
    fig = px.imshow(df_plt.corr(), x=df_plt.columns, y=df_plt.columns, aspect='auto')
    fig.show()

def main(df_input):
    df_column_dtype = ['AQI index', 'CO', 'NO2', 'O3', 'SO2', 'Dew', 'Humidity', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']
    df = pd.read_csv(df_input)
    #Chart1
    pol_ind_by_month(df=df, df_column_dtype=df_column_dtype)
    # #Chart2
    pol_ind_by_station(df=df, df_column_dtype=df_column_dtype)
    # #Chart3
    pol_ind_by_month_station(df=df, df_column_dtype=df_column_dtype)
    #Chart4
    heatmap_plot(df=df, df_column_dtype=df_column_dtype)

if __name__ == "__main__":
    main("data\\result\\pre-process-data.csv")