import requests
from bs4 import BeautifulSoup as bs
import re
import html

import pandas as pd

def run():
    url = 'https://jobs.unicef.org/en-us/listing/'

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    with requests.Session() as s:
        r = s.get(url, headers = headers)
        src = r.content
        soup = bs(src, features = "lxml")
        soup.prettify

        button_count = soup.find('span', {'class':'count'})

        count = int(button_count.text) + 20
        new_url = url + "?page=1&page-items=" + str(count)

        r2 = s.get(new_url, headers=headers)
        src2 = r2.content
        soup2 = bs(src2, features = "lxml")
        soup2.prettify

        allPages = []
        data = soup2.find_all('a', {'class':'job-link'})
        for link in data:
            url = link.get('href')
            if url not in allPages:
                allPages.append(url)

        page_url = []
        job_position = []
        des_and_req = []
        location = []
        ImmEcs = []
        organization = []

        root_url= 'https://jobs.unicef.org'

        for page in allPages:
            result = s.get(root_url + page)
            page_source = result.content
            soup = bs(page_source, features = "lxml")
            soup.prettify

            for script in soup(['script','style']):
                script.decompose()
            strips = list(soup.stripped_strings)
            strips = str(strips)

            immunization = ['Immunization', 'immunisation', 'vaccine', 'vaccines','vaccine-preventable diseases', 'vpd outbreak',
                'immunization campaign', 'SIA','supplemental immunization act ivities', 'cold chain', 'GAVI','shigella', 'cholera',
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

                page_url.append(root_url + page)

                job_data = soup.find('div', id = 'job-content')
                job_position.append(job_data.h2.getText())

                description_data = soup.find('div', id = 'job-details')
                str_description_data = description_data.getText()
                des_and_req.append(str_description_data)

                location_data = soup.find('span', {'class': 'location'})
                location.append(location_data.getText())

                organization.append('UNICEF')

    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization


    Data = DataFrame.drop_duplicates()
    return Data
    #Data.to_csv("UNICEF_Data.csv")
