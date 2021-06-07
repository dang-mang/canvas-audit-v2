import os
import sys
import fileinput

def fix_json(input_filename='input.json', directory = "data/", output_filename = "output.csv"):
    output_path = directory + output_filename
    input_path = directory + input_filename
    clean_path = directory + 'input_clean.json'
    remove_empty_lines(input_path, clean_path)
    with open(clean_path) as f:
        #newText=f.read().replace('}{', '},\n{').replace("]\n[",",").replace(",\n]","\n]")
        newText=f.read().replace('[', '').replace("]","").replace('}\n{','},\n{').replace('}{', '},\n{').replace(',\n,',',\n')
        newText= newText.replace('[', '').replace("]","")
        newText= "[{0}]".format(newText)
        
    with open(input_path, "w") as f:
        f.write(newText)
    
    os.system(f"python3 json_to_csv.py l {input_path} {output_path}")

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

