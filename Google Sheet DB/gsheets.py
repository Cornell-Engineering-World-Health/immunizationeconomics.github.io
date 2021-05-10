import pygsheets
import pandas as pd
from datetime import datetime as dt

def init():
    #authorization
    gc = pygsheets.authorize(service_file='./credentials.json')

    spreadsheet = gc.open_by_key('1o_o4vil2VPIjO_XEECPz9yz3IAImEd8R1l9GQZkEeUY')

    worksheet = spreadsheet[1] #get the second sheet, which is where all our stuff is, this is of type Worksheet

    worksheet.clear(start='A2')

    return worksheet

def writetosheets(webscraper, worksheet):

    webscraper.insert(0,'Timestamp', str(dt.now()))
    #convert dataframe to a list without the headers!
    df_matrix = webscraper.values.tolist()

    # append to the worksheet your dataframe (overwrite=false means it will add new rows every time you insert)
    worksheet.append_table(df_matrix, start='A1', dimension="ROWS", end=None, overwrite=False)

def 