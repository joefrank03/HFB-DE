"""
HFB DATA ENGINEERING EXERCISE
__author__ = 'Joseph Fernandez'
"""
import requests
import json
import csv

CENSUS_API_KEY = 'API_KEY'

ANY_AGE = 'SAEPOVALL_PT'
UNDER_18 = 'SAEPOVRT0_17_PT'
MEDIAN_HOUSE_HOLD_INCOME = 'SAEMHI_PT'
REQUIRED_COUNTY_NAME = 'Harris County'

DATA_ELEMENTS_LIST = [ANY_AGE, UNDER_18, MEDIAN_HOUSE_HOLD_INCOME]

POVERTY_DATA = r'http://api.census.gov/data/timeseries/poverty/saipe?' \
               r'get=NAME,{variable}&time=2018&for=county&in=state:48&key={CENSUS_API_KEY}'

header = ['County', 'Data_Element', 'Year', 'State_Code', 'County_Code']

for i in DATA_ELEMENTS_LIST:
    # 1 BUILD URL WITH QUERY PARAMETERS
    URL = POVERTY_DATA.format(variable=i, CENSUS_API_KEY=CENSUS_API_KEY)

    # 2 GET DATA USING REQUESTS & FILTER DATA FROM RESPONSE TO GET HARRIS COUNTY
    print('\nURL: {}'.format(URL))
    response = requests.get(URL)  # GET DATA
    json_data = json.loads(response.text)  # CONVERT FROM STRING TO JSON
    print('JSON DATA: {}'.format(json_data))

    harris_county_data = []
    for data in json_data:
        if REQUIRED_COUNTY_NAME in data:  # FILTER DATA
            harris_county_data.append(data)
            break

    # 3 SAVE TO CSV WITH PROPER HEADERS
    print('Harris County Data: {}'.format(i))
    print(header)
    print(harris_county_data)
    with open('harris_county_{variable}_data.csv'.format(variable=i), 'w') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(header)
        csv_writer.writerows(harris_county_data)

"""

3 Parts

1. Build URL with Query parameters
2. Get Data using requests & Filter data from Response to get Harris County
3. Save to CSV with proper Headers


UNDER AGE 18 POVERTY
['NAME', 'SAEPOVRT0_17_PT', 'time', 'state', 'county']
['Harris County', '24.8', '2018', '48', '201']

Poverty Any Age
['NAME', 'SAEPOVALL_PT', 'time', 'state', 'county']
['Harris County', '767367', '2018', '48', '201']


Median Household income

['NAME', 'SAEMHI_PT', 'time', 'state', 'county']
['Harris County', '60241', '2018', '48', '201']
"""
