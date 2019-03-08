# -*- coding: utf-8 -*-
"""
Created on Tue March 5 09:52:01 2019

@author: James Moore
"""

# Import appropriate libraries
import json
import os
import sys
import pandas as pd

#specify directory
wkdir = 'NA'
csvFilename = 'NA'
numLoop = 0
while os.path.isdir(wkdir)==False or os.path.isfile(csvFilename)==False:
    #specify directory of file to convert
    wkdir = str(input('Please Specify Directory: '))     
    if os.path.isdir(wkdir)==False:
        print('Invalid Directory Specified:\n')
        numLoop = numLoop+1
    #specify name of file to convert
    else:
        os.chdir(wkdir)
        csvFilename = str(input('Please Specify File Name: '))
        
        #Check if the user does not enter a .csv specification
        if csvFilename[-4:] != '.csv':
            csvFilename = csvFilename+'.csv'
        
        #check if file exists
        if os.path.isfile(csvFilename)==False:
            print('\nInvalid Input:\n' \
                  'The file entered does not exist in the specified directory.\n' \
                  'Please Check Directory and File Specifications and Try Again.\n')
            numLoop = numLoop+1
    
    #terminate after 3 failed attempts to find existing file        
    if numLoop > 3:
        sys.exit('Too Many Failed Attempts\n' \
                 'Program Terminating...')
#%%  
#Read in .csv data using pandas
csvReader = pd.read_csv(csvFilename)

#create blank list to write to .json
callList = list()

#get unique call-ids
callID = csvReader[csvReader.columns[0]].unique()

#iterate through unique call-ids
for idKey in callID:
    #set up nested list
    nestIDList = ('call-id','start','end','users')
    idNest = dict([(key,[]) for key in nestIDList])
    
    #subset based on call-ID
    tempDat = csvReader[csvReader['call-id']==idKey]
    
    #record start and end times for the entire call
    startTime = min(tempDat[tempDat.columns[2]])
    endTime = max(tempDat[tempDat.columns[3]])
    
        #record call id, start/end time
    idNest['call-id'] = idKey
    idNest['start']=startTime
    idNest['end']=endTime
    
    #find unique users in each call and iterate through each
    user = tempDat[tempDat.columns[1]].unique()
    for userKey in user:
        #record data for specific user on call
        userRow = tempDat[tempDat['user']==userKey]
        userRow = userRow.drop('call-id',axis = 1)
        userRowList = dict(userRow.iloc[0])
        #append the existing list of users on call
        idNest['users'].append(userRowList)
    
    #update Master List    
    callList.append(idNest)
    
    
#%% 
#Write our data to .json file
jsonFilename = 'jConvert_'+csvFilename[:-4]+'.json'
with open(jsonFilename,'w') as jsonFile:
    jsonFile.write(json.dumps(callList))
  #%%  
    
    
    
    
    
    
    
    
#Write JSON file