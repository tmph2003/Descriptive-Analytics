import pre_processing_data as pref
import pandas as pd

df = pd.read_csv("historical_air_quality_2021_en.csv")
df_summarized = pref.summarization_data(df)
df_cleaned, df_column_dtype = pref.clean_data(df_summarized)
latest_df = pref.transform_data(df_cleaned, df_column_dtype)
latest_df.describe()