import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = 'https://thinkwell.global/work-for-us/our-vacancies/'
driver.get(url)

def run():
    with requests.Session() as s:
        r = s.get(url)
        src = driver.page_source
        soup = bs(src, features = "lxml")
        soup.prettify()

        rootUrl = "https://apply.workable.com/thinkwell"

        pageUrl = []
        jobPosition = []
        location = []
        des_and_req = []
        ImmEcs = []
        organization = []

        allLinks = []
        allJobNames = []

        data = soup.find_all('h3', class_='whr-title')

        for nameLink in data:
            link = nameLink.find('a')['href']
            allLinks.append(link)

            name = nameLink.find('a').text
            allJobNames.append(name)


        jobIndex = 0
        for page in allLinks:
            driver.get(page)
            pageSource = driver.page_source
            soup = bs(pageSource, features = "lxml")
            soup.prettify()

            for script in soup(['script','style']):
                script.decompose()
            strips = list(soup.stripped_strings)
            strips = str(strips)

            immunization = ['Immunization', 'immunisation', 'vaccine', 'vaccines','vaccine-preventable diseases', 'vpd outbreak',
                'immunization campaign', 'SIA','supplemental immunization activities', 'cold chain', 'GAVI','shigella', 'cholera',
                'bcg', 'dtp', 'dpt', 'measles', 'influenza', 'conjugate vaccine']

            economics = ['Economics','expenditure tracking', 'financing',
                'value for vaccination' , 'costing', 'economic analysis','costs' , 'equity', 'cost effectiveness', 'cost-effectiveness',
                'cost benefit analysis', 'benefit-cost analysis','cost utility analysis','budget impact analysis' , 'budget' , 'budgeting' ,
                'GAVI','funding gap','fiscal']

            imm_result = any(ele in strips for ele in immunization)
            ec_result = any(ele in strips for ele in economics)


            if imm_result or ec_result:
                if (imm_result and ec_result): ImmEcs.append('Both')
                elif imm_result: ImmEcs.append('Immunization')
                else: ImmEcs.append('Economics')

                descriptionString = ""
                requirementsString = ""
                desReqString = ""

                locationList = soup.find_all("p", class_="job-details-styles__details--11P0z job-styles__headerDetails--1HMvu")
                for col in locationList:
                    if "job-location" in str(col):
                        text = col.text
                        text = re.sub('HFA/USAID','', text)
                        text = re.sub('Full time','',text)
                        text = re.sub('Contracts','',text)
                        text = re.sub('SP4PHC','',text)
                        text = re.sub('Finance','',text)
                        location.append(text)
                #print(location)

                strongTextDes = ""
                descriptionCode = soup.find("div", class_="job-preview-styles__description--2BkR3")
                strongCodeDes = descriptionCode.find_all("strong")
                for strong in strongCodeDes:
                    strongTextDes = "DELETE" + strong.text + "DELETE"
                    if "YOU ARE" not in strongTextDes and "OVERVIEW" not in strongTextDes: strong.replaceWith(strongTextDes)
                descriptionString = descriptionString + descriptionCode.get_text(separator="\n").replace("      ", " ").replace("DELETE\n", "").replace("\nDELETE", "").replace("DELETE", "").replace("\n,", ",")
                desReqString = desReqString + descriptionString

                strongTextRes = ""
                requirementsCode = soup.find("div", class_="job-preview-styles__requirements--2kg4_")
                if requirementsCode != None:
                    strongCodeRes = requirementsCode.find_all("strong")
                    for strong in strongCodeRes:
                        strongTextRes = "DELETE" + strong.text + "DELETE"
                        if "YOU ARE" not in strongTextRes and "OVERVIEW" not in strongTextRes: strong.replaceWith(strongTextRes)
                    requirementsString = requirementsString + requirementsCode.get_text(separator="\n").replace("      ", " ").replace("DELETE\n", "").replace("\nDELETE", "").replace("DELETE", "").replace("\n,", ",")

                desReqString = desReqString + "\n" + requirementsString
                des_and_req.append(desReqString)

                pageUrl.append(page)
                jobPosition.append(allJobNames[jobIndex])

                organization.append('Thinkwell')

            jobIndex += 1


    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= pageUrl
    DataFrame['Job']= jobPosition
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    return Data
    #Data.to_csv("Thinkwell_Data.csv")

    driver.quit()
