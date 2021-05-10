import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

main_url = 'https://jobs.cdc.gov/search-jobs'

def clean(s):
  return re.sub('[^A-Za-z0-9 /-]+', '', s)

def run():
    with requests.Session() as s:
        r = s.get(main_url)
        src = r.content
        soup = bs(src, features="lxml")
        soup.prettify()

        allPages = []
        data = soup.find_all('a', class_ = 'locationclick')
        for link in data:
            url = link.get('href')
            if url not in allPages:
                allPages.append(url)

        page_url = []
        job_position = []
        location = []
        organization = []
        des_and_req = []
        ImmEcs = []

        root_url= 'https://jobs.cdc.gov'

        for page in allPages:
            result = s.get(root_url + page)
            page_source = result.content
            soup = bs(page_source, features="lxml")
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

                if (root_url+page)=='https://jobs.cdc.gov/':
                    page_url = page_url
                else:
                    page_url.append(root_url+page)

                job_data = soup.find_all('main', id = 'content')
                for data in job_data:
                    div = data.find('div', class_ = 'wrapper-small')
                    section = div.find('section', class_ = 'job-description')
                    h1 = section.find('h1')
                    string = str(h1)
                    start = string.find('<h1>') + len('<h1>')
                    end = string.find('</h1>')
                    job = string[start:end]
                    job_position.append(job)

                desreq_data = soup.find_all('main', id = 'content')
                for data in desreq_data:
                    div = data.find('div', class_ = 'wrapper-small')
                    section = div.find('section', class_ = 'job-description')
                    div1 = section.find('div', class_ = 'ats-description')
                    div2 = str(div1)
                    start = div2.find('JOB SUMMARY: </b><br/>') + len('JOB SUMMARY: </b><br/>')
                    end = div2.find(']<br/><br/><b>REQUIREMENTS:')
                    text = div2[start:end]
                    text.replace('<br/><br/><b>','')
                    des_and_req.append(text)

                location_data = soup.find_all('main', id = 'content')
                for data in location_data:
                    div = data.find('div', class_ = 'wrapper-small')
                    span = data.find('span', class_= 'job-location job-info')
                    text = span.get_text()
                    text = text[10:]
                    location.append(text)
                organization.append('CDC')

    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    return Data
    # Data.to_csv("CDC_Data.csv")
