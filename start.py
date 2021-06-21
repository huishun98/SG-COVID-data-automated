import pandas as pd
import re
import requests
import numpy as np
from dotenv import load_dotenv
from service.sheets import SheetsService
import datetime

from settings import RAW_DATA_URL, ONEMAP_URL, CORRECTIONS_WORKSHEET_NAME, PLANNING_AREA_WORKSHEET_NAME, MAIN_WORKSHEET_NAME

load_dotenv()

# retrieve required data from google sheets
sheets = SheetsService()
address_changes = sheets.getWorksheet(CORRECTIONS_WORKSHEET_NAME).get_as_df().set_index('Raw').to_dict()['Corrected']
planning_area_df = sheets.getWorksheet(PLANNING_AREA_WORKSHEET_NAME).get_as_df()

# set global variables
main_df = pd.read_excel(RAW_DATA_URL)
baseline = planning_area_df.iloc[0]

# data processing
def processing():
    main_wks = sheets.getWorksheet(MAIN_WORKSHEET_NAME)
    old_data = main_wks.get_as_df()

    # end if no change in data
    # if len(old_data.index) == len(main_df.index):
    #     print('Code is not run because there is no change in data.')
    #     return
    
    # get start date of interest
    now = datetime.datetime.today()
    days_offset = datetime.timedelta(days = 14)
    start_date = str((now - days_offset).date())

    # keep unchanged old data
    result_df = old_data[old_data['Date'] < start_date]
    volatile_data_df = main_df[main_df['Date'] >= start_date]
    result_df = pd.concat([volatile_data_df, result_df], ignore_index=True) # append above

    # get geocodes
    for index, row in volatile_data_df.iterrows():
        result = re.search('(?s:.*)\((.*?)\)', row['Location'])
        location = result.group(1) if result else location
        location = address_changes.get(location) if location in address_changes else location
        
        # call request
        response = requests.get(ONEMAP_URL, params={
            'searchVal': location,
            'returnGeom': 'Y',
            'getAddrDetails': 'Y'
        })
        print('{}: {}'.format(index, location))
        result = response.json()['results'][0]
        result_df.at[index,'Longitude']=result['LONGITUDE'] # row index in result_df should correspond to row index in volatile_data_df
        result_df.at[index,'Latitude']=result['LATITUDE']
        result_df.at[index,'Postal']=result['POSTAL']
        result_df.at[index,'Area']= find_place(result['LONGITUDE'], result['LATITUDE'])

    main_wks.set_dataframe(result_df,(1,1))

# define helper function
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
    processing()