import pandas as pd
import glob
import os

def merge_csv(source_filename = 'source.csv', output_filename = 'output.csv', directory = 'data/',first = 'l_0_id', last = 'canvas_user_id', final = 'merged.csv'):

    #change CSV to pandas dataframe
    df_source = pd.read_csv(source_filename, header=0).astype(str)
    df_output = pd.read_csv(directory + output_filename, header=0).astype(str)
    if final != 'admins_final.csv':
        final = directory + final
    #rename 
    df_renamed = df_output.rename(columns = {first:last})

    #merge dataframes
    df_merged = df_renamed.merge(df_source, how='left', on=last)

    #dataframe to CSV 
    df_merged.to_csv(final, index=False, header=True)

def main():
    merge_csv()

    print("Final CSV file successfully generated. Cleaning files...")

if __name__ == "__main__":
    # execute only if run as a script
    main()


