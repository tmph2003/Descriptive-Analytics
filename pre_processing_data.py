import pandas as pd

def summarization_data(df):
    print("====================Summarizing data====================")
    description = df.describe()
    mode = df.select_dtypes(include=['float64','int64']).mode().iloc[0]
    median = df.select_dtypes(include=['float64','int64']).median()
    mode.name = 'mode'
    median.name = 'median'
    description = description._append(mode)._append(median)
    print(description)
    description.to_csv("data\\result\\DATA_SUMMARIZATION_0.csv")
    print("====================Tỷ lệ thiếu data====================")
    data_na = (df.isnull().sum() / len(df)) * 100
    missing_data = pd.DataFrame({"Tỷ lệ thiếu data(%)" : data_na})
    print(missing_data)

    print("===============Số lượng data bị trùng lặp===============")
    duplicated_rows_data = df.duplicated().sum()
    print(f"\nSố lượng data trùng lặp: {duplicated_rows_data}")

    print("================Số lượng data riêng biệt================")
    print("\nSố lượng data riêng biệt:")
    num_distinct_values = []
    for column in df.columns:
        num_distinct_values.append(len(df[column].unique()))
    distinct_values_df = pd.DataFrame({'Column': df.columns, 'NumDistinctValues': num_distinct_values})
    print(distinct_values_df)

    print(f"\n5 dòng đầu của dataset:\n {df.head(5)}")

    return df

def clean_data(df):
    print("=====================Cleaning data======================")
    print("====================Loại bỏ data trùng lặp==============")
    df.drop_duplicates(inplace=True)

    print("=====Xử lí dữ liệu không nhất quán và sai chính tả======")
    df_column_dtype = ['AQI index', 'CO', 'NO2', 'O3', 'SO2', 'Dew', 'Humidity', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']
    result = []
    for column in df_column_dtype:
        if df[column].dtype == 'object':
            unique_non_numeric_chars = df[column].str.extract('([^0-9])').drop_duplicates()
        else:
            unique_non_numeric_chars = df[column].astype(str).str.extract('([^0-9])').drop_duplicates()
        temp = unique_non_numeric_chars[0].tolist()
        for i in temp:
            if i not in result:
                result.append(i)
    print(f"Những kí tự đặc biệt trong các cột có kiểu dữ liệu số: {result}")
    df_column_dtype = ['AQI index', 'CO', 'NO2', 'O3', 'SO2', 'Dew', 'Humidity', 'Pressure', 'PM10', 'PM2.5', 'Temperature', 'Wind']
    for i in df_column_dtype:
        df[i] = df[i].replace(result, 0)
        df[i] = df[i].fillna(0)
    # Xử lý dữ liệu sai chính tả, chuyển đổi về dạng số
    for column in df_column_dtype:
        if df[column].dtype == 'object':
            df[column] = df[column].str.replace(',', '', regex=True).astype(float)

    df['Data Time S'] = pd.to_datetime(df['Data Time S'])
    df['Date'] = df['Data Time S'].dt.date
    df['Time'] = df['Data Time S'].dt.time

    for column in df_column_dtype:
        df[column] = df[column].astype(float)
        df = df.fillna(0)
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    mean_value = df.groupby('Month')[df_column_dtype].mean()
    for i in range(1, 12):
        for j in df_column_dtype:
            df[j] = df[j].where(df['Month'] == i, df[j].replace(0, mean_value[j].values[i - 1]))
    
    # Điền khuyết cho các cột dữ liệu dạng string
    def dominant_pollutant(row):
        if row['PM10'] > row['PM2.5']:
            return 'pm10'
        elif row['PM10'] < row['PM2.5']:
            return 'pm25'
        else:
            return 'aqi'
    df['Dominent pollutant'] = df.apply(dominant_pollutant, axis=1)
    df.drop(['Date', 'Time'], axis=1, inplace=True)

    def myfunc(x):
        if x <= 50:
            return 1, "Good"
        elif x <= 100:
            return 2, "Moderate"
        elif x <= 150:
            return 3, "Unhealthy for Sensitive Group"
        elif x <= 200:
            return 4, "Unhealthy"
        elif x <= 300:
            return 5, "Very Unhealthy"
        else:
            return 6, "Hazardous"
    df['Alert level'], df['Status'] = zip(*df['AQI index'].apply(myfunc))
    
    return df, df_column_dtype

def transform_data(df, df_column_dtype):
    print("====================Transforming data===================")
    print("====================Normalizing data====================")
    df = df[df['SO2']<df['SO2'].quantile(0.9)]
    return df

def main(df_input):
    df = pd.read_csv(df_input)
    df_summarized = summarization_data(df)
    df_cleaned, df_column_dtype = clean_data(df_summarized)
    latest_df = transform_data(df_cleaned, df_column_dtype)
    latest_df.to_csv("data\\result\\pre-process-data.csv")
    print("========================Describe========================")
    print(latest_df.describe())
    latest_df.describe().to_csv("data\\result\\DATA_SUMMARIZATION_0.csv")
if __name__ == "__main__":
    main("data\\input\\historical_air_quality_2021_en.csv")