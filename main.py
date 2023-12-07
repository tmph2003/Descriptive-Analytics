import pre_processing_data as pref
import build_chart as bch
import LinearReg as lr
import os

def main():
    pref.main("data\\input\\historical_air_quality_2021_en.csv")
    bch.main("data\\result\\pre-process-data.csv")
    lr.main()
    os.system('pause')
    
if __name__ == "__main__":
    main()