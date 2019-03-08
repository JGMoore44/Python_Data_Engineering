# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 09:24:41 2019

@author: James Moore
"""
import csv
import os
import sys
import re
#%%

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
##Define Checking functions for each feature
        
#Define Function for checking ID format
def id_Checker(matchString):
    pattern = re.compile('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
    matchString = str(matchString)
    try:
        m = pattern.match(matchString)
        m.span()
        if m.start() != 0 or len(matchString)>36:
            return False
        else:
            return True
    except:
        return False

#Define Function for checking time format
def time_Checker(matchString):
    pattern = re.compile('[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])[T]'\
                         '([01]?\d|2[0-3]):([0-5]?\d):?([0-5]?\d)[.][0]{3}[Z]')
    matchString = str(matchString)
    try:
        m = pattern.match(matchString)
        m.span()
        if m.start() != 0 or len(matchString)>24:
            return False
        else:
            return True
    except:
        return False

#Define Function for Checking User format  
def user_Checker(matchString):
    matchString = str(matchString[-4:])
    pattern = re.compile('[a-z]\d{3}')
    try:
        m = pattern.match(matchString)
        m.span()
        if m.start()!=0 or m.end()<4:
            return False
        else:
            return True
    except:
        return False
    
#%%
#Report Invalidities and their corresponding locations
numErrors = 0
with open(csvFilename) as csvFile:
    csvReader = csv.DictReader(csvFile)
    #Try to iterate through each row of file
    try:    
        for row in csvReader:
            #check if there are more than 5 fields in data
            if len(row)>5:
                print("Error with Entry: "+str(csvReader.line_num)+". Too many fields detected.")
                numErrors +=1
            #check if there are less than 5 fields in data
            if len(row)<5:
                print("Error with Entry: "+str(csvReader.line_num)+". Not all fields are detected.")
                numErrors +=1
            #check if call-id and media-id follow proper format
            if id_Checker(row['call-id'])==False:
                print("Error with Entry: "+str(csvReader.line_num)+". Data does not follow call-id format.")
                numErrors += 1
            if id_Checker(row['media-id'])==False:
                print("Error with Entry: "+str(csvReader.line_num)+". Data does not follow media-id format.")
                numErrors += 1   
            #check if Time follows proper format
            if time_Checker(row['start'])==False:
                print("Error with Entry: "+str(csvReader.line_num)+". Data does not follow start time format.")
                numErrors +=1
            if time_Checker(row['end'])==False:
                print("Error with Entry: "+str(csvReader.line_num)+". Data does not follow end time format.")
                numErrors +=1
            #Check Valid User Format
            if user_Checker(row['user'])==False:
                print("Error with Entry: "+str(csvReader.line_num)+". Data does not follow user format.")
                numErrors +=1                
    #Exception if row is unable to be read
    except:
        numErrors += 1
        print("\nUnable to Encode Entry: "+str(csvReader.line_num+1)+". Abnormal encoding type at this location.")
        sys.exit('Terminating Program...')
        

#Let user know if file passes validation script
if numErrors == 0:
    print('File Passes Validation') 
#%%