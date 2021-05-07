import pygsheets

def init():
    #authorization
    gc = pygsheets.authorize(service_file='./credentials.json')

    spreadsheet = gc.open_by_key('1o_o4vil2VPIjO_XEECPz9yz3IAImEd8R1l9GQZkEeUY')

    worksheet = spreadsheet[1] #get the second sheet, which is where all our stuff is, this is of type Worksheet

    worksheet.clear(start='A2')

    return worksheet
