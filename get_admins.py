import subprocess
import pandas as pd
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
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL_to_use[0]}{sys_id}{URL_to_use[1]}\" >> {out}"

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

def write_to_file(URL_to_use,sys_IDs, inp = input_filename, csv = output_filename, destination = directory):
    inp = destination + inp
    os.system(f"echo \"[\" >> {inp}")
    num_users = len(sys_IDs) 
    for n in sys_IDs:
        os.system(get_command(URL_to_use, n, inp))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {inp}")    
        percent = sys_IDs.index(n)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)}/{num_users})")
    os.system(f"echo \"]\" >> {inp}")
    input_string = inp.split("/")[1]

    print(f"Finished downloading {num_users} rows of user data.\nNow converting {input_string} to {csv}")

def merge_IDs(directory = directory, file1 = 'merged.csv' ,file2 ='logins.csv'):
    print("Processing student accounts")
    #df1 is 'l_0'
    df1 = pd.read_csv(directory + file1, header=0)
    #df2 is just 'l_'
    df2 = pd.read_csv(directory + file2, header=0)
    
    #print(df1)
    count = 0
    length = df1.shape[0]
    for i1, row1 in df1.iterrows():
        for i2, row2 in df2.iterrows(): 
            #print(i1 / length * 100, '%')
            login_id = row2['l_login_id']
            sis_id = row1['l_0_sis_user_id']
            if str(login_id) in str(sis_id) and 'nan' != str(login_id):
                #print(f"{count+1}:{login_id} is in {sis_id}.")    
                df2.at[i2, 'l_login_id'] = str(row1['l_0_sis_user_id'])
                df1.at[i1, 'l_0_sis_user_id'] = str(row1['l_0_sis_user_id'])
                count += 1
    print(f"{count} student accounts with matching admin accounts found.")
    print("Generating .csv file..."

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
    df_merged = df_renamed.merge(df2, how='left', on='l_login_id')

    #dataframe to CSV 
    df_merged.to_csv(directory+'with_ids.csv', index=False, header=True)
    print(f".csv file creatd with {count} student and admin accounts merged")

def clean_csv(input_filename = 'with_ids.csv'):
    #put code to rename the columns of the file to make them readable for the end user
    #create a new file and put it in the main directory, not the data/ directory
    pass

def collapse_csv(destination = directory, filename = "output.csv"):
    with open(destination + filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    length = len(data) 
    #put data in their own row
    print("Processing data...")
    for i, value in enumerate(data):
        if i != 0 and len(value) > 9: 
            if value[9] != '':
                data.insert(i,value[9:17])
            if value[18] != '':
                data.insert(i,value[18:26])
            if(i >= length):
                break
    
    #remove empties
    for i,x in enumerate(data):
        for z in x:
            if z == '':
                x.remove(z)
        data[i] = data[i][0:9]
    #data[0] = data[0][0:9]

    with open(directory+'collapsed.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerows(data)   
    print("Data processing complete.")
    
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
   
    usernames = get_usernames()
    print(usernames)
    

    #get i-numbers from API
    print("Fetching IDs from API...")
    login_in = "logins.json"
    login_out = "logins.csv"
    write_to_file(URL_LOGIN, usernames, inp = login_in, destination = first, csv = login_out)
    fix_json(input_filename = login_in ,output_filename = login_out)
    print("IDs fetched from API.")
    
    print("Merging student account information with their admin accounts...")
    merge_IDs()
    print("Student account merge complete.")
    print("Cleaning up final csv file (not implemented yet")
    clean_csv()

    #merge_csv(source_filename = 'merged.csv', output_filename = 'logins.csv', directory = 'data/',first = 'l_0_id', last = 'canvas_user_id', final = 'final.csv')

    #print("Merging final CSV file...")
    #fix_csv()

    #merge_csv(source_filename = 'id.csv', output_filename = 'merged.csv', final = 'admins_final.csv', first = 'l_email' ,last = 'l_email')
    #print("Final CSV file successfully generated. Cleaning files...")
    #clean_files()
    print("Process complete.")

if __name__ == "__main__":
    # execute only if run as a script
    main()

