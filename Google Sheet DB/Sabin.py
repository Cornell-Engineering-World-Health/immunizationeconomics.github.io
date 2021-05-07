import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

def run():
    url = 'https://www.sabin.org/careers'

    with requests.Session() as s:
        r = s.get(url)
        src = r.content
        soup = bs(src, features = "lxml")
        soup.prettify()

        allPages = []
        data = soup.find_all('h2', {'class' : 'node__title node-title'})
        for link in data:
            url = link.find('a')
            if url not in allPages:
                allPages.append(url.get('href'))

        page_url = []
        job_position = []
        des_and_req = []
        location = []
        ImmEcs = []
        organization = []

        root_url= 'https://www.sabin.org'

        for page in allPages:
            result = s.get(root_url + page)
            page_source = result.content
            soup = bs(page_source, features = "lxml")
            soup.prettify()

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
                soup_lines = soup.find('div', class_ = 'field-item even', property = 'content:encoded')
                str_soup_lines = str(soup_lines)
                if not 'Location:' in str_soup_lines:
                    continue

                if (imm_result and ec_result): ImmEcs.append('Both')
                elif imm_result: ImmEcs.append('Immunization')
                else: ImmEcs.append('Economics')

                page_url.append(root_url + page)

                job_data = soup.find('h1',{'class':'title'})
                job_position.append(job_data.text)

                total = ''
                for tag in soup_lines:
                    if tag == ' ':
                        continue
                    total += tag.getText() + '\n'

                start_des = total.find('Responsibilities')
                end_des = total.find('Requirements')
                des = total[start_des:end_des]
                description= des.replace('\n', ' ')

                start_req = total.find('Requirements')
                end_req = total.find('How to Apply')
                req = total[start_req:end_req]
                requirements= req.replace('\n', ' ')

                both = description+requirements
                des_and_req.append(both)

                start_loc = total.find('Location:') + len('Location:')
                end_loc = total.find('Why Sabin:')
                loc = total[start_loc:end_loc]
                location.append(loc.replace('\n', ' '))

                organization.append('Sabin')

    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    #Data.to_csv("Sabin_Data.csv")
    return Data
