import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs
import re

import pandas as pd

url = 'https://jobs.lever.co/r4d'

def run():
    with requests.Session() as s:
        r = s.get(url)
        src = r.content
        soup = bs(src, features = "lxml")
        soup.prettify()
        #print(soup)

        allPages = []
        links = soup.find_all('a',class_ = 'posting-title')
        #print(links)
        for link in links:
            if link not in allPages:
                allPages.append(link.get('href'))
        #print(allPages)

        page_url = []
        job_position = []
        location = []
        des_and_req = []
        ImmEcs = []
        organization = []

        for page in allPages:
            result = s.get(page)
            page_source = result.content
            soup = bs(page_source, features = "lxml")
            soup.prettify()

            for script in soup(['script','style']):
                script.decompose()
            strips = list(soup.stripped_strings)
            strips = str(strips)
            #print(strips)

            immunization = ['Immunization', 'immunisation', 'vaccine', 'vaccines','vaccine-preventable diseases', 'vpd outbreak',
                'immunization campaign', 'SIA','supplemental immunization act ivities', 'cold chain', 'GAVI','shigella', 'cholera',
                'bcg', 'dtp', 'dpt', 'measles', 'influenza', 'conjugate vaccine']

            economics = ['Economics','expenditure tracking', 'financing',
                'value for vaccination' , 'costing', 'economic analysis','costs' , 'equity', 'cost effectiveness', 'cost-effectiveness',
                'cost benefit analysis', 'benefit-cost analysis','cost utility analysis','budget impact analysis' , 'budget' , 'budgeting' ,
                'GAVI','funding gap','fiscal']

            #checking for Immunization and Economic key words
            imm_result = any(ele in strips for ele in immunization)
            ec_result = any(ele in strips for ele in economics)

            if imm_result or ec_result:
                if (imm_result and ec_result): ImmEcs.append('Both')
                elif imm_result: ImmEcs.append('Immunization')
                else: ImmEcs.append('Economics')

                page_url.append(page)

                loc_data = soup.find('div', class_='sort-by-time posting-category medium-category-label')
                loc_text = loc_data.getText()
                loc_text = re.sub('/', '', loc_text)
                loc_text = re.sub('Remote - ','',loc_text)
                location.append(loc_text)
                #print(location)

                job_pos = soup.find('div', class_ = 'posting-headline')
                h2 = job_pos.find('h2')
                job_position.append(h2.getText())
                #print(job_position)

                big_text = soup.find('div', class_ = 'section page-centered')
                text = big_text.getText()
                string = str(text)
                #print(string)
                start = string.find('Opportunity') + len('Opportunity ')
                end = string.find('Responsibilities')
                opportunity = string[start:end]
                des_and_req.append(opportunity )
                #print(des_and_req)

                organization.append('R4D')


    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    return Data
    #Data.to_csv("R4D_Data.csv")
