import CDC
import JSI
import JohnsHopkins
import R4D
import Sabin
import Thinkwell
import UNICEF
import BMFG
import MSH
import GAVI
from writetosheets import writetosheets
from init import init

webscrapers = [CDC,JSI,JohnsHopkins,R4D,Sabin,Thinkwell,UNICEF,BMFG,MSH,GAVI]

def run(webscrapers):

    worksheet = init()
    for webscraper in webscrapers:
        df = webscraper.run()
        writetosheets(df,worksheet)

run([CDC,JSI,JohnsHopkins,R4D,Sabin,Thinkwell,UNICEF,BMFG,MSH,GAVI])
