from oauthlib.oauth2.rfc6749.clients import base
from sheets import SheetsService
import pandas as pd
import re
import requests
import numpy as np

from settings import RAW_DATA_URL, ONEMAP_URL, CORRECTIONS_WORKSHEET_NAME, PLANNING_AREA_WORKSHEET_NAME, MAIN_WORKSHEET_NAME

main_df = pd.read_excel(RAW_DATA_URL)
request_url = ONEMAP_URL
sheets = SheetsService()

# retrieve required data from google sheets
address_changes = sheets.getWorksheet(CORRECTIONS_WORKSHEET_NAME)\
    .get_as_df()\
    .set_index('Raw')\
    .to_dict()['Corrected']
planning_area_df = sheets.getWorksheet(PLANNING_AREA_WORKSHEET_NAME).get_as_df()

baseline = planning_area_df.iloc[0]

def main():
    main_wks = sheets.getWorksheet(MAIN_WORKSHEET_NAME)

    # get geocodes
    for index, row in main_df.iterrows():
        result = re.search('(?s:.*)\((.*?)\)', row['Location'])
        location = result.group(1) if result else location
        location = address_changes.get(location) if location in address_changes else location
        
        # call request
        response = requests.get(request_url, params={
            'searchVal': location,
            'returnGeom': 'Y',
            'getAddrDetails': 'Y'
        })
        print('{}: {}'.format(index, location))
        result = response.json()['results'][0]
        main_df.at[index,'Longitude']=result['LONGITUDE']
        main_df.at[index,'Latitude']=result['LATITUDE']
        main_df.at[index,'Postal']=result['POSTAL']
    
    for index, row in main_df.iterrows():
        main_df.at[index,'Area']= find_place(row['Longitude'], row['Latitude'])

    main_wks.set_dataframe(main_df,(1,1))

def find_place(lng, lat):
    result = baseline['Area']
    
    baseline_a = np.array((float(baseline['Longitude']), float(baseline['Latitude'])))
    b = np.array((float(lng), float(lat)))

    minimum_distance = np.linalg.norm(baseline_a-b)
        
    for index, row in planning_area_df.iterrows():
        a = np.array((float(row['Longitude']), float(row['Latitude'])))
        distance = np.linalg.norm(a-b)
        if distance < minimum_distance:
            minimum_distance = distance
            result = row['Area']
        
    return result

if __name__ == '__main__':
    main()