import os
import subprocess
import pandas
from config import *
from json_to_csv import *
out_path = directory + "/" + filename

def get_command(sys_id):
    #generate command with sys id
    return f"curl -H \"Authorization: Bearer {token}\" \"{URL[0]}{sys_id}{URL[1]}\" >> {out_path}"

def main():
    #prepare directory for output
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    if os.path.exists(out_path):
        os.remove(out_path)
    
    #get data from source
    data = pandas.read_csv("source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    print(f"Found {num_users} users in source.csv.\nPreparing to download data from {URL[0]}")
    
    #write to file
    os.system(f"echo \"[\" >> {out_path}")
    for n in sys_IDs:
        os.system(get_command(n))
        if n != sys_IDs[-1]:
            os.system(f"echo \",\" >> {out_path}")    
        percent = sys_IDs.index(n)/num_users * 100 
        print(f"Download progress - {round(percent,2)}% ({sys_IDs.index(n)}/{num_users})")

    os.system(f"echo \"]\" >> {out_path}")
    print(f"Finished downloading {num_users} rows of user data.\nNow downloading ")
    flatten("input.csv", "list.csv")
if __name__ == "__main__":
    # execute only if run as a script
    main()

