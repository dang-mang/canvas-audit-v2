import pandas as pd
import os
import fileinput
from fix_json import *
from config import *
directory = "data/"
ID_path = directory + "id.json"

def get_usernames(): 
    #get data from source
    data = pd.read_csv(directory + "merged.csv", header=0)
    usernames = list(data['l_email'].to_list())
    
    no_dupes = []
    for i in usernames:
        if i not in no_dupes:
            no_dupes.append(i)
    
    usernames = []
    for u in no_dupes:
        usernames.append(str(u).split('@')[0])
    
    for u in usernames:
        print(u)

    num_users = len(usernames) 
    print(f"Found {num_users} usernames in merged.csv.\nPreparing to download data from {URL_ID}")
    return usernames 
    

def get_command_id(username):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL_ID}{username}\" >> {ID_path}"

def write_user(usernames):
    num_users = len(usernames)
    user_out_file = directory + "usernames.json"
    if os.path.exists(ID_path):
        os.remove(ID_path)

    os.system(f"echo \"[\" >> {ID_path}")
    for idx, u in enumerate(usernames):
        os.system(get_command_id(u))
        #if u != usernames[-1]:
        if idx+1 == num_users:
            os.system(f"echo \",\" >> {ID_path}")    
        percent = (idx+1)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({idx+1}/{num_users})")
    os.system(f"echo \"]\" >> {ID_path}")
    input_string = ID_path.split("/")[1]
    print("Download complete.")

def read_lines():
    phrase = "The specified resource does not exist."
    for line in fileinput.input(ID_path, inplace=True):
        if phrase in line:
            continue
        print(line, end='')
    

    
def concat_IDs():
    usernames = get_usernames()
    write_user(usernames)
    read_lines()
    print("Generating CSV file.")
    fix_json(ID_path, output_filename = "id.csv")

def main():
    concat_IDs()

if __name__ == "__main__":
    # execute only if run as a script
    main()
