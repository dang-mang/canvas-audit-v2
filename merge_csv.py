import pandas as pd
import glob
import os

def merge_csv():
    # making data frame from csv file
      
    # changing index cols with rename()
    csv_files=["source.csv", "admins.csv"]

    #get data from source
    data = pd.read_csv("source.csv", header=0)
    sys_IDs = list(data['canvas_user_id'].to_list())
    num_users = len(sys_IDs) 
    
    combined
    df = pd.DataFrame().reindex_like(combined_csv)
    for x in sys_IDs:
        z = combined_csv.loc[combined_csv['l_id']==x]
        for row in z:
            df.loc[len(df.index)] = row
        print(f"row {df.index} finished")
    print(df)

def main():
    merge_csv()

if __name__ == "__main__":
    # execute only if run as a script
    main()


