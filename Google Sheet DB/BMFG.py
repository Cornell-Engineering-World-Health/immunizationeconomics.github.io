from crawler import get_job_postings
import os, json
import pandas as pd

def run():
    data = get_job_postings('https://gatesfoundation.wd1.myworkdayjobs.com/Gates',4,False)

    immunization_keywords = ['Immunization', 'immunisation', 'vaccine', 'vaccines','vaccine-preventable diseases', 'vpd outbreak',
                            'immunization campaign', 'SIA','supplemental immunization act ivities', 'cold chain', 'GAVI','shigella', 'cholera',
                            'bcg', 'dtp', 'dpt', 'measles', 'influenza', 'conjugate vaccine']

    economics_keywords = ['Economics','expenditure tracking', 'financing',
                        'value for vaccination' , 'costing', 'economic analysis','costs' , 'equity', 'cost effectiveness', 'cost-effectiveness',
                        'cost benefit analysis', 'benefit-cost analysis','cost utility analysis','budget impact analysis' , 'budget' , 'budgeting' ,
                        'GAVI','funding gap','fiscal']


    new_json_files = []
    for json_text in data:
        desc = json_text['description']
        imm_result = any(ele in desc for ele in immunization_keywords)
        ec_result = any(ele in desc for ele in economics_keywords)
        if (imm_result or ec_result):
            if json_text not in new_json_files:
                json_text['immunization'] = imm_result
                json_text['economics'] = ec_result
                new_json_files.append(json_text)


    page_url = []
    job_position = []
    location = []
    description_and_requirements = []
    ImmEcs = []
    organization = []

    for index in new_json_files:
        jp = index['labels'][0]
        job_position.append(jp)
        description = index['description']
        description_and_requirements.append(description)
        loc = index['labels'][2]
        location.append(loc)
        if (imm_result and ec_result): ImmEcs.append('Both')
        elif imm_result: ImmEcs.append('Immunization')
        else: ImmEcs.append('Economics')
        organization.append('BMFG')
        page_url.append('https://gatesfoundation.wd1.myworkdayjobs.com/Gates')


    DataFrame = pd.DataFrame()
    DataFrame['Page Url'] = page_url
    DataFrame['Job']= job_position
    DataFrame['Location'] = location
    DataFrame['Type'] = ImmEcs
    DataFrame['Description'] = description_and_requirements
    DataFrame['Organization'] = organization

    Data = DataFrame.drop_duplicates()
    #Data.to_csv("BMGF_Data.csv")
    return Data
