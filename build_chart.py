import plotly.express as px
import pandas as pd

def main(df_input):
    df_column_dtype = ['AQI index', 'CO', 'NO2', 'O3', 'SO2', 'Dew', 'Humidity', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']
    df = pd.read_csv(df_input)
    df_plt = df[df_column_dtype].groupby(df['Month']).mean().reset_index()
    for i in df_column_dtype:
        fig = px.line(df_plt, x='Month', y=df_plt[i], title=f'Line Plot for {i}')
        fig.show()

if __name__ == "__main__":
    main("data\\result\\pre-process-data.csv")