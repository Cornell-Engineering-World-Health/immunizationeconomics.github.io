import pygsheets
import pandas as pd

#authorization
gc = pygsheets.authorize(service_file='./credentials.json')

# Create empty dataframe, this will be what you are updating your google sheet with
df = pd.DataFrame()

# Create a column, I assume you know how to use pandas so just set the df to what you want
df['Timestamps'] = ["time 1" , "time 2"]
df['Page Url'] = ["link 1", "link 2"]
df['Job'] = ["job 1", "job2"]
df["Location"] = ["location 1", "location 2"]
df["Type"] = ["econmoics","immunization"]
df["Description"] = ["description 1", "description 2"]

#convert dataframe to a list without the headers!
df_matrix = df.values.tolist()

"""
open the google spreadsheet by key

look at a google sheet URL
Example: https://docs.google.com/spreadsheets/d/1o_o4vil2VPIjO_XEECPz9yz3IAImEd8R1l9GQZkEeUY/edit#gid=0

The variable below "spreadsheet" is of type Spreadsheet, docs located here: https://pygsheets.readthedocs.io/en/staging/spreadsheet.html
"""
spreadsheet = gc.open_by_key('1o_o4vil2VPIjO_XEECPz9yz3IAImEd8R1l9GQZkEeUY')

worksheet = spreadsheet.sheet1 #get the FIRST sheet, which is where all our stuff is, this is of type Worksheet

# append to the worksheet your dataframe (overwrite=false means it will add new rows every time you insert)
worksheet.append_table(df_matrix, start='A1', dimension="ROWS", end=None, overwrite=False)
