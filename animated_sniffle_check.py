'''
@Created: on Nov 12, 2020
@author: jesmin.aktar
@resource: https://animated-sniffle.pagerinc.com/docs#/default/list_application_versions_api_v1_appversions_get
@url: 'https://animated-sniffle.pagerinc.com/api/v1/appversions'

@requirement: Ask user for environment name and create a new sheet.
1- provide input for environment name & put data in a list
2- provide input for app names
3- write exception if app name & version is missing from an environment [raise ValueError("arrays must all be same length"]
4- app list might not match in all env. i.e boradcast doen't apply to pgr-rr
'''
import subprocess
import json
import xlsxwriter
import pandas as pd
from google_auth_oauthlib import flow


appflow = flow.InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"])
appflow.run_local_server()
token = appflow.credentials.id_token

curl_cmd= 'curl https://animated-sniffle.pagerinc.com/api/v1/appversions -H "Authorization: Bearer {0}"'.format(token)

token_data = subprocess.check_output(curl_cmd, shell=True).decode('UTF-8')
data = json.loads(token_data)

#env_name = 'hrz-prod' #input('enter your environment name: ')

def get_env_data(env_name, data):
    env_data = []
    for i in data:
        if i['environment'] == env_name:  
            env_data=i['data'] 
    return env_data             

env_name = ['hrz-prod', 'pgr-prod', 'cox-prod']
def get_env_data2(env_name, data):
    env_data = []
    env_dict = {}
    for i in data:
        if i['environment'] in env_name:  
            env_data.append(i['data']) 
            env_dict = dict.fromkeys(env_name, env_data)
    return env_dict

def get_app_versions(app_list, env_data):
    versions = []  
    for i in env_data:
        if i['app'] in app_list:
            versions.append(i['image_version']) 
    return versions        
   
    
def write_to_xl(workbook_name, sheet_name, list1, list2):  
    #create three DataFrames
    df1 = pd.DataFrame({'App' : list1, 'Version' : list2 })
    df2 = pd.DataFrame({'dataset': ['Dani', 'Chris', 'Archana']})
    df3 = pd.DataFrame({'dataset': [3, 6, 6]})
    
    #create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(workbook_name+'.xlsx', engine='xlsxwriter')
    
    #write each DataFrame to a specific sheet
    df1.to_excel(writer, sheet_name=env_name)
    df2.to_excel(writer, sheet_name= 'hrz')
    df3.to_excel(writer, sheet_name= 'pgr')
        
    writer.save()             
        
''' variables '''
#env_name = input('enter your environment name: ')
env_name = 'hrz-prod'
workbook_name = "pandas_column_formats"
#apps = input('enter your app/service name: ')
my_apps = ['socker', 'faro','enterprise-admin', 'edge-api-cc'] 

env_data = get_env_data(env_name, data)
versions = get_app_versions(my_apps, env_data)
write_to_xl(workbook_name, env_name, my_apps, versions)

#write_to_xl(workbook_name, 'pgr-dev', my_apps, versions)

    



env_dict = get_env_data2(env_name, data)

def get_value_from_env_dict(env_dict):
    for i in env_dict.values():
        return i


env_data = get_value_from_env_dict(env_dict)

# def get_app_versions2(my_apps, env_data):
# versions = []  
# for i in env_data:
#     if i['app'] in my_apps:
#         versions = versions.append(i['image_version']) 
#     return versions 


myList = set(['apple', 'banana'])
lst = [['apple', 'orange','banana'], ['banana', 'kiwi', 'apple'], ['apple', 'cherry','banana']]
counter=0
for i in lst:
    s = set(i)
    s.intersection(myList)
    


#apps = input('enter your app/service name: ')
#apps = ['socker', 'faro','enterprise-admin', 'edge-api-cc']
# versions = []
# for i in env_data:
#     if i['app'] in apps:
#         versions.append(i['image_version'])
        
# # Store data to write to excel   
# to_xl = list(map(list, zip(apps, versions)))
# col_header = [{'header': env_name},
#               {'header': 'app'}, 
#               {'header': 'version'}]
#                    
# # Create a workbook, add a worksheet, add a table & close the workbook.
# workbook = xlsxwriter.Workbook('versions.xlsx')
# worksheet = workbook.add_worksheet(env_name)
# worksheet.add_table('B1:D1', {'data':to_xl})
# #worksheet.add_table('A1:D1', {'data':to_xl, 'columns':col_header})
# workbook.close()







