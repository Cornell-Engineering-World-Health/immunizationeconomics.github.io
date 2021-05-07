import pygsheets
import pandas as pd
from datetime import datetime as dt

def writetosheets(webscraper, worksheet):

    webscraper.insert(0,'Timestamp', str(dt.now()))
    #convert dataframe to a list without the headers!
    df_matrix = webscraper.values.tolist()

    # append to the worksheet your dataframe (overwrite=false means it will add new rows every time you insert)
    worksheet.append_table(df_matrix, start='A1', dimension="ROWS", end=None, overwrite=False)
