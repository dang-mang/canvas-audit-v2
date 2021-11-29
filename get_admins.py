import subprocess
import pandas as pd
import numpy as np
import csv
from config import *
from pathlib import Path
from fix_json import *
from fix_csv import *
from merge_csv import *
from concat_IDs import *
directory = "data/"
input_filename = "input.json"
output_filename = "output.csv"

def get_command(URL_to_use, sys_id,out = input_filename):
    command = f"curl -H \"Authorization: Bearer {token}\" \"{URL_to_use[0]}{sys_id}{URL_to_use[1]}\" >> {out}" 
    print(command)
    return command 


def get_IDs(): 
    #get data from source
    data = pd.read_csv("source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    print(f"Found {num_users} users in source.csv.\nPreparing to download data from {URL[0]}")
    return sys_IDs

def get_usernames(input_filename = "merged.csv"):
    #get data from source                        
    data = pd.read_csv(directory + input_filename, header=0)
    usernames = list(data['l_0_sis_user_id'].to_list())
    num_users = len(usernames)
    print(f"Found {num_users} users in {input_filename}.\nPreparing to download data from {URL_LOGIN[0]}")
    
    #remove underscores
    clean = []
    for u in usernames:
        clean.append(str(u))
    
    usernames = []
    clean = [u for u in clean if '_' in u]
    for u in clean:
        usernames.append(u.split('_')[1])
    
    clean = []
    for u in usernames:
        if u not in clean:
            clean.append(u)
    return clean
#    #get data from source
#    data = pd.read_csv(directory + input_filename, header=0)
#    usernames = list(data['l_0_sis_user_id'].to_list())
#    num_users = len(usernames) 
#    print(f"Found {num_users} users in {input_filename}.\nPreparing to download data from {URL_LOGIN[0]}")
#    
#    #remove underscores
#    clean = []
#    for u in usernames:
#        clean.append(str(u))
#   
#    return clean
#    
#    usernames = []
#    clean = [u for u in clean if '_' in u]
#    for u in clean:
#        usernames.append(u.split('_')[1])
#    
#    clean = []
#    for u in usernames:
#        if u not in clean:
#            clean.append(u)
#    
#    return clean
#    return usernames

def write_to_file(URL_to_use,sys_IDs, inp = input_filename, csv = output_filename, destination = directory):
    
    inp = destination + inp
    print(f"filename = {inp}, output = {directory}{output_filename}")
    print(inp)
    os.system(f"echo \"[\" >> {inp}")
    num_users = len(sys_IDs) 
    print(sys_IDs)

    c = 0
    for n in sys_IDs:
        print(f"index = {sys_IDs.index(n)}, count = {c}")
        c+=1
        os.system(get_command(URL_to_use, n, inp))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {inp}")    
        percent = (sys_IDs.index(n)+1)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)+1}/{num_users})")
    os.system(f"echo \"]\" >> {inp}")
    input_string = inp.split("/")[1]

    print(f"Finished downloading {num_users} rows of user data.\nNow converting {input_string} to {csv}")

#def merge_IDs(directory = directory, file1 = 'merged.csv' ,file2 ='logins.csv'):
def merge_IDs(directory = directory, file1 = 'collapsed.csv' ,file2 ='logins.csv'):
    print("Processing student accounts...")
    #df1 is 'l_0'
    df1 = pd.read_csv(directory + file1, header=0)
    #df2 is just 'l_'
    df2 = pd.read_csv(directory + file2, header=0)
    
    #print(df1)
    count = 0
    length = df1.shape[0]
    for i1, row1 in df1.iterrows():
        for i2, row2 in df2.iterrows(): 
            #print(i1 / length * 100, '%)
            first = 'l_login_id'
            last = 'l_0_sis_user_id'
            login_id = row2[first]
            sis_id = row1[last]
            if str(login_id) in str(sis_id) and 'nan' != str(login_id):
                #print(login_id, sis_id)
                #print(f"{count+1}:{login_id} is in {sis_id}.")    
                df2.at[i2, first] = str(row1[last])
                df1.at[i1, last] = str(row1[last])
                count += 1
    print(f"{count} student accounts with matching admin accounts found.")
    print("Generating .csv file...")

    count = 0
    length = df1.shape[0]
    for i1, row1 in df1.iterrows():
        for i2, row2 in df2.iterrows(): 
            #print(i1 / length * 100, '%')
            login_id = row2['l_login_id']
            sis_id = row1['l_0_sis_user_id']
            if str(login_id) == str(sis_id) and 'nan' != str(login_id):
                #print(f"{count+1}:{login_id} == {sis_id}.")    
                count += 1

    df_renamed = df1.rename(columns = {'l_0_sis_user_id':'l_login_id'})

    #merge dataframes
    df_merged = df_renamed.merge(df2, how='left', on='l_login_id').drop_duplicates()

    #dataframe to CSV 
    df_merged.to_csv(directory+'with_ids.csv', index=False, header=True)
    print(f".csv file creatd with {count} student and admin accounts merged")

