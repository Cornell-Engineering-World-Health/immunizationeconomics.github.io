import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

url = 'https://jobs.hopkinsmedicine.org/jobs'

def run():
    with requests.Session() as s:
        r = s.get(url)
        src = r.content
        soup = bs(src, features="lxml")
        soup.prettify()

        pagination = soup.find_all('a', class_ = 'page')
        last = int(pagination[-1].getText())

        allPages = []
        for job_page in range(last):
            r = s.get(url + '?page_jobs=' + str(job_page + 1))
            src = r.content
            soup = bs(src, features = "lxml")
            soup.prettify()

            data = soup.find_all('div', class_ = 'job')
            for link in data:
                job_url = link.find('a')
                if job_url not in allPages:
                    allPages.append(job_url.get('href'))

        page_url = []
        job_position = []
        des_and_req = []
        location = []
        ImmEcs = []
        organization = []

        root_url= 'https://jobs.hopkinsmedicine.org'
        count = 0
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

            job_data = soup.find('div',{'class':'job-details-content'})
            if job_data.find('div') == None:
                count += 1
                continue
            div = list(job_data.find('div'))

            if imm_result or ec_result:
                if (imm_result and ec_result): ImmEcs.append('Both')
                elif imm_result: ImmEcs.append('Immunization')
                else: ImmEcs.append('Economics')

                page_url.append(root_url + page)

                h1 = job_data.find('h1')
                job_position.append(h1.getText())

                text = ''
                for tag in div:
                    if tag == ' ':
                        continue
                    text += tag.getText() + '\n'
                des_and_req.append(text)

                location_data = soup.find('body')
                string = location_data.getText()
                start = string.find('Location: ') + len('Location: ')
                end = string.find('Category: ')
                loc = string[start:end]
                loc = loc.replace('\n','')
                result = ''.join([i for i in loc if not i.isdigit()])
                location.append(result)

                organization.append('Johns Hopkins')

    DataFrame = pd.DataFrame()
    DataFrame['Page Url']= page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = des_and_req
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    return Data
    #Data.to_csv("JohnsHopkins_Data.csv")
