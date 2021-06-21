import os
import subprocess
import pandas as pd
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
    
    #merge source and generated
    print("Merging source file and output file...")
    merge_csv()
    print("CSV file merged.")
    
    #get i-numbers from API
    print("Fetching IDs from API...")
    login_in = "logins.json"
    login_out = "logins.csv"
    write_to_file(URL_LOGIN, sys_IDs, inp = login_in, destination = first, csv = login_out)
    fix_json(input_filename = login_in ,output_filename = login_out)
    print("IDs fetched from API.")

    #print("Merging final CSV file...")
    #fix_csv()

    #merge_csv(source_filename = 'id.csv', output_filename = 'merged.csv', final = 'admins_final.csv', first = 'l_email' ,last = 'l_email')
    #print("Final CSV file successfully generated. Cleaning files...")
    #clean_files()
    print("Process complete.")

if __name__ == "__main__":
    # execute only if run as a script
    main()

