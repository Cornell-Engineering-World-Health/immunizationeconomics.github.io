import webscrapers.CDC
import webscrapers.JSI
import webscrapers.JohnsHopkins
import webscrapers.R4D
import webscrapers.Sabin
import webscrapers.Thinkwell
import webscrapers.UNICEF
import webscrapers.BMFG
import webscrapers.MSH
import webscrapers.GAVI
import gsheets

webscrapers = [CDC,JSI,JohnsHopkins,R4D,Sabin,Thinkwell,UNICEF,BMFG,MSH,GAVI]

def run(webscrapers):

    worksheet = gsheets.init()
    for webscraper in webscrapers:
        df = webscraper.run()
        gsheets.writetosheets(df,worksheet)

run([CDC,JSI,JohnsHopkins,R4D,Sabin,Thinkwell,UNICEF,BMFG,MSH,GAVI])
#