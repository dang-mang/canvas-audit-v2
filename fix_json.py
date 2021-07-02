import os
import sys
import fileinput

def fix_json(input_filename='input.json', directory = "data/", storage_path = "data/first/", output_filename = "output.csv"):
    output_path = directory + output_filename
    input_path = storage_path + input_filename
    clean_path = storage_path + input_filename.split(".")[0] + "_clean.json"
    remove_empty_lines(input_path, clean_path)
    with open(input_path) as f:
        #new_text=f.read().replace('}{', '},\n{').replace("]\n[",",").replace(",\n]","\n]")
        #new_text=f.read().replace('[', '').replace(']','').replace('}\n{','},\n{').replace('}{', '},\n{').replace(',\n,',',\n')
        new_text=f.read().replace('][', '],\n[').replace('}{', '},\n{')
        
    with open(clean_path, "w") as f:
        f.write(new_text)

    os.system(f"python3 json_to_csv.py l {clean_path} {output_path}")

def remove_empty_lines(input_path, clean_path):
    char = '{'
    newfile = open(clean_path, 'w')
    for line in open(input_path, 'r'):
        if char in line:
            newfile.write(line)
    newfile.close()

def main():
    fix_json()

if __name__ == "__main__":
    # execute only if run as a script
    main()
