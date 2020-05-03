#install these: pandas, xlwt, xlrd, csv. psycopg2-binary
import psycopg2
import pandas as pd
import xlwt
import csv

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def convert_it():
    conn = psycopg2.connect(host="ec2-18-235-20-228.compute-1.amazonaws.com",database="d541dctpgsmsse", user="gfwqeznjqizuki", password="745f9be7c8779add122a2ffc9bde86565fbf809359f3fb33f382843b02403a83",port="5432")
    cursor = conn.cursor()
    cursor.execute("select * from user_data;")

    with open("survey.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    data = pd.read_csv("survey.csv")

    # valuable data
    total_count = len(data)

    males = list(data['gender']).count('Male')
    veg_males = list(zip(data['gender'],data['food_pref'])).count(('Male', 'VEG'))
    non_veg_males = list(zip(data['gender'],data['food_pref'])).count(('Male', 'NON-VEG'))
    egg_males = list(zip(data['gender'],data['food_pref'])).count(('Male', 'EGG'))

    females = list(data['gender']).count('Female')
    veg_females = list(zip(data['gender'],data['food_pref'])).count(('Female', 'VEG'))
    non_veg_females = list(zip(data['gender'],data['food_pref'])).count(('Female', 'NON-VEG'))
    egg_females = list(zip(data['gender'],data['food_pref'])).count(('Female', 'EGG'))

    # Initialising excel sheet
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    sheet2 = book.add_sheet('sheet2')

    # creating columns in sheet 1
    columns_headings=['Sr no.','email','name','gender','age','state','city','time_taken','time_stamp']
    for i,v in enumerate(columns_headings):
        sheet1.write(0,i,v)

    columns_headings.pop(0)

    # entering data in sheet 1
    for i in range(len(data)):
        sheet1.write(i+1,0,i+1)
        for j,v in enumerate(columns_headings):
            sheet1.write(i+1,j+1,str(data[v][i]))

    # CREATING STRUCTURED DATA
    structured_data = []
    abc = ['A','B','C','D','E','F','G','H','I','J','K','L']
    for i1,u in enumerate(['NK','NL','XL']):
        for i2,w in enumerate(['beverages','snacks','main_courses','others']):
            for i,v in enumerate(data[w+u]):
                temp = v.replace('\'','').replace(' ','').replace('{','').replace('}','').replace('\"','').split(',')
                for e in temp:
                    if e == '':
                        temp.remove('')
                for m in temp:
                    structured_data.append((m,data['gender'][i],w+u+' '+abc[4*i1+i2]))
        
    sample_model = pd.read_excel('sample-model.xlsx')

    #copying sample data
    for i,v in enumerate(sample_model):
        sheet2.write(0,i,v)
    for i,v in enumerate(sample_model):
        for j,k in enumerate(sample_model[v]):
            if type(k)==type(1.0):
                pass
            else:
                sheet2.write(j+1,i,k)

    mdlis=[]
    fdlis=[]
    def tableFill(male_index,n):
        mtempdlis = []
        ftempdlis = []
        for a in range(n):
            
            mc=structured_data.count((sample_model[list(sample_model)[male_index-2]][a].replace('\'','').replace(' ','').replace('\"',''),'Male',list(sample_model)[male_index-2]))
            fc=structured_data.count((sample_model[list(sample_model)[male_index-2]][a].replace('\'','').replace(' ','').replace('\"',''),'Female',list(sample_model)[male_index-2]))
            d1=1
            # VEG NON-VEG EGG BOTH
            cri=sample_model[list(sample_model)[male_index-1]][a]
            if  cri== 'VEG':
                d1=veg_males+non_veg_males+egg_males
            elif cri=='NON-VEG':
                d1=non_veg_males
            elif cri=='BOTH':
                d1=veg_males+non_veg_males+egg_males
            elif cri=='EGG':
                d1=non_veg_males+egg_males
            d2=1
            # VEG NON-VEG EGG BOTH
            cri=sample_model[list(sample_model)[male_index-1]][a]
            if  cri== 'VEG':
                d2=veg_females+non_veg_females+egg_females
            elif cri=='NON-VEG':
                d2=non_veg_females
            elif cri=='BOTH':
                d2=veg_females+non_veg_females+egg_females
            elif cri=='EGG':
                d2=non_veg_females+egg_females
            mtempdlis.append(mc)
            ftempdlis.append(fc)
            try:sheet2.write(a+1,male_index,'{:.2f}'.format(mc/d1))
            except :pass
            try:sheet2.write(a+1,male_index+1,'{:.2f}'.format(fc/d2))
            except :pass
            try:sheet2.write(a+1,male_index+2,'{:.2f}'.format((mc+fc)/(d2+d1)))
            except :pass
        mdlis.append(mtempdlis)
        fdlis.append(ftempdlis)

    def tableFill2(male_index,n,ml,fl):
        for a in range(n):
            mc=structured_data.count((sample_model[list(sample_model)[male_index-2]][a].replace('\'','').replace(' ','').replace('\"',''),'Male',list(sample_model)[male_index-2]))
            fc=structured_data.count((sample_model[list(sample_model)[male_index-2]][a].replace('\'','').replace(' ','').replace('\"',''),'Female',list(sample_model)[male_index-2]))
            d1=1
            # VEG NON-VEG EGG BOTH
            cri=sample_model[list(sample_model)[male_index-1]][a]
            if  cri== 'VEG':
                d1=veg_males+non_veg_males+egg_males
            elif cri=='NON-VEG':
                d1=non_veg_males
            elif cri=='BOTH':
                d1=veg_males+non_veg_males+egg_males
            elif cri=='EGG':
                d1=non_veg_males+egg_males
            d1-=ml[a]
            d2=1
            # VEG NON-VEG EGG BOTH
            cri=sample_model[list(sample_model)[male_index-1]][a]
            if  cri== 'VEG':
                d2=veg_females+non_veg_females+egg_females
            elif cri=='NON-VEG':
                d2=non_veg_females
            elif cri=='BOTH':
                d2=veg_females+non_veg_females+egg_females
            elif cri=='EGG':
                d2=non_veg_females+egg_females
            d2-=fl[a]
            try:sheet2.write(a+1,male_index,'{:.2f}'.format(mc/d1))
            except: pass
            try:sheet2.write(a+1,male_index+1,'{:.2f}'.format(fc/d2))
            except: pass
            try:sheet2.write(a+1,male_index+2,'{:.2f}'.format((mc+fc)/(d1+d2)))
            except: pass
    tableFill(2,16)
    tableFill(7,57)
    tableFill(12,36)
    tableFill(17,12)
    tableFill2(22,16,mdlis[0],fdlis[0])
    tableFill2(27,57,mdlis[1],fdlis[1])
    tableFill2(32,36,mdlis[2],fdlis[2])
    tableFill2(37,12,mdlis[3],fdlis[3])
    tableFill2(42,16,mdlis[0],fdlis[0])
    tableFill2(47,57,mdlis[1],fdlis[1])
    tableFill2(52,36,mdlis[2],fdlis[2])
    tableFill2(57,12,mdlis[3],fdlis[3])

    book.save("output.xls")
    xltodrive()

def xltodrive():
    file_name = 'output.xls'
    gauth = GoogleAuth()
    gauth.CommandLineAuth()

    drive = GoogleDrive(gauth)

    filex = drive.CreateFile()
    filex.SetContentFile(file_name)
    filex.Upload()
    # print(f"Uploading {file_name}...")


# convert_it()