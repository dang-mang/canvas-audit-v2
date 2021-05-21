import pandas as pd
import glob
import os

def merge_csv(source_filename = 'source.csv', output_filename = 'output.csv', directory = 'data/'):
    #change CSV to pandas dataframe
    df_source = pd.read_csv(directory + source_filename, header=0)
    df_output = pd.read_csv(directory + output_filename, header=0)
    
    #rename 
    df_renamed = df_output.rename(columns = {'l_id':'canvas_user_id'})

    #merge dataframes
    df_merged = df_renamed.merge(df_source, how='left', on='canvas_user_id')

    #dataframe to CSV 
    df_merged.to_csv(directory + 'merged.csv', index=False, header=True)
def main():
    merge_csv()

if __name__ == "__main__":
    # execute only if run as a script
    main()


