import requests
import pandas as pd
from bs4 import BeautifulSoup as BS
from datetime import datetime

root_url = 'https://fhir.monash.edu/hapi-fhir-jpaserver/fhir/'

dReport_url= root_url +"DiagnosticReport"

data3 = pd.DataFrame(columns =['patientid','gender', 'birthDate',  'maritualStatus', 'totalCholesterol',"Triglycerides", 'lowDensity', 'highDensity', 'issued'] )

def checkDate(patient_id,new_date):
    # check whether the observation's issued date is the latest
    if patient_id not in data3.index:
        return True
    else:
        old_date = data3.loc[patient_id,'issued']
        if new_date > old_date:
            data3.drop([patient_id])
            return True
        else:
            return False



next_page = True
next_url = dReport_url
count_page = 0
count_patient = 0

while next_page == True:
    dReports = requests.get(url=next_url).json()
    
    # As discussed before, The monash FHIR server return results in a series of pages. 
    # Each page contains 10 results as default.
    # here we check and record the next page 
    next_page = False
    links = dReports['link']
    for i in range(len(links)):
        link=links[i]
        if link['relation'] == 'next':
            next_page = True
            next_url = link['url']
            count_page += 1
            
    # Extract data 
    entry = dReports['entry']
    for i in range(len(entry)):
        patient_array = []
        results = entry[i]['resource']['result']
        
        # l = []
        # for tr in elem:
        #     td = tr.find_all('td')
        #     row = [tr.text for tr in td]
        #     l.append(row)
        # print(pd.DataFrame(l, columns=["A", "B", "C", "D", "E"]))
        # print("----------------------------------------------")
        # print("----------------------------------------------")
        # print("----------------------------------------------")
        # print("----------------------------------------------")
        
        # Check whether this observation is on chterol or not.
        print("----------------------------------------------")
        print("----------------------------------------------")
        print("----------------------------------------------")

        patient_id = entry[i]['resource']['subject']['reference'][len('Patient/'):]
        issued = entry[i]['resource']['issued'][:len('2008-10-14')]
        date = datetime.strptime(issued, '%Y-%m-%d').date()

        # Get patient's basic information
        patient_data = requests.get(url = root_url+"Patient/"+patient_id).json()

        gender = patient_data['gender']
        birth = patient_data['birthDate']
        birthDate = datetime.strptime(birth, '%Y-%m-%d').date()
        maritalStatus = patient_data['maritalStatus']['text']
        
        patient_array.append(patient_id)
        patient_array.append(gender)
        patient_array.append(birthDate)
        patient_array.append(maritalStatus)

        print(results)
        for result in results:
        #for result in results:        
            # Check if the patient's Chterol value has already been recorded in the dataframe
           
            # Record chtoral(including total, Triglycerides, lowDensity and highDensity) value
            
            # observation_ref = result['reference']
            # observation_data = requests.get(url = root_url + observation_ref).json()
            #print(observation_data['code']['text'])
            # value = observation_data['valueQuantity']['value']
            # patient_array.append(value)
            # patient_array.append(date)
            # print(patient_array)
            # data3.append(patient_array)
        #print(patient_array)
        # print(data3)
        # print("----------------------------------------------")
        # print("----------------------------------------------")
        # print("----------------------------------------------")