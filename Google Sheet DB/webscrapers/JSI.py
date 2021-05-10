import requests
from bs4 import BeautifulSoup as bs
import re

import pandas as pd

def run():
    url = 'https://careers.jsi.com/JSIInternet/Careers/jobpostings.cfm'

    with requests.Session() as s:
        r = s.get(url)
        src = r.content
        soup = bs(src, features = "lxml")
        soup.prettify()

        allPages = []
        data = soup.find_all('li', class_ = 'opensquare opensquare-link-list-item')
        for link in data:
            url = link.find('a')
            if url not in allPages:
                allPages.append(url.get('href'))

        page_url = []
        job_position = []
        location = []
        description = []
        requirements = []
        des_and_req = []
        ImmEcs = []
        organization = []

        root_url= 'https://careers.jsi.com'

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
                if (imm_result and ec_result): ImmEcs.append('Both')
                elif imm_result: ImmEcs.append('Immunization')
                else: ImmEcs.append('Economics')

                page_url.append(root_url + page)

                job_position_data = soup.find('div', id = 'job-description-container')
                h3 = job_position_data.find('h3')
                job_position.append(h3.getText())

                des_res_data = soup.find_all('div',attrs={'style':'margin-top:5px;margin-bottom:15px;text-align:left;'})
                for data in des_res_data:
                    desres = str(des_res_data)
                    start1 = desres.find('[<div style="margin-top:5px;margin-bottom:15px;text-align:left;">') + len('[<div style="margin-top:5px;margin-bottom:15px;text-align:left;">')
                    end1 = desres.find('</div>, <div style="margin-top:5px;margin-bottom:15px;text-align:left;"')
                    text1 = desres[start1:end1]
                    text1 = re.sub('<\S*>', '', text1)
                    text1 = re.sub('<a href="\S*">', '', text1)
                    if text1 not in description:
                        description.append(text1)
                    start2 = desres.find('</div>, <div style="margin-top:5px;margin-bottom:15px;text-align:left;">1.') + len('</div>, <div style="margin-top:5px;margin-bottom:15px;text-align:left;">1.')
                    end2 = desres.find('</div>]')
                    text2 = desres[start2:end2]
                    text2 = re.sub('<\S*>', '', text2)
                    text2 = re.sub('<div style="\S*">', '', text2)
                    text2 = re.sub('<a href="\S*">', '', text2)
                    if text2 not in requirements:
                        requirements.append(text2)

                des_and_req.append(text1+text2)

                location_data = soup.find_all('div', id = 'job-description-container')
                for data in location_data:
                    p = data.find('p')
                    if p.find('strong'=='Location:'):
                        text = p.text
                        text = text[10:]
                        location.append(text)

                organization.append('JSI')

    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['ImmEcs'] = ImmEcs
    DataFrame['Description and Requirements'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    return Data

    #Data.to_csv("JSI_Data.csv")
