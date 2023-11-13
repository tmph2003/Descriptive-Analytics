import pre_processing_data as pref
import build_chart as bch

def main():
    pref.main("data\\input\\historical_air_quality_2021_en.csv")
    bch.main("data\\result\\pre-process-data.csv")
    return

if __name__ == "__main__":
    main()