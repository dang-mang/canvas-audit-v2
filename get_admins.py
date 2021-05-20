import os
import subprocess
import pandas
from config import *
from fix_json import *
directory = "data/"
input_filename = directory + "input.json"
output_filename = directory + "output.csv"
def get_command(sys_id):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL[0]}{sys_id}{URL[1]}\" >> {input_filename}"
def get_IDs(): 
    #get data from source
    data = pandas.read_csv(directory + "source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    print(f"Found {num_users} users in source.csv.\nPreparing to download data from {URL[0]}")
    return sys_IDs

def write_to_file(sys_IDs):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    os.system(f"echo \"[\" >> {input_filename}")
    num_users = len(sys_IDs) 
    for n in sys_IDs:
        os.system(get_command(n))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {input_filename}")    
        percent = sys_IDs.index(n)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)}/{num_users})")
    os.system(f"echo \"]\" >> {input_filename}")
    input_string = input_filename.split("/")[1]

    print(f"Finished downloading {num_users} rows of user data.\nNow converting {input_string} to {output_filename}")

def main():
    sys_IDs = get_IDs()
    write_to_file(sys_IDs)
    fix_json(input_filename)
if __name__ == "__main__":
    # execute only if run as a script
    main()