def clean_csv(input_filename = 'with_ids.csv'):
    #put code to rename the columns of the file to make them readable for the end user
    final_filename = directory + "admins_final.csv"
    with open(directory + input_filename, 'r') as fin:
        data = fin.read().splitlines(True)

    f1 = open(final_filename, 'w')

    f1.write("Account Level(?),Authentication Provider ID(?),Account Creation Date,? Unknown ID 1,Extra ID 1(?),Extra ID 1(?),Login Username,Unique Canvas ID,?,Full Name,I-Number,Student E-Mail,Account Type,Role ID,Role,Status,Created by (?),Root Domain,Student Avatar URL,Student Account Creation Date,Student Email,Error Report(?),L ID (?),L Integration ID (?),Student Last Login Date,Locale (?),Full Name,Avatar Update Permissions,Name Update Permissions,Limit Parent Web Acces Permissions,Root Account URL,Student Short Name,SIS Import ID,Student I-Number,Student Sortable Name\n")
    f1.writelines(data[1:])
    print(f"CSV file cleaned and written as \"{final_filename}\".")


def collapse_csv(destination = directory, filename = "output.csv"):
    with open(destination + filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    length = len(data) 
    #put data in their own row
    print("Processing data to collapse dataframe...")
    for i, value in enumerate(data):
        if i != 0 and len(value) > 9: 
            if value[9] != '':
                data.insert(i,value[9:17])
            if value[18] != '':
                data.insert(i,value[18:26])
            if(i >= length):
                break
    
    #remove empties
   # for i,x in enumerate(data):
   #     for z in x:
   #         if z == '':
   #             x.remove(z)
   #     data[i] = data[i][0:9]
    #data[0] = data[0][0:9]

    with open(directory+'collapsed.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(data)   
    print("Data processing complete.")
    
def source_merge():
    df1 = pd.read_csv("source.csv", header=0)
    df2 = pd.read_csv(directory + "admins_final.csv", header=0)
    id_string = 'Unique Canvas ID'

    df_renamed = df1.rename(columns = {'canvas_user_id':'Unique Canvas ID'})
    #remove duplicates from source
    df_renamed[['Unique Canvas ID']] = df_renamed[['Unique Canvas ID']].fillna(0)
    df_renamed = df_renamed.drop_duplicates('Unique Canvas ID',keep='first')
    df2[['Unique Canvas ID']] = df2[['Unique Canvas ID']].fillna(0)
    
    df_renamed[id_string] = df_renamed[id_string].astype(str)
    df2[id_string] = df2[id_string].astype(str)

        
    #merge dataframes
    df_merged = df2.merge(df_renamed, how='outer', on=id_string).drop_duplicates()
    #df_merged = pd.merge(df_renamed,df2,on=id_string)
    
    
    #change column order and names
    i0_column = df_merged.pop('admin_user_name')
    i1_column = df_merged.pop('Student Last Login Date')
    i2_column = df_merged.pop('user_id')
    i3_column = df_merged.pop('Login Username')

    df_merged.insert(0,'Name',i0_column)
    df_merged.insert(1,'I-Number (student)',i1_column)
    df_merged.insert(2,'I-Number (employee)',i2_column)
    df_merged.insert(3,'Employee Login',i3_column)
    
    df_merged = df_merged.rename(columns={"Full Name": "Profile Picture link",
        "Created by (?)": "Language(?)",
        "I-Number":"Account Creation Date",
        "Root Domain":"Student Account Name",
        "Student Avatar URL":"Update Avatar Permission",
        "Student Account Creation Date":"Update Name Permission",
        "Student Email":"Limit Parent Web app Permission",
        "Error Report(?)":"Root Account URL",
        "L ID (?)":"Short Name",
        "L Integration ID (?)":"SIS Import ID",
        "Locale (?)":"Sortable Name",
        "Status":"Last Login Date",
        "Role ID":"? Unknown ID #2"})

    df_merged.pop("Full Name.1")
    df_merged.pop("Avatar Update Permissions")
    df_merged.pop("Name Update Permissions")
    df_merged.pop("Limit Parent Web Acces Permissions")
    df_merged.pop("Root Account URL")
    df_merged.pop("Student Short Name")
    df_merged.pop("SIS Import ID")
    df_merged.pop("Student I-Number")
    df_merged.pop("Student Sortable Name")
    #dataframe to CSV 
    df_merged.to_csv('report.csv', index=False, header=True)
    print("final report created and written as \"report.csv\"")

def clean_files(path):  
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))
 
def main():
    #get sys ids from source file
    sys_IDs = get_IDs()
    
    #prep
    first = directory + "first/"
    os.makedirs(first, exist_ok=True)
    clean_files(first)


    #first API call for IDs
    write_to_file(URL, sys_IDs, destination = first)
    print("Fixing JSON and converting to CSV...")
    fix_json()
    print("CSV file created.")

    collapse_csv() 
 
    #merge source and generated
    print("Merging source file and output file...")
    merge_csv(output_filename = "collapsed.csv")
    print("CSV file merged.")
  
    #print(usernames)
   

    #get i-numbers from API
    usernames = get_usernames()
    print(usernames)
    print("Fetching IDs from API...")
    login_in = "logins.json"
    login_out = "logins.csv"
    
    #removes all "None" and  instances from usernames list
    usernames = [u for u in usernames if u != "None"]
    usernames = [u for u in usernames if u != "nan"]
    write_to_file(URL_LOGIN, usernames, inp = login_in, destination = first, csv = login_out)
    fix_json(input_filename = login_in ,output_filename = login_out)
    print("IDs fetched from API.")
  
    print("Merging student account information with their admin accounts...")
    merge_IDs()
    print("Student account merge complete.")
    print("Cleaning up final csv file...")
    clean_csv()
    source_merge()
    
    print("Process complete.")


if __name__ == "__main__":
    # execute only if run as a script
    main() 
