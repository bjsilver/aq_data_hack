#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:23:30 2024

@author: eebjs
"""

import pandas as pd
import time
import requests
from requests.adapters import HTTPAdapter, Retry

def response_to_dataframe(response, index='id'):
    df = pd.json_normalize(response.dict()['results'])
    df = df.set_index(index)
    return df

# we can use this function to download the entire list of stations
# it will take some time!
def download_all_pages(request, index='id', **kwargs):

    more_results = True
    page_num = 1
    limit = 1000
    dfs = []
    retries = 1
        
    # we keep adding one to the page number and downloading the results until none are returned
    while more_results:

        start_time = time.time()
        
        try:
            locations_response = request(limit=limit, page=page_num, **kwargs)
        except Exception as e:
            print('getting', e, 'exception')
            print(f'wating {2**retries} seconds and retrying')
            retries += 1
            time.sleep(2**retries)
            continue
        
        
        if len(locations_response.results) == 0:
            more_results = False
        else:
            dfs.append(response_to_dataframe(locations_response, index=index))
            retries = 1
    
            # print(page_num, end='...')
            page_num += 1
            print('.', end='')

        end_time = time.time()

        # ensuring each iteration of the loop takes at least one second so we won't exceed API limits
        iteration_time = end_time - start_time
        # print('iteration time:', iteration_time)
        if iteration_time < 1.1:
            # print('waiting', 1.1 - iteration_time)
            time.sleep(1.1 - iteration_time)
            
    
    # merge all the DataFrames together
    if len(dfs) > 0:
        df = pd.concat(dfs)
        return df


def download_measurement_portion(locations_id, date_from, date_to, parameters_id,
                              client):
    
    request = client.measurements.list

    df = download_all_pages(request, index='period.datetime_from.utc',
                       locations_id=locations_id, date_from=date_from, date_to=date_to, 
                       parameters_id=parameters_id)
        
    
    return df


# def download_all_measurements(location_id=)


#%%

def download_measurement_data(locations_id, date_from, date_to,
                              parameters_id, client):

    dindex = pd.date_range(date_from, date_to)
    years = dindex.year.unique()
    
    dfs = []
    for param in parameters_id:
        print('downloading data for parameter id:', param)
    
        for year in years:
            
            
            portion = download_measurement_portion(locations_id=locations_id, 
                                      date_from=f'{year}-01-01',
                                      date_to=f'{year}-12-31', 
                                      parameters_id=param,
                                      client=client)
            
            print('year:', year, 'downloaded')
            
            if portion is not None:
                dfs.append(portion)
    if len(dfs) > 0:
        df = pd.concat(dfs)
        df.index.name = 'datetime'
        df.index= pd.to_datetime(df.index)
        df = df[['value','parameter.name']]
        df = df.reset_index().set_index(['datetime', 'parameter.name']).squeeze().unstack('parameter.name')
        
        return df

#%%



# def download_location_data(location_metadata, api_key):
    
#     # replace start and end with strings
#     #start = str(start.date())
#     #end = str(end.date())
    
#     limit = 1000
#     page = 1
#     remaining_data = True
    
    
#     dfs = []
        
#     # we keep adding one to the page number and downloading the results until none are returned
#     while remaining_data:
#         print(page)
    
#         start_time = time.time()
    
#         url = ("https://api.openaq.org/v2/measurements?"
#            f"date_from={location_metadata['datetime_first.utc']}T00%3A00%3A00%2B00%3A00&"
#            f"date_to={location_metadata['datetime_last.utc']}T00%3A10%3A00%2B00%3A00&"
#            f"limit={limit}&page={page}&"
#            "offset=0&sort=desc&"
#            #"parameter=2&"
#            #"radius=1000&"
#            f"location_id={location_metadata.name}&"
#            "order_by=datetime")
#         headers = {"accept": "application/json",
#                   "X-API-Key": api_key}
        
#         s = requests.Session()
#         retries = Retry(total=10, backoff_factor=5, status_forcelist=[408, 429, 500, 502, 503, 504])
#         s.mount('http://', HTTPAdapter(max_retries=retries))
#         response = s.get(url, headers=headers)
#         #print('response:'+str(response.status_code))
    
        
#         if 'results' in response.json():
#             df = pd.json_normalize(response.json()['results'])
#             dfs.append(df)
#         else:
#             remaining_data = False
    
#         page += 1
    
#         # ensuring each iteration of the loop takes at least 1.1 seconds so we won't exceed API limits
#         end_time = time.time()
#         iteration_time = end_time - start_time
#         print(iteration_time)
#         if iteration_time < 1:
#             time.sleep(1.1 - iteration_time)

#     df = pd.concat(dfs)
#     df['date.utc'] = pd.to_datetime(df['date.utc'])
#     df = df[['value','parameter', 'date.utc']]
#     df = df.set_index(['date.utc', 'parameter']).squeeze().unstack('parameter')

#     return df

    