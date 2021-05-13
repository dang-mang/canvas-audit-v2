import os
import subprocess
import pandas
from config import *
from fix_json import *
input_filename = "./input.json"

def get_command(sys_id):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL[0]}{sys_id}{URL[1]}\" >> {input_filename}"

def main():
    #get data from source
    data = pandas.read_csv("source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    print(f"Found {num_users} users in source.csv.\nPreparing to download data from {URL[0]}")
    
    #write to file
    os.system(f"echo \"[\" >> {input_filename}")
    for n in sys_IDs:
        os.system(get_command(n))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {input_filename}")    
        percent = sys_IDs.index(n)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)}/{num_users})")

    os.system(f"echo \"]\" >> {input_filename}")
    input_string = input_filename.split("/")[1]
    print(f"Finished downloading {num_users} rows of user data.\nNow converting {input_string} to {output_filename}")
    fix_json(input_filename, output_filename)
if __name__ == "__main__":
    # execute only if run as a script
    main()

