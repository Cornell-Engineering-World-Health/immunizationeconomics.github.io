import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re

import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def run():
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = 'https://www.gavi.org/work-with-us/vacancies'
    browser.get(url)

    iframe = browser.find_element_by_xpath("//iframe[@src='/iframes/careers/']");
    browser.switch_to.frame(iframe)

    iframe2 = browser.find_element_by_xpath("//iframe[@src='https://gavialliancecareers.secure.force.com/recruit/fRecruit__ApplyJobList?portal=Global']");
    iframe2Url = iframe2.get_attribute("src")
    browser.switch_to.frame(iframe2);


    with requests.Session() as s:
        r = s.get(iframe2Url)
        src = r.content
        soup = bs(src, features = "lxml")
        soup.prettify()

        rootUrl = "https://gavialliancecareers.secure.force.com"

        pageUrl = []
        jobPosition = []
        location = []
        description = []
        requirements = []
        des_and_req = []
        ImmEcs = []
        organization = []

        allLinks = []
        allJobNames = []
        allLocations = []

        table = soup.find("table").find("tbody").find_all("tr")

        nameLinkList = []
        for data in table:
            allTd = data.find_all("td")
            nameLinkList.append(allTd[1])
            allLocations.append(allTd[2].text)

        for nameLink in nameLinkList:
            name = nameLink.find('a').text
            allJobNames.append(name)

            link = nameLink.find('a')['href']
            completeUrl = rootUrl + link
            allLinks.append(completeUrl)


        jobIndex = 0
        for page in allLinks:
            result = s.get(page)
            pageSource = result.content
            soup = bs(pageSource, features = "lxml")
            soup.prettify()

            for script in soup(['script','style']):
                script.decompose()
            strips = list(soup.stripped_strings)
            strips = str(strips)


            leftColTable = soup.find("table").find("table", class_ = 'detailList').find_all("label")
            rightColTable = soup.find("table").find_all("table", class_ = 'htmlDetailElementTable')

            headingColList = []
            descrAndReqRowNum = 7
            for heading in leftColTable:
                name = heading.text.replace("\n", "")
                headingColList.append(name)
            headingColList = headingColList[descrAndReqRowNum:]


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

                localTableIndex = 0
                descriptionString = ""
                requirementsString = ""
                jobString = ""
                for jobData in rightColTable:
                    jobInfo = jobData.find('div')
                    jobString += str(jobInfo)
                    if "<li>" in jobString:
                        jobInfo = jobData.find('div').getText(separator="\n").replace(".\n", ".\n\n").replace("\n\n\n", "\n").replace(" \n"," ").replace("\n ", " ")
                    else: jobInfo = jobData.find('div').getText(separator="\n")

                    if localTableIndex <= 1: # if data is a description
                        descriptionString = descriptionString + "\n" + headingColList[localTableIndex] + "\n" + jobInfo + "\n"
                    else: # if data is a requirement
                        requirementsString = requirementsString + "\n" + headingColList[localTableIndex] + "\n" + jobInfo + "\n"
                    localTableIndex += 1

                description.append(descriptionString)
                requirements.append(requirementsString)

                des_and_req.append(descriptionString+requirementsString)


                pageUrl.append(page)
                jobPosition.append(allJobNames[jobIndex])
                location.append(allLocations[jobIndex])
                organization.append('GAVI')

            jobIndex += 1


    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= pageUrl
    DataFrame['Job']= jobPosition
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    #Data.to_csv("GAVI_Data.csv")
    return Data

    browser.quit()
