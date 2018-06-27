'''
Created on Jun 24, 2018

@author: Mark Holton
'''

import sys
from _ast import Num
from array import array
import pandas as pd
import numpy as np
from pywin.scintilla import control

textfile = sys.argv[1]
with open(textfile,'r') as i:
    lines = i.readlines() 
print("start")


def lineToArray(line):
    line=line.rstrip()
    array = line.split("\t")
    return array

masterDF = pd.DataFrame()
# index=1
# indxs=[]
# for line in lines:
#     if(index==1):
#         indxs=lineToArray(line)
#         index=index+1
#         continue
#     sampList = lineToArray(line)
#     df1=pd.DataFrame({indxs[0]:indxs, sampList[0]:sampList},index=indxs)
#     if(index==2):
#         print(df1)
#         masterDF=df1
#         index=index+1
#         continue
#     tempArr=[masterDF,df1]
#     masterDF=pd.merge(masterDF,df1,how="outer",on=indxs[0])
#     if(index==3):
#         print(df1)
#         print(masterDF)
#     if(index==50):
#         print(df1)
#         print(masterDF)
#         break
#     print(index)
#     index=index+1
#         
# print(masterDF)



#get values for antibiotics as array and cycle through
#if value is not (some value) then add to new dataframe
#return data frame



#built other way
#build dictionary first, then pass dict to dataframe as arg
dataDict = {}
index=0
indxs=[]
colums=[]
tempDArray=[]
for line in lines:
    if(index==0):
        colums=lineToArray(line)
        index=index+1
        continue
    sampList = lineToArray(line)
    counter=0
    for element in sampList:
        index_name=colums[counter]
        if counter==0:
            indxs.append(sampList[0])  
        if index_name in dataDict:
            tempDArray=dataDict.get(index_name)
            tempDArray.append(element)
            dataDict[index_name]=tempDArray
        else:
            dataDict[index_name]=[element]
        counter=counter+1
   
    print(index)
    if(index==200):
        break
    index=index+1
        
masterDF=pd.DataFrame(dataDict,index=indxs)
print(masterDF)

# antibots_list=masterDF["antibiotic_history"]
# count=0
# for element in antibots_list:
#     if element!="I have not taken antibiotics in the past year.":
#         masterDF=masterDF.drop(indxs[count])
#     count=count+1
# print(masterDF)

def multiDrop_mental(is_control,colum_name , dbs_one,dbs_two,):
    mental_list_1_2=masterDF[colum_name]
    count=0
    retDF=masterDF
    for element in mental_list_1_2:
        if is_control==True and element==dbs_one or element == dbs_two:
            retDF=retDF.drop(indxs[count])
        if is_control==False and element!=dbs_one and element != dbs_two:
            retDF=retDF.drop(indxs[count])
        count=count+1

    return retDF
 
    
masterDF=masterDF[masterDF.antibiotic_history == "I have not taken antibiotics in the past year."]
print(masterDF)
indxs=masterDF["#SampleID"]

controlDF= multiDrop_mental(True,"depression_bipolar_schizophrenia", "Self-diagnosed", "Diagnosed by a medical professional (doctor, physician assistant)")
#controlDF=controlDF[ controlDF.mental_illness_type_depression != "Yes"]
print("on to mental")
mentalDF= multiDrop_mental(False,"depression_bipolar_schizophrenia", "Self-diagnosed", "Diagnosed by a medical professional (doctor, physician assistant)")
#mentalDF=mentalDF[ mentalDF.mental_illness_type_depression != "No"]

print(controlDF)

print("\nmental\n")
print(mentalDF)

depress_to_control_match_Dict={}
mentindexs=mentalDF["#SampleID"]
controlindexs=controlDF["#SampleID"]

print(controlindexs.size)
men_count=0
cont_count=0
while men_count < mentindexs.size:
    row=mentalDF.iloc[men_count]
    m_id=row.iloc[0]
    age=row.iloc[49]
    bmi=row.iloc[75]
    smoking =row.iloc[205]
    match_array=[]
    if(age=="Unspecified" or bmi=="Unspecified" or smoking=="Unspecified" ):
        print("error some info not given for " +m_id)
        men_count=men_count+1
        continue
    
    
    age=int(float(age))
    while cont_count < controlindexs.size:
        #print("running"+str(cont_count))
        con_row=controlDF.iloc[cont_count]
        con_id=con_row.iloc[0]
        if con_id=="10317.000020706":
            print("found")
        con_age=con_row.iloc[49]
        con_bmi=con_row.iloc[75]
        con_smoking =con_row.iloc[205]
        if con_age=="Unspecified":
            cont_count=cont_count+1
            continue
        con_age=int(float(con_age))
        if con_bmi==bmi and con_smoking==smoking and age-5<=con_age and con_age<=age+5 :
            match_array.append(con_id)
        cont_count=cont_count+1
    depress_to_control_match_Dict[m_id]=match_array    
    men_count=men_count+1
    
    
print(depress_to_control_match_Dict)
    



print("done")
   
    