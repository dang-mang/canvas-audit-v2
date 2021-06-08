import pandas as pd
import os
import fileinput
from fix_json import *
from config import *
directory = "data/"
ID_path = directory + "id.json"
clean_path = directory + "id_clean.json"

def get_usernames(): 
    input_path = directory+'input.csv'
    #get data from source
    data = pd.read_csv(input_path, header=0)
    usernames = list(data['l_email'].to_list())
    
    no_dupes = []
    for i in usernames:
        if i not in no_dupes:
            no_dupes.append(i)
    
    usernames = []
    for u in no_dupes:
        usernames.append(str(u).split('@')[0])
    

    num_users = len(usernames) 
    print(f"Found {num_users} usernames in {input_path}.\nPreparing to download data from {URL_LOGIN}")
    return usernames 
    

def get_command_id(username):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL_LOGIN}{username}\" >> {ID_path}"

def write_user(usernames):
    num_users = len(usernames)
    user_out_file = directory + "usernames.json"
    if os.path.exists(ID_path):
        os.remove(ID_path)

    os.system(f"echo \"[\" >> {ID_path}")
    for idx, u in enumerate(usernames):
        os.system(get_command_id(u))
        #if u != usernames[-1]:
        if idx+1 != num_users:
            os.system(f"echo \",\" >> {ID_path}")    
        percent = (idx+1)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({idx+1}/{num_users})")
    os.system(f"echo \"\\n]\" >> {ID_path}")
    input_string = ID_path.split("/")[1]
    print("Download complete.")

def read_lines(json_filename):
    phrase = "The specified resource does not exist."
    #for line in fileinput.input(ID_path, inplace=True):
    with open(json_filename) as oldfile, open(clean_path, 'w') as newfile:
        for line in oldfile:
            if not phrase in line:
                newfile.write(line)
    
def concat_IDs():
    usernames = get_usernames()
    write_user(usernames)
    read_lines(ID_path)
    print("Generating CSV file.")
    fix_json(clean_path, output_filename = "id.csv")

def main():
    concat_IDs()

if __name__ == "__main__":
    # execute only if run as a script
    main()

